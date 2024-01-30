from django.shortcuts import render, redirect
from django.views import View
from .forms import CatrAddForm
from .cart import Cart
from django.shortcuts import get_object_or_404
from django.contrib import messages
from imagazine.goods.models import Goods
from yookassa import Configuration, Payment
from imagazine.settings import *
from django.urls import reverse_lazy
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.core.mail import send_mail
from imagazine.cart.mixins import RightUserMixinOrder
from django.views.generic import DetailView
from imagazine.coupons.forms import CouponForm
from imagazine.coupons.models import Coupons
from datetime import datetime as dtim

Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY

def avaliable_item(cart, product, cd={'count': 0}):
    if cart.cart.get(str(product.id), False):
        if cd['count'] + cart.cart[str(product.id)]['count'] > product.count:
            return False
        return True
    elif cd['count'] > product.count:
        return False
    return True

def avaliable_cart(cart):
    lst = list()
    for k, v in cart.cart.items():
        product = get_object_or_404(Goods, id=k)
        lst.append(avaliable_item(cart, product))
    return all(lst)



# Create your views here.
class AddProductCartView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Goods, id=kwargs['id'])
        form = CatrAddForm(request.POST, initial={'count': 1})
        if form.is_valid():
            cd = form.clean()
            if avaliable_item(cart, product, cd):
                cart.add(product, cd['count'])
                messages.success(request, 'Товар добавлен в корзину успешно')
            else:
                messages.error(request, 'Товара нет в таком количестве')
        else:
            messages.error(request, 'Товар не добавлен в корзину')
        return redirect('cart:index')
    
class RemoveProductCart(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Goods, id=kwargs['id'])
        cart.remove(product)
        return redirect('cart:index')
    
class IndexCart(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        d = dict()
        for i, v in cart.cart.items():
            d[Goods.objects.get(id=i).get_model()] = {'count': v['count'], 'price': v['price']}
        return render(request, 'cart/index.html', {'cart': d, 'cart_': cart, 'form': CatrAddForm, 'form_p': CouponForm(initial={'coupon': request.session.get('code', '')})})
    
    def post(self, request, *args, **kwargs):
        form = CouponForm(request.POST)
        if form.is_valid():
            coupon = form.cleaned_data['coupon']
            datetime = dtim.now()
            try:
                c = Coupons.objects.get(code=coupon, valid_from__lte=datetime, valid_to__gte=datetime, active=True)
                discount = c.discount
                cart = Cart(request)
                cart.discount(discount)
                request.session['code'] = coupon
            except:
                messages.error(request, 'Нет такого промокода')
        
        return redirect('cart:index')
    
class PaymentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    
    def get(self, request, *args, **kwargs):
        idempotence_key = str(uuid.uuid4())
        cart = Cart(request)
        if avaliable_cart(cart):
            lst = list()
            for product_id, count_price in cart.cart.items():
                d = dict()
                d["description"] = get_object_or_404(Goods, id=product_id).name
                d["quantity"] = count_price['count']
                d['amount'] = {"value": count_price['price'] - (cart.session['discount'] / 100) * count_price['price'], "currency": "RUB"}
                d.update({"vat_code": "2",
                "payment_mode": "full_prepayment",
                "payment_subject": "commodity"})
                lst.append(d)
                
            payment = Payment.create({
                "amount": {
                "value": str(cart.price()),
                "currency": "RUB"
                },
                "receipt": {
                    "customer": {
                            "email": request.user.email
                },
                     "items": lst
    },
                "payment_method_data": {
                "type": "bank_card"
                },
                "confirmation": {
                "type": "redirect",
                "return_url": 'https://0ca1-79-139-191-0.ngrok-free.app'+ str(reverse_lazy('main'))
                },
                "capture": False,
                "description": "Заказ в Imag"
            }, idempotence_key)

            # get confirmation url
            confirmation_url = payment.confirmation.confirmation_url
            
            # модель заказа
            order = Order.objects.create(order_id=payment.id, customer=request.user, payment='no')
            for product_id, count_price in cart.cart.items():
                product = get_object_or_404(Goods, id=product_id)
                count = count_price['count']
                OrderItem.objects.create(order=order, product=product, count=count)
                
            order.price = int(payment['amount']['value'][:-3])
            order.created_at = payment['created_at']
            order.save()
            cart.clear_cart()
            return HttpResponseRedirect(confirmation_url)
        else:
            messages.error(request, 'Товара уже нет в таком количестве')
            return redirect('cart:index')
    
    
class YoomoneyNotifView(APIView):
    '''сюда приходит уведомление о том, что денбги переведены и дальше идет логика приложения'''
    def post(self, request):
        payment_id = request.data['object']['id']
        order = Order.objects.get(order_id=payment_id)
        for item in order.items.all():
            if item.count > item.product.count:
                response = Payment.cancel(payment_id, str(uuid.uuid4()))
                return Response(response, status=200)
            else:
                product = item.product
                product.count = product.count - item.count
                product.save()
        Payment.capture(payment_id)
        order.payment = 'yes'
        order.save()
        send_mail(
            f'Чек Imag {payment_id}',
            'Заказ оплачен и принят в магазине. Вы можете просмотреть его в соответсвующем поле "Заказы". Если возникли какие-то проблемы - напишите на почту faridylkaaa@yandex.ru',
            'faridylkaaa@yandex.ru',
            recipient_list=[order.customer.email],
            fail_silently=False
        )
        return Response(status=200)
    
class OrdersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.filter(payment='yes').order_by('-created_at')
        return render(request, 'cart/orders.html', {'orders': orders})
    
class OrderView(RightUserMixinOrder, DetailView):
    context_object_name = 'order'
    template_name = 'cart/order_profile.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Заказ №'+str(content['order'].id)
        content['count'] = sum(item.count for item in content['order'].items.all())
        return content