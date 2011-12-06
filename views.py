from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from la.models import Book, Library

def home(request):
	return HttpResponse('You are looking at the homepage of something awesome')

def book(request, book_id):
	b = Book.objects.get(pk = book_id)
	return render_to_response('lib_admin/book.html', { 'book' : b})
