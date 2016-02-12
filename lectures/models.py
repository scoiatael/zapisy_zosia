from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class LectureManager(models.Manager):

    def create_lecture(self, new_data, user):
        data = new_data.cleaned_data
        lecture = self.model( author    = user,
                              title     = data['title'],
                              duration  = data['duration'],
                              abstract  = data['abstract'],
                              # sprezentujpl_email = data['sprezentujpl_email'], 
                              info      = data['info'],
                              date_time = timezone.now(),
                              accepted  = False
                            )
        lecture.save()
        return lecture


type_choices = ((0, 'Wykład'), (1, 'Warsztaty'))
person_type_choices = ((0, 'Sponsor'), (1, 'Gość'), (2, 'Normalny'))


class Lecture(models.Model):
    title     = models.CharField(max_length=256)
    duration  = models.PositiveIntegerField(choices=[(5,5), (15,15),(20,20),(25,25),(30,30), (100,'inne')])
    abstract  = models.TextField(max_length=768)
    info      = models.TextField(max_length=2048, blank=True)
    type        = models.IntegerField(choices=type_choices, verbose_name='Typ zajęć', default=0)
    person_type = models.IntegerField(choices=person_type_choices, verbose_name='Typ wykładowcy', default=2)


    description = models.TextField(max_length=2048, blank=True, verbose_name='Opis')
    author    = models.ForeignKey(settings.AUTH_USER_MODEL)
    author_show = models.CharField(max_length=256, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    for_committe = models.BooleanField(default=True, verbose_name='Dla komitetu programowego')
    accepted  = models.BooleanField(default=False)

    order = models.IntegerField(default=99)

    objects = LectureManager()

    class Meta:
        verbose_name = 'Wykład'
        verbose_name_plural = 'Wykłady'
        ordering = ['order', 'id']

    def __str__(self):
        return "{} - {}".format(self.author, self.title)
