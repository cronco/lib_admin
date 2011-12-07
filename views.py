from django.http import HttpResponse, Http404
from django.db.models import Q
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, redirect
from django.utils.safestring import SafeString
from la.models import *
from la.helpers import buildGenreTree
from la import isbn
import datetime

l = Library.objects.get()
latest = Book.objects.all().order_by('-add_date')[:5]
genres = buildGenreTree()
dictionary ={'library' : l, 'latest' : latest, 'genres' : genres }

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

def newsItem(request, news_id):

	n = News.objects.get(pk = news_id)
	c = RequestContext(request, dictionary)
	c['news'] = n
	return render_to_response('lib_admin/book.html', {}, c)

def catalogue(request, author_id = 0, genre_id = 0):

	c = RequestContext(request, dictionary)
	b = False

	if not author_id and not genre_id and request.method != 'POST':

		b = Book.objects.all()[:10]

	elif author_id:

		a = Author.objects.get(id = author_id)
		c['author'] = a
		b = Book.objects.filter(authors = author_id)[:10]

	elif genre_id:

		g = Genre.objects.get(id = genre_id)
		c['genre'] = g
		b = Book.objects.filter(genres = genre_id)[:10]

	elif request.method == 'POST':

		p = request.POST.get('search_string', '')
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
	
	c['books'] = b
	return render_to_response('lib_admin/catalogue.html',{}, c)
