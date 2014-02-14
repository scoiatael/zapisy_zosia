# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url, include

urlpatterns = patterns('committee.views',
                       url(r'^$', 'lectures', name='main'),
                       url(r'^vote', 'vote', name='vote'),
                       )