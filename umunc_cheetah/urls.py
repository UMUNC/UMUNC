from django.conf.urls import patterns, include, url
from view import *

# from umunc.part_upload import upload

urlpatterns = patterns('',
    (r'^$', default),
    (r'^datacontrol/heartbeat/$', datacontrol_heartbeat),
    (r'^datacontrol/communication/$', datacontrol_communication),
    (r'^datacontrol/meeting/$', datacontrol_meeting),
    (r'^datacontrol/file/$', datacontrol_file),
    (r'^datacontrol/setting/$', datacontrol_setting),
    (r'^history/communication/(\d+)/$', history_communication),
    (r'^history/meeting/$', history_meeting),
    # (r'^upload$', upload),
    # (r'^accounts/login/$', plogin),
    # (r'^accounts/register/$', pregister),
    # (r'^accounts/check/$', pcheck),
    # (r'^accounts/logout/$', plogout),
    # (r'^accounts/change/$', pchange),
    # (r'^$', default),
    # (r'^step1/$', step1),
    # (r'^step2/$', step2),
    # (r'^step3/$', step3),
    # Examples:
    # url(r'^$', 'umunc.views.home', name='home'),
    # url(r'^umunc/', include('umunc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)