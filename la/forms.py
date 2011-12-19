from django.forms import ModelForm
from la.models import *

class CheckoutForm(ModelForm):

	class Meta:
		model = Checkout
		exclude = ('extension','return_date' )

class ExtraBookCheckoutForm(CheckoutForm):

	class Meta:
		model = Checkout
		fields = ('book', )


