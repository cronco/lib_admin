from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
	name = models.CharField(max_length = 100)
	bio = models.TextField(blank = True)

	def __unicode__(self):
		return self.name

class Genre(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 250, null=True)
	parent_genre = models.ForeignKey('self', null = True)

	def __unicode__(self):
		return self.name

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
	cover = models.ImageField('book cover',upload_to = 'covers/', null=True)
	preview = models.FileField('book preview', upload_to = 'previews/', null=True)
	synopsis = models.TextField('book synopsis, description', null=True)
	genres = models.ManyToManyField(Genre, null=True)
	publisher = models.ForeignKey(Publisher) 
	authors = models.ManyToManyField(Author)

	def __unicode__(self):
		return self.name

class Checkout(models.Model):
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	checkout_date = models.DateTimeField(auto_now_add = True)
	return_date = models.DateTimeField(null = True)

	def __unicode__(self):
		return self.user + ' ' + self.book

class Library(models.Model):
	name = models.CharField('Library name', max_length = 100)
	#maximum number of days a person can lend a book
	max_lend_period = models.IntegerField('Maximum lending period') 

class News(models.Model):
	title = models.CharField('News Title', max_length = 200)
	content = models.TextField('News content')
	pub_date = models.DateField(help_text = 'Publishing date', auto_now_add = True)
	last_edit_date = models.DateField(help_text = 'Last edit date', auto_now = True)
