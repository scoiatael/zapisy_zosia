from django.db import models
from django.conf import settings
from lectures.models import Lecture


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    lecture = models.ForeignKey(Lecture)
    value = models.IntegerField(choices=[(x, x) for x in range(11)], default=0, verbose_name='ocena')
    text = models.TextField(null=True, blank=True, verbose_name='Uwagi')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ocena wykładu'
        verbose_name_plural = 'Oceny wykładów'

    def __str__(self):
        return "{}: {} {}".format(self.lecture, self.user, self.value)
