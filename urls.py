import os

from django.conf.urls import patterns, url, include
from django.contrib import admin
import registration.views
import blog.views
import lectures.views
import newrooms.views
import common.views

from blog.feeds import *

feeds = {
    'blog': LatestBlogEntries,
}

admin.autodiscover()



urlpatterns = patterns('',
    # Example:
    # (r'^zapisy_zosia/', include('zapisy_zosia.foo.urls')),

     (r'^$', blog.views.index),

     (r'^rooms/$', newrooms.views.index),
     (r'^rooms/list.json$', newrooms.views.json_rooms_list),

     # (r'^rooms/fill/$', newrooms.views.fill_rooms),
     # (r'^rooms/modify/$', newrooms.views.modify_room),
     # (r'^rooms/open/$', newrooms.views.open_room),
     # (r'^rooms/close/$', newrooms.views.close_room),
     # (r'^rooms/trytogetin/$', newrooms.views.trytogetin_room),
     # (r'^leave_room/$', newrooms.views.leave_room),

     (r'^blog/$', blog.views.index),

     # rss feed
     (r'^feeds/$', LatestBlogEntries()),

     # admin related
     (r'^admin/register_payment/$', registration.views.register_payment),
     # TODO(Karol): we disable separate transportation payment for this edition.
     # (r'^admin/register_bus_payment/$', registration.views.register_bus_payment),
     url(r'^admin/', include(admin.site.urls)),

     # registration related
     (r'^register/$', registration.views.register),
     (r'^register/thanks/$', registration.views.thanks),
     (r'^register/regulations/$', registration.views.regulations),

     # (r'^register/add_org/$', registration.views.add_organization),
     (r'^register/activate/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', registration.views.activate_user),

     (r'^change_preferences/$', registration.views.change_preferences),

     # login / logout
     (r'^login/$', common.views.login_view),
     (r'^accounts/login/', common.views.login_view),
     (r'^logout/$', common.views.logout_view),
     (r'^logout/bye/$', common.views.thanks),

     # apps main urls
     (r'^lectures/$', lectures.views.index),
     (r'^program/$', lectures.views.program),

     # static media
     # note, that this should be disabled for production code
	 # (may be disabled outside of django, though)

     # urls required for password change/reset
     (r'^password_change/$', common.views.password_change),
     (r'^password_change/done/$', common.views.password_change_done),

     (r'^password_reset/$', 
         'django.contrib.auth.views.password_reset',
         { 'template_name':'password_reset_form.html' }),
     (r'^password_reset/done/$', 
         'django.contrib.auth.views.password_reset_done',
         { 'template_name':'password_reset_done.html' }),
     (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
         'django.contrib.auth.views.password_reset_confirm',
         { 'template_name':'password_reset_confirm.html' }),
     (r'^reset/done/$',
         'django.contrib.auth.views.password_reset_complete',
         { 'template_name':'password_reset_complete.html' }),
)
import settings

if settings.DEBUG:
    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#        }),
        (r'^static_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static_media')})
   )
