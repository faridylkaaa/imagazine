from django.conf import settings
from imagazine.goods.models import Goods

class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def save(self):
        self.session.modified = True
        
    def add(self, product, count=1):
        id_product = str(product.id)
        if id_product in self.cart.keys():
            self.cart[id_product] = {'count': self.cart[id_product].get('count', 0) + count, 'price': product.price}
        else:
            self.cart[id_product] = {'count': count, 'price': product.price}

        self.save()
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()
            
    def len(self):
        return sum(c['count'] for c in self.cart.values())
    
    def get_total_price(self):
        s = str(sum(c['count'] * c['price'] for c in self.cart.values()))
        return ''.join([s[i] + ' ' if i % 3 == 0 and i != len(s) else s[i] for i in range(-1, -len(s)-1, -1)])[::-1]
    
    def clear_cart(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True