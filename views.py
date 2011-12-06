from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.safestring import SafeString
from la.models import Book, Library, News
import datetime

l = Library.objects.get()
latest = Book.objects.all().order_by('-add_date')[:5]
c = Context({'library' : l, 'latest' : latest})

def home(request):
	news = News.objects.all().order_by('-pub_date')[:5]
	c['news'] = news
	return render_to_response('lib_admin/home.html', c)

def book(request, book_id):
	b = Book.objects.get(pk = book_id)
	if b.authors.count() == 1:
		others = Book.objects.filter(authors = b.authors.get()).exclude(id = b.id)
		c['others_by_author'] = others
	c['book'] = b
	return render_to_response('lib_admin/book.html', c)

def newsItem(request, news_id):
	n = News.objects.get(pk = news_id)
	c['news'] = n
	return render_to_response('lib_admin/book.html', c)

def catalogue(request, author_id = 0, genre_id = 0):
	b = Book.objects.all()[10:]
	c['books'] = b
	return render_to_response('lib_admin/catalogue.html', c)
