from django.db import models
from django.utils import timezone


class ZosiaDefinition(models.Model):
    active_definition			= models.BooleanField()
    # dates
    registration_start			= models.DateTimeField()
    registration_final			= models.DateTimeField()

    registration_limit          = models.IntegerField(default=170)

    payment_deadline            = models.DateTimeField()
    lectures_suggesting_start	= models.DateTimeField()
    lectures_suggesting_final	= models.DateTimeField()
    rooming_start				= models.DateTimeField()
    rooming_final				= models.DateTimeField()
    zosia_start                 = models.DateTimeField()
    zosia_final                 = models.DateTimeField()
    bus_limit                   = models.IntegerField(default=98)
    bus16_limit                 = models.IntegerField(default=48)
    bus18_limit                 = models.IntegerField(default=48)
    # prices
    price_overnight             = models.IntegerField()
    price_overnight_breakfast   = models.IntegerField()
    price_overnight_dinner      = models.IntegerField()
    price_overnight_full        = models.IntegerField()
    price_transport             = models.IntegerField()
    price_organization          = models.IntegerField()
    # bank account
    account_number              = models.CharField(max_length=32)
    account_data_1              = models.CharField(max_length=40)
    account_data_2              = models.CharField(max_length=40)
    account_data_3              = models.CharField(max_length=40)
    # place
    city                        = models.CharField(max_length=20)
    city_c                      = models.CharField(max_length=20, verbose_name="miasto w celowniku")
    city_url                    = models.URLField()
    hotel                       = models.CharField(max_length=30)
    hotel_url                   = models.URLField()

    active                      = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ustawienie'
        verbose_name_plural = 'Ustawienia'

    def rooming_is_open(self):
        return timezone.now() <= self.rooming_final

    @property
    def bus_is_full(self):
        from users.models import UserPreferences
        if not hasattr(self, '_bus_is_full'):
            self._bus_is_full = UserPreferences.objects.filter(state=self, bus=True).count() >= self.bus_limit

        return self._bus_is_full
