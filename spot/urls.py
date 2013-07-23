from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from spot import settings

handler404 = "spot_app.views.handler404"
handler500 = "spot_app.views.handler500"

urlpatterns = patterns('',
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    url(r'^$', 'spot_app.views.home', name='home'),
    url(r'^register/$', 'spot_app.views.register', name='register'),
    url(r'^login/$', 'spot_app.views.login', name='login'),
    url(r'^logout/$', 'spot_app.views.logout', name='logout'),
    
    url(r'^prueba/$', 'spot_app.views.madre_prueba', name='prueba'),
    # url(r'^spot/', include('spot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
