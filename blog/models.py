# -*- coding: UTF-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime


class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    pub_date = models.DateTimeField(editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField(max_length=2048)

    class Meta:
        verbose_name = 'Wpis na blogu'
        verbose_name_plural = 'Wpisy na blogu'

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        super(BlogPost, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return "/blog/"
