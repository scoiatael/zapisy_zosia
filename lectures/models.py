# -*- coding: UTF-8 -*-
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class LectureManager(models.Manager):

    def create_lecture(self, new_data, user):
        data = new_data.cleaned_data
        lecture = self.model( author    = user,
                              title     = data['title'],
                              duration  = data['duration'],
                              abstract  = data['abstract'],
                              # sprezentujpl_email = data['sprezentujpl_email'], 
                              info      = data['info'],
                              date_time = datetime.now(),
                              accepted  = False
                            )
        lecture.save()
        return lecture


type_choices = ((0, u'Wykład'), (1, u'Warsztaty'))
person_type_choices = ((0, u'Sponsor'), (1, u'Gość'), (2, u'Normalny'))

class Lecture(models.Model):
    title     = models.CharField(max_length=256)
    duration  = models.PositiveIntegerField(max_length=3)
    abstract  = models.TextField(max_length=512)
    info      = models.TextField(max_length=2048, blank=True)
    #dodatkowe info dla organizatorów
#
    type        = models.IntegerField(choices=type_choices, verbose_name=u'Typ zajęć', default=0)
    person_type = models.IntegerField(choices=person_type_choices, verbose_name=u'Typ wykładowcy', default=2)

    photo_url = models.CharField(max_length=250, null=True, blank=True)

    description = models.TextField(max_length=2048, blank=True, verbose_name=u'Opis')
    author    = models.ForeignKey(settings.AUTH_USER_MODEL)
    author_show = models.CharField(max_length=256, null=True, blank=True)
    date_time = models.DateTimeField()
    accepted  = models.BooleanField()

    order = models.IntegerField(default=99)
    #sprezentujpl_email = models.EmailField()

    objects = LectureManager()

    def __unicode__(self):
        return u"%s - %s" % (self.author, self.title)
        
