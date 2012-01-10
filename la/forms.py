from django.forms import Form, ModelForm, TextInput, MultiWidget, HiddenInput, CheckboxInput, ModelChoiceField
from la.models import *

class AutoCompleteWidget(MultiWidget):

	def __init__(self, attrs = {}, *args, **kwargs):
		if 'class' in attrs:
			attrs['class'] = attrs['class'] + ' autocomplete'
		else:
			attrs['class'] = 'autocomplete'
		widgets = (
				TextInput(attrs = attrs),
				HiddenInput(attrs = attrs)
				)
		super(AutoCompleteWidget, self).__init__(widgets, *args, **kwargs)

	def decompress(self, value):
		if value:
			return [None, value]
		return [None, None]

		
	def value_from_datadict(self, data, files, name):
		return  data.get('%s_1' % name, None)

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
		self.fields['book'].widget = AutoCompleteWidget(attrs = {'data-search' :
			"book", 
			'data-role' : 'checkout-book'})
		self.fields['user'].widget = AutoCompleteWidget(attrs = 
								{'data-search' : "user",
								'data-role' : "checkout-user"})

class ExtraBookCheckoutForm(CheckoutForm):

	class Meta:
		model = Checkout
		exclude = ('extension', 'return_date')

	def __init__(self, *args, **kwargs):
		super(ExtraBookCheckoutForm, self).__init__(*args, **kwargs)
		self.fields['user'].widget = HiddenInput(attrs ={'class': 'extrauserfield'})


class CheckinForm(ModelForm):

	class Meta:
		model = Checkout
		fields = ('return_date', )


	def __init__(self, *args, **kwargs):
		super(CheckinForm, self).__init__(*args, **kwargs)
		self.fields['return_date'].widget = CheckboxInput()
		#self.fields['user'].widget = HiddenInput(attrs ={'class': 'extrauserfield'})

class AutoUserForm(Form):

	user = ModelChoiceField(
			queryset = User.objects.all(),
			widget = AutoCompleteWidget(attrs={
					"data-search" : "user",
					"data-role" : "checkin-user",
					"class" : "checkin-user",
					}))


