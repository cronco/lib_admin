from django.forms import ModelForm, TextInput, MultiWidget, HiddenInput
from la.models import *

class AutoCompleteWidget(MultiWidget):


	def __init__(self, *args, **kwargs):
		widgets = (
				TextInput(attrs = {'class' : "autocomplete"}),
				HiddenInput()
				)
		super(AutoCompleteWidget, self).__init__(widgets, *args, **kwargs)

	def decompress(self, value):
		if value:
			return [data[0], data[1]]
		return [None, None]

		

	class Media:
		js = ('js/jquery-ui-1.8.16.custom.min.js',)
		css = {'all': ('js/css/jquery-ui-1.8.16.custom.css',) }

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



