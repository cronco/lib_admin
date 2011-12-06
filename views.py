from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from la.models import Book, Library, News
import datetime

l = Library.objects.get()
c = Context({"library" : l})

def home(request):
	news = News.objects.all().order_by('-pub_date')[:5]
	c['news'] = news
	return render_to_response('lib_admin/home.html', c)

def book(request, book_id):
	b = Book.objects.get(pk = book_id)
	c['book'] = b
	return render_to_response('lib_admin/book.html', c)
