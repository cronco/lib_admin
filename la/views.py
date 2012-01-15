from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.core import serializers
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator
from django.utils.safestring import SafeString
from django.forms.models import modelformset_factory, formset_factory
from la.models import *
from la.helpers import buildGenreTree
from la import isbn
from la.forms import *
import datetime

l = Library.objects.get()
latest = Book.objects.all().order_by('-add_date')[:5]
genres = buildGenreTree()
dictionary ={'library' : l, 'latest' : latest, 'genres' : genres, 'base_url' : settings.BASE_URL }

def home(request):

	news = News.objects.all().order_by('-pub_date')[:5]
	c = RequestContext(request, dictionary)
	c['news'] = news
	return render_to_response('lib_admin/home.html',{}, c)

def book(request, book_id):

	b = Book.objects.get(pk = book_id)
	c = RequestContext(request, dictionary)
	others = []
	for author in b.authors.all():

		others +=Book.objects.filter(authors = author).exclude(id = b.id)
		c['others_by_author'] = others

	c['book'] = b
	return render_to_response('lib_admin/book.html', {}, c)

def news_item(request, news_id):

	n = News.objects.get(pk = news_id)
	c = RequestContext(request, dictionary)
	c['news'] = n
	return render_to_response('lib_admin/book.html', {}, c)

def authors(request, page_no = 1):
	a = Author.objects.all().order_by('last_name')
	c = RequestContext(request, dictionary)
	
	paginator = Paginator(a, 1)
	a = paginator.page(page_no)
	c['authors'], c['context'] = a, 'authors'
	return render_to_response('lib_admin/authors.html', {}, c)

def catalogue(request, author_id = 0, genre_id = 0, page_no = 1):

	c = RequestContext(request, dictionary)
	b = None

	if not author_id and not genre_id:

		if 'search' in request.GET:

			p = request.GET['search']
			c['context'] = 'search'
			c['search'] = p

			if isbn.looks_like_isbn(p):

				c['looks_like_isbn'] = True
				if isbn.isValid(p):

					c['isbn'] = True
					try:

						b = Book.objects.get(isbn = p)
						return redirect(b)

					except Book.DoesNotExist:
						pass

			else:
				b = Book.objects.filter(
					Q(name__icontains = p) | 
					Q(authors__last_name__icontains = p) |
					Q(authors__first_name__icontains = p)
					)

		else:
			b = Book.objects.all()
			c['context'] = 'catalogue'

	elif author_id:

		a = Author.objects.get(id = author_id)
		c['author'] = a
		c['context'] = 'author/%s' % author_id
		b = Book.objects.filter(authors = author_id)

	elif genre_id:

		g = Genre.objects.get(id = genre_id)
		c['genre'] = g
		c['context'] = 'genre/%s' % genre_id
		b = Book.objects.filter(genres = genre_id)

	try:
		paginator = Paginator(b, 1)
		b = paginator.page(page_no)
	except TypeError:
		pass
	c['books'] = b
	return render_to_response('lib_admin/catalogue.html',{}, c)

def login_view(request):
	"""
	Displays a login form and logs user in if form data
	is sent through POST
	"""
	c = RequestContext(request, dictionary)
	if request.method == "POST":
		form = AuthenticationForm(data = request.POST)
		if form.is_valid():

			login(request, form.get_user())

			if request.session.test_cookie_worked():
				request.session.delete_test_cookie()

			return redirect('home')
	else:
		form = AuthenticationForm(request)
		request.session.set_test_cookie()
	c['form'] = form
	return render_to_response('lib_admin/login.html', {}, c)

@login_required
def logout_view(request):
	logout(request)
	return redirect('home')


def register(request):
	c = RequestContext(request, dictionary)
	if request.method == "POST":
		form = CompleteUserCreationForm(data = request.POST)
		if form.is_valid():
			u = form.save()
			p = Permission.objects.get(codename = 'checkout_book')
			u.user_permissions.add(p)
			u.save()
			p.save()
			redirect('edit_user', user_id = u.id)
	else:
		form = CompleteUserCreationForm()
	c['form'] = form
	return render_to_response('forms/general.html', {}, c)

@user_passes_test(lambda u: u.is_staff)
def create_user(request):
	c = RequestContext(request, dictionary)
	if request.method == "POST":
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			u = form.save()
			p = Permission.objects.get(codename = 'checkout_book')
			u.user_permissions.add(p)
			u.save()
			p.save()
			redirect('edit_user', user_id = u.id)
	else:
		form = UserCreationForm()
	c['form'] = form
	return render_to_response('forms/general.html', {}, c)

@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id = 0):
	c = RequestContext(request, dictionary)
	u = User.objects.get(pk = user_id)
	if request.method == "POST":
		form = UserChangeForm(data = request.POST, instance = u)
		if form.is_valid():
			u = form.save()
	else:
		form = UserChangeForm(instance = u)
	c['form'] = form
	return render_to_response('forms/general.html', {}, c)

