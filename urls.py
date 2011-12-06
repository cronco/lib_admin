from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'lib_admin.views.home', name='home'),
	 url(r'^book/(?P<book_id>\d+)$','lib_admin.views.book', name='book'),
	 url(r'^search$', 'lib_admin.views.search'),
	 url(r'^catalogue$', 'lib_admin.views.catalogue'),
	 url(r'^news$', 'lib_admin.views.news'),
	 url(r'^news/(?P<news_id>\d+)$', 'lib_admin.views.newsItem')
	 
    # url(r'^lib_admin/', include('lib_admin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
  #   url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
