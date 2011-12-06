from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('lib_admin.views',
     url(r'^$', 'home', name='home'),
	 url(r'^book/(?P<book_id>\d+)$','book', name='book'),
	 url(r'^catalogue$', 'catalogue'),
	 url(r'^genre/(?P<genre_id>\d+)$', 'catalogue', name='genre_catalogue'),
	 url(r'^author/(?P<author_id>\d+)$', 'catalogue', name='author_catalogue'),
	 url(r'^search$', 'catalogue', name='search'),
	 url(r'^news$', 'news'),
	 url(r'^news/(?P<news_id>\d+)$', 'newsItem')
	 
    # url(r'^lib_admin/', include('lib_admin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
  #   url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
