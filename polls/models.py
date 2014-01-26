# -*- coding: UTF-8 -*-
import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from common.models import ZosiaDefinition
from users.models import UserPreferences


class PollManager(models.Manager):

    def open_for_user(self, user):
        polls = self.get_queryset()
        definition = get_object_or_404(ZosiaDefinition, active_definition=True)
        preferences = get_object_or_404(UserPreferences, user=user, state=definition)
        result = []
        now = datetime.datetime.now()
        for poll in polls:
            if not poll.visible:
                continue
            if poll.time_start and poll.time_start > now:
                continue
            if poll.time_end and poll.time_end < now:
                continue
            if poll.only_bus and not preferences.bus:
                continue

            result.append(poll)

        return result


class Poll(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'tytuł')
    description = models.TextField(verbose_name=u'opis', null=True, blank=True)

    created = models.TimeField(auto_now_add=True)
    edited = models.TimeField(auto_now=True)

    time_start = models.DateTimeField(null=True, blank=True, verbose_name=u'Początek')
    time_end = models.DateTimeField(null=True, blank=True, verbose_name=u'Koniec')
    only_bus = models.BooleanField(default=False, verbose_name=u'Tylko dla jadących autokarem')

    visible = models.BooleanField(default=False, verbose_name=u'Widoczna')

    objects = models.Manager()
    filtered = PollManager()

    class Meta:
        verbose_name = u'Ankieta'
        verbose_name_plural = u'Ankiety'

    def __unicode__(self):
        return u"%s" % (self.title,)


class Question(models.Model):
    poll = models.ForeignKey('Poll', verbose_name=u'Ankieta')
    question = models.CharField(max_length=255, verbose_name=u'Pytanie')
    order = models.IntegerField(default=100)

    class Meta:
        verbose_name = u'Pytanie'
        verbose_name_plural = u'Pytanie'
        ordering = ['order', 'id']

    def __unicode__(self):
        return u"%s" % (self.question,)


class UserAnswer(models.Model):
    question = models.ForeignKey('Question', verbose_name=u'pytanie')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    created = models.TimeField(auto_now_add=True)
    edited = models.TimeField(auto_now=True)

    class Meta:
        verbose_name = u'Odpowiedź'
        verbose_name_plural = u'Odpowiedzi'