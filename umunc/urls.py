from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from part_upload import upload_page
import umunc_iris.urls
import umunc_cheetah.urls
import umunc_mpc.urls
import view

urlpatterns = patterns('',
    (r'^iris/', include(umunc_iris.urls)),
    (r'^cheetah/', include(umunc_cheetah.urls)),
    (r'^mpc/', include(umunc_mpc.urls)),
    (r'^default$', view.default),
    (r'^upload$', upload_page),
    
    # Examples:
    # url(r'^$', 'umunc.views.home', name='home'),
    # url(r'^umunc/', include('umunc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
