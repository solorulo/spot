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
    # url(r'^spot/', include('spot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('spot_app.views',
    url(r'^$', 'profile', name='profile'),
    url(r'^verify_user$', 'verify_user', name='verify_user'),
    url(r'^register_image$', 'register_image', name='register_image'),
    url(r'^signup$', 'register', name='register'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    
    # url(r'^prueba/$', 'madre_prueba', name='prueba'),
)

urlpatterns += patterns('spot_app.home_views',
    url(r'^home/global$', 'home_global', name='home_global'),
    url(r'^home/top$', 'home_top', name='home_top'),
    url(r'^home/nearby$', 'home_nearby', name='home_nearby'),
)

urlpatterns += patterns('spot_app.photo_views',
    url(r'^photo/add$', 'photo_add', name='photo_add'),
    
    # url(r'^prueba/$', 'madre_prueba', name='prueba'),
)
