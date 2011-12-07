from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import isbn

class Author(models.Model):
	first_name = models.CharField('author\'s first name', max_length = 100)
	last_name = models.CharField('author\'s last name', max_length = 100)
	bio = models.TextField(blank = True)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def name(self):
		return self.first_name + ' ' + self.last_name

	@models.permalink
	def get_absolute_url(self):
		return('author_catalogue', [str(self.id)])

class Genre(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 250, blank=True)
	parent_genre = models.ForeignKey('self', null = True, default = 0)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return('genre_catalogue', [str(self.id)])

class Publisher (models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Book(models.Model):
	isbn = models.CharField('ISBN code', max_length = 20)
	name = models.CharField('book title', max_length = 200)
	pub_date = models.DateField('publishing date', null=True)
	add_date = models.DateField('added to library date', auto_now_add = True)
	copies = models.IntegerField('number of available copies')
	cover = models.ImageField('book cover',upload_to = 'covers/', null=True, blank=True)
	preview = models.FileField('book preview', upload_to = 'previews/', null=True, blank=True)
	synopsis = models.TextField('book synopsis, description', blank=True)
	genres = models.ManyToManyField(Genre, null=True)
	publisher = models.ForeignKey(Publisher) 
	authors = models.ManyToManyField(Author)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('book', [str(self.id)])
	
	def get_amazon_link(self):
		return isbn.url("amazon",self.isbn)

	def available(self):
		return self.copies > Checkout.objects.filter(book = self.id, return_date = None).count()

class Checkout(models.Model):
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	checkout_date = models.DateTimeField(auto_now_add = True)
	return_date = models.DateTimeField(null = True, blank=True)

	def __unicode__(self):
		return self.user.username + ' ' + self.book.name

class Library(models.Model):
	name = models.CharField('library name', max_length = 100)
	#maximum number of days a person can lend a book
	max_lend_period = models.IntegerField('maximum lending period') 
	opening_hour = models.TimeField('opening hour')
	closing_hour = models.TimeField('closing hour')
	description = models.TextField(blank = True)

class News(models.Model):
	title = models.CharField('News Title', max_length = 200)
	content = models.TextField('News content')
	pub_date = models.DateField(help_text = 'Publishing date', auto_now_add = True)
	last_edit_date = models.DateField(help_text = 'Last edit date', auto_now = True)