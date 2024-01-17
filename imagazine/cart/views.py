from django.shortcuts import render, redirect
from django.views import View
from .forms import CatrAddForm
from .cart import Cart
from django.shortcuts import get_object_or_404
from django.contrib import messages
from imagazine.goods.models import Goods

def avaliable(cd, cart, product):
    if cart.cart.get(str(product.id), False):
        if cd['count'] + cart.cart[str(product.id)]['count'] > product.count:
            return False
        return True
    elif cd['count'] > product.count:
        return False
    return True

# Create your views here.
class AddProductCartView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Goods, id=kwargs['id'])
        form = CatrAddForm(request.POST, initial={'count': 1})
        if form.is_valid():
            cd = form.clean()
            if avaliable(cd, cart, product):
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