import os

from django.contrib import admin
from django.conf.urls import patterns, url, include
import blog.views
import lectures.views
import rooms.views
import common.views

from blog.feeds import *
import users.views

feeds = {
    'blog': LatestBlogEntries,
}

admin.autodiscover()



urlpatterns = patterns('',
    # Example:
    # (r'^zapisy_zosia/', include('zapisy_zosia.foo.urls')),

     (r'^$', blog.views.index),
     # url(r'^rooms/$', include('rooms.url', namespace='rooms')),

     (r'^blog/$', blog.views.index),

     # rss feed
     (r'^feeds/$', LatestBlogEntries()),

     # admin related
     # (r'^admin/register_payment/$', registration.views.register_payment),
     url(r'^admin/', include(admin.site.urls)),

     # registration related
     (r'^register/$', users.views.register),
     (r'^register/thanks/$', users.views.thanks),
     (r'^register/regulations/$', users.views.regulations),

     (r'^register/activate/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', users.views.activate_user),

     (r'^change_preferences/$', users.views.change_preferences),

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

     url(r'^password_reset/$',
         'django.contrib.auth.views.password_reset',
         { 'template_name':'password_reset_form.html' }, name='password_reset'),
     url(r'^password_reset/done/$',
         'django.contrib.auth.views.password_reset_done',
         { 'template_name':'password_reset_done.html' }, name='password_reset_done'),
     url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
         'django.contrib.auth.views.password_reset_confirm',
         { 'template_name':'password_reset_confirm.html' }, name='password_reset_confirm'),
     (r'^reset/done/$',
         'django.contrib.auth.views.password_reset_complete',
         { 'template_name':'password_reset_complete.html' }),
     (r'^static_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static_media')})
)
import settings

if settings.DEBUG:
    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#        }),
        (r'^static_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static_media')})
   )
