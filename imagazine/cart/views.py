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
        return render(request, 'cart/index.html', {'cart': d, 'cart_': cart, 'form': CatrAddForm})
    
class PaymentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    
    def get(self, request, *args, **kwargs):
        idempotence_key = str(uuid.uuid4())
        cart = Cart(request)
        if avaliable_cart(cart):
            payment = Payment.create({
                "amount": {
                "value": str(cart.price()),
                "currency": "RUB"
                },
                "payment_method_data": {
                "type": "bank_card"
                },
                "confirmation": {
                "type": "redirect",
                "return_url": 'https://fcc3-79-139-191-0.ngrok-free.app'+ str(reverse_lazy('main'))
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
        return Response(status=200)
