# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^$', 'polls.views.main', name='main'),
                       url(r'^thanks', 'polls.views.thanks', name='thanks'),
                       url(r'^vote$', 'polls.views.vote', name='vote')
                       )