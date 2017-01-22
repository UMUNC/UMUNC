from django.conf.urls import patterns, include, url
from django.contrib import admin
from umunc_mpc.views import *

from umunc import settings

if settings.UMUNC_MPC_ENABLE:
    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'LBlogger.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^$', view_list),
        url(r'^list/(.*)/$', view_list),
        url(r'^post/(\d+)/$', view_post_gloable),
        url(r'^post/(.*)/(\d+)/$', view_post),
        url(r'^dashboard/$', dashboard),
        url(r'^dashboard/edit/(\d)+/$', dashboard_edit),
    )
else:
    urlpatterns = patterns('',
    )
