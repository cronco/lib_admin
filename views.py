from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.utils.safestring import SafeString
from la.models import Book, Library, News
from la.helpers import buildGenreTree
import datetime

l = Library.objects.get()
latest = Book.objects.all().order_by('-add_date')[:5]
genres = buildGenreTree()
dictionary ={'library' : l, 'latest' : latest, 'genres' : genres} 

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

	if not author_id and not genre_id:
		b = Book.objects.all()[10:]
	elif author_id:
		b = Book.objects.filter(authors = author_id)[10:]
	
	c['books'] = b
	return render_to_response('lib_admin/catalogue.html',{}, c)
