from django.forms import Form, ModelForm, TextInput, MultiWidget, HiddenInput, CheckboxInput, ModelChoiceField, ValidationError
import isbn
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
			"data-role" : "checkout-book"})
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
		fields = ('return_date','extension', )


	def __init__(self, *args, **kwargs):
		super(CheckinForm, self).__init__(*args, **kwargs)
		self.fields['return_date'].widget = CheckboxInput()
		self.fields['extension'].widget.attrs = {'class' : 'autohidden'}

class AutoUserForm(Form):

	user = ModelChoiceField(
			queryset = User.objects.all(),
			widget = AutoCompleteWidget(attrs={
					"data-search" : "user",
					"data-role" : "checkin-user",
					"class" : "checkin-user",
					}))

class BookForm(ModelForm):

	def clean_isbn(self):
		isbn_val = self.cleaned_data["isbn"]
		if isbn_val:
			if not isbn.isValid(isbn_val):
				raise ValidationError("The isbn you entered is not valid")
		return isbn_val

	class Meta:
		model = Book

class AuthorForm(ModelForm):

	class Meta:
		model = Author

class GenreForm(ModelForm):

	class Meta:
		model = Genre

class CompleteUserCreationForm(UserCreationForm):


	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", )

class UserSelfChangeForm(UserChangeForm):


	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", )


class SettingsForm(ModelForm):

	class Meta:
		model = Library
