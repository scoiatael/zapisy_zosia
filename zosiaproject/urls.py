"""zosiaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

import blog.views
from blog.feeds import *
import lectures.views
import users.views

feeds = {
    'blog': LatestBlogEntries,
}

urlpatterns = [
    url(r'^$', blog.views.index),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^rooms/', include('rooms.urls', namespace='rooms')),

    # rss feed
    url(r'^feeds/$', LatestBlogEntries()),

    # admin related
    url(r'^admin/register_payment/$', users.views.register_payment),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^committee/', include('committee.urls', namespace='committee')),

    # authentication related
    url('^', include('common.urls')),

    # registration related
    url(r'^register/$', users.views.register),
    url(r'^waiting/$', users.views.waiting_list),
    url(r'^register/thanks/$', users.views.thanks),
    url(r'^register/regulations/$', users.views.regulations),

    url(r'^register/activate/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', users.views.activate_user),

    url(r'^change_preferences/$', users.views.change_preferences),

    # apps main urls
    url(r'^lectures/$', lectures.views.index),
    url(r'^agenda/$', include('agenda.urls', namespace='agenda')),
]
