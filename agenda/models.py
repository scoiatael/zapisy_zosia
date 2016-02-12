from django.db import models
from django.utils import timezone

class Agenda(models.Model):
    pub_date = models.DateTimeField()
    content = models.TextField()

    class Meta:
        get_latest_by = 'pub_date'

    def __str__(self):
        return 'Agenda #{}'.format(self.id)