@login_required
def user_checkouts(request, user = None):
	c = RequestContext(request, dictionary)
	checkouts = Checkout.objects.filter(Q(user = user or request.user.id)).order_by('checkout_date')
	if 'show' in request.GET and request.GET['show'] == 'outstanding':
		checkouts = checkouts.filter(Q(return_date = None))
	c['checkouts'] = checkouts
	return render_to_response('lib_admin/checkouts.html', {}, c)

@user_passes_test(lambda u: u.is_staff)
def admin(request):
	c = RequestContext(request, dictionary)
	return render_to_response('lib_admin/admin.html', {}, c)

@user_passes_test(lambda u: u.is_staff)
def checkout(request):
	c = RequestContext(request, dictionary)
	CheckoutFormSet = formset_factory(CheckoutForm)
	if request.method == "POST":
		formset = CheckoutFormSet(data = request.POST)
		if formset.is_valid():
			for form in formset:
				form.save()
		c['valid'] = formset.is_valid()
	else:
		formset = CheckoutFormSet()
	extraBooksFormset = formset_factory(ExtraBookCheckoutForm)
	c['form'] = CheckoutFormSet
	c['extraBooksFormset'] = extraBooksFormset
	c['context'] = 'checkout'
	return render_to_response('lib_admin/checkout.html', {}, c)

@user_passes_test(lambda u: u.is_staff)
def checkin(request):
	c = RequestContext(request, dictionary)
	CheckinFormSet = modelformset_factory(Checkout, CheckinForm)
	if request.method == "POST":
		data = request.POST.copy()
		for i in range(0, int(data['form-TOTAL_FORMS'])):
			if 'form-' + str(i) + '-return_date' in data:
				data['form-' + str(i) + '-return_date'] = datetime.date.today().isoformat()
			else:
				data['form-' + str(i) + '-return_date'] = ''

		formset = CheckinFormSet(data = data)
		user_form = AutoUserForm(data = data)
		if formset.is_valid():
			c['cool'] = 'cool'
			formset.save()
		else:
			c['err'] = formset.errors
			c['data'] = data
	else:
		CheckinFormSet = modelformset_factory(Checkout, CheckinForm)
		user_form = AutoUserForm()
	c['user_form'] = user_form
	c['form'] = CheckinFormSet
	c['context'] = 'checkin'
	return render_to_response('lib_admin/checkin.html', {}, c)

@user_passes_test(lambda u: u.is_staff)
def add_book(request):
	c = RequestContext(request, dictionary)
	if request.method == "POST":
		form  = BookForm(data = request.POST)
		if form.is_valid():
			form.save()
	else:
		form = BookForm()
	c['form'] = form

	return render_to_response('forms/general.html', {}, c)

@user_passes_test(lambda u: u.is_staff)
def edit_book(request, book_id = 0):
	c = RequestContext(request, dictionary)
	if book_id:
		b = Book.objects.get(pk = book_id)
		if request.method == "POST":
			form  = BookForm(data = request.POST, instance = b)
			if form.is_valid():
				form.save()
		else:
			form = BookForm(instance = b)
		c['form'] = form

	return render_to_response('forms/general.html', {}, c)

def autocomplete(request):
	
	if 'book' in request.GET:
		count = Checkout.objects.filter(
				Q(book__name__istartswith = request.GET['book']) |
				Q(book__isbn__startswith = request.GET['book']),
				Q(return_date__isnull = True)
					).count()
		b = Book.objects.filter(
						Q(name__istartswith=request.GET['book']) |
						Q(isbn__startswith = request.GET['book']) 
					).exclude(copies__lte = count
					).order_by('name').distinct()
		#Exclude books which are already lent to the user.
		if 'user_id' and 'checkout-book' in request.GET:
			b = b.exclude(
					Q(checkout__user = request.GET['user_id']),
					Q(checkout__return_date__isnull=True)
					)
		return HttpResponse(serializers.serialize('json', b))

	#if we're autocompleteing for users
	if 'user' in request.GET:

		u = User.objects.filter(
					Q(last_name__istartswith=request.GET['user']) |
					Q(first_name__istartswith=request.GET['user']) |
					Q(email__istartswith=request.GET['user']) 
				).order_by('last_name')

		# If we're searching for users who are able to checkout books,
		# exclude those who don't have the necessary permission
		if 'checkout-user' in request.GET:
			u = u.filter( Q(user_permissions__codename = 'checkout_book'))
		return HttpResponse(serializers.serialize('json', u))

	if 'checkouts' in request.GET:
		x = modelformset_factory(Checkout, CheckinForm)
		query = Checkout.objects.filter(
						Q(return_date__isnull = True),
						Q(user = request.GET['user_id'])
				).order_by('checkout_date')
		c = RequestContext(request, dictionary)
		forms = x(queryset = query)
		c.update({'checkouts' : zip(query, forms), 'formset':
			forms.management_form})
		return render_to_response('forms/checkin.html', {}, c)

