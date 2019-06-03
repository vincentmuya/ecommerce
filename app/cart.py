from decimal import Decimal
from django.conf import settings
from .models import Item

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
