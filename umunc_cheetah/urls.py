from django.conf.urls import patterns, include, url
from view import *

from umunc import settings

if settings.UMUNC_CHEETAH_ENABLE:
    urlpatterns = patterns('',
        (r'^$', default),
        (r'^datacontrol/heartbeat/$', datacontrol_heartbeat),
        (r'^datacontrol/communication/$', datacontrol_communication),
        (r'^datacontrol/meeting/$', datacontrol_meeting),
        (r'^datacontrol/file/$', datacontrol_file),
        (r'^datacontrol/setting/$', datacontrol_setting),
        (r'^history/communication/(\d+)/$', history_communication),
        (r'^history/meeting/$', history_meeting),
    )
else:
    urlpatterns = patterns('',
    )
