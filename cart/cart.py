from decimal import Decimal
from django.conf import settings
from app.models import Product

class Cart(object):

    def __init__(self, request):
        """
        initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(setting.CART_SESSION_ID)
        if not cart:
            #save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID]= {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add aproduct to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        #update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        #mark the session as "modified" to make sure its saved
        self.session.modifed = True

    def remove(self.product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
