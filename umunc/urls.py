from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from part_upload import upload
import umunc_iris.urls
import umunc_cheetah.urls

urlpatterns = patterns('',
    (r'^iris/', include(umunc_iris.urls)),
    (r'^cheetah/', include(umunc_cheetah.urls)),
    (r'^$', umunc_iris.view.test),
    (r'^upload$', upload),
    
    # Examples:
    # url(r'^$', 'umunc.views.home', name='home'),
    # url(r'^umunc/', include('umunc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
