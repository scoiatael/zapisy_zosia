# -*- coding: UTF-8 -*-
import datetime
from django.db import models
from django.conf import settings
from lectures.models import Lecture


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    lecture = models.ForeignKey(Lecture)
    value = models.IntegerField(choices=[(x, x) for x in range(11)], default=0, verbose_name=u'ocena')
    text = models.TextField(null=True, blank=True, verbose_name=u'Uwagi')
    created = models.DateTimeField(auto_now_add=True, auto_now=True)
    edited = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'Ocena wykładu'
        verbose_name_plural = u'Oceny wykładów'

    def __unicode__(self):
        return u"%s: %s (%s)" % (self.lecture, self.user, self.value)