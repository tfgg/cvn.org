from django.conf.urls.defaults import *
from settings import MEDIA_ROOT
from django.views.static import serve

import signup

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enablese admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', serve,
     {'document_root': MEDIA_ROOT,
      'show_indexes': True}),
    ('^', include('signup.urls')),
     
)
