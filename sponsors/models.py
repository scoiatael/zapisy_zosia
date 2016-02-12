from django.db import models


class Sponsor(models.Model):
    name = models.CharField(verbose_name='name', max_length=255, unique=True)
    url  = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='img')
    order = models.IntegerField(default=100)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'sponsor'
        verbose_name_plural = 'sponsorzy'

    def __str__(self):
        return self.name
