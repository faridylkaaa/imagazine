from django.shortcuts import render, redirect
from django.views import View
from .forms import CatrAddForm
from .cart import Cart
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Product

# Create your views here.
class AddProductCartView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Cart, id=kwargs['id'])
        form = CatrAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, cd['count'])
            messages.success(request, 'Товар добавлен в корзину успешно')
        else:
            messages.error(request, 'Товар не добавлен в корзину')
        return redirect('cart:index')
    
class RemoveProductCart(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['id'])
        cart.remove(product)
        return redirect('cart:index')
    
class IndexCart(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        d = dict()
        for i, v in cart.cart.items():
            d[Product.obects.get(id=i).product_set] = {'count': v.count, 'price': v.price}
        return render(request, 'cart/index.html', {'cart': d, 'cart_': cart})