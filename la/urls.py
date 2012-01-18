from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('la.views',

		# The main views, for displayin books, authors, 
		# for the front

		url(r'^$', 'home', name='home'),
		url(r'^book/(?P<book_id>\d+)/?$','book', name='book'),
		url(r'^catalogue/$', 'catalogue'),
		url(r'^catalogue/(?P<page_no>\d+)/?$', 'catalogue', name='catalogue'),
		url(r'^genre/(?P<genre_id>\d+)/?$', 'catalogue'),
		url(r'^genre/(?P<genre_id>\d+)/(?P<page_no>\d+)/?$', 'catalogue', name='genre'),
		url(r'^author/(?P<author_id>\d+)/?$', 'catalogue'),
		url(r'^author/(?P<author_id>\d+)/(?P<page_no>\d+)/?$', 'catalogue', name='author'),
		url(r'^authors/?$', 'authors'),
		url(r'^authors/(?P<page_no>\d+)?$', 'authors', name='authors'),
		url(r'^search/?$', 'catalogue'),
		url(r'^search(/(?P<page_no>\d+)?)?$', 'catalogue', name='search'),
		url(r'^news/(?P<news_id>\d+)/?$', 'news_item'),

		# The user parts follow here
		url(r'^login/?$', 'login_view', name='login'),
		url(r'^logout/?$', 'logout_view', name='logout'),
		url(r'^my-checkouts/?$', 'user_checkouts', name='user_checkouts'),
		url(r'^register/?$', 'register', name='register'),
		url(r'^my-profile/?$', 'user_profile', name='user_profile'),
		# Finally, admin stuff
		url(r'^admins/?$', 'admin', name='admin'),
		url(r'^admins/checkout/?$', 'checkout', name='checkout'),
		url(r'^admins/checkin/?$', 'checkin', name='checkin'),
		url(r'^admins/user/edit/(?P<user_id>\d+)/?$', 'edit_user'),
		url(r'^admins/user/edit/?$', 'edit_user', name='edit_user'),
		url(r'^admins/user/create/?$', 'create_user', name='create_user'),
		#CRUD crap
		url(r'^admins/book/add/?$', 'add_book', name='add_book'),
		url(r'^admins/book/edit/(?P<book_id>\d+)/?$', 'edit_book', name='edit_book'),

		# API stuff (feels good sayin that)
		url(r'^admins/autocomplete/?$', 'autocomplete'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
