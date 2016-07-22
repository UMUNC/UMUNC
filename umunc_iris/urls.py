from django.conf.urls import patterns, include, url
from view import *
from umunc import settings

if settings.UMUNC_IRIS_REGISTER:
    urlpatterns = patterns('',
        (r'^accounts/login/$', plogin),
        (r'^accounts/register/$', pregister),
        (r'^accounts/check/$', pcheck),
        (r'^accounts/logout/$', plogout),
        (r'^accounts/change/$', pchange),
        (r'^$', default),
        (r'^step1/$', step1),
        (r'^step2/$', step2),
        (r'^step3/$', step3),
        (r'^step4/$', step4),
        (r'^step5/$', step5),
        (r'^step6/$', step6),
        (r'^step7/$', step7),
        (r'^admin/sendmail/$', sendmail),
        (r'^admin/markpayment/$', markpayment),
        # (r'^.*/$', temp),
        # Examples:
        # url(r'^$', 'umunc.views.home', name='home'),
        # url(r'^umunc/', include('umunc.foo.urls')),

        # Uncomment the admin/doc line below to enable admin documentation:
        # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        #url(r'^admin/', include(admin.site.urls)),
    )
else:
    urlpatterns = patterns('',
        (r'^accounts/login/$', plogin),
        (r'^accounts/logout/$', plogout),
        (r'^accounts/change/$', pchange),
        (r'^admin/sendmail/$', sendmail),
        (r'^admin/markpayment/$', markpayment),
    )
