from django.conf import settings
from imagazine.goods.models import Game

class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def save(self):
        self.session.modified = True
        
    def add(self, product, count):
        id_product = str(product.id)
        is_game = isinstance(product.product_set, Game)
        self.cart[id_product] = {'count': self.cart.get('count', 0) + count, 'price': product.product_set.price, 'is_game': is_game}
        self.save()
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()
            
    def len(self):
        return sum(c['count'] for c in self.cart.values())
    
    def get_total_price(self):
        return sum(c['count'] * c['price'] for c in self.cart.values())
    
    def clear_cart(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True