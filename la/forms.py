from django.forms import ModelForm, TextInput
from la.models import *

class AutoCompleteWidget(TextInput):


	def __init__(self, *args, **kwargs):
		super(AutoCompleteWidget, self).__init__(*args, **kwargs)
		self.attrs = {'class' : "autocomplete"}

	class Media:
		js = ('js/jquery-ui-1.8.16.custom.min.js',)

class CheckoutForm(ModelForm):


	class Meta:
		model = Checkout
		exclude = ('extension','return_date' )
		fields = ('user', 'book', )

	def __init__(self, *args, **kwargs):
		super(CheckoutForm, self).__init__(*args, **kwargs)
		self.fields['book'].widget = AutoCompleteWidget()

class ExtraBookCheckoutForm(CheckoutForm):

	class Meta:
		model = Checkout
		fields = ('book', )

	def __init__(self, *args, **kwargs):
		super(ExtraBookCheckoutForm, self).__init__(*args, **kwargs)



