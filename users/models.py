from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.utils.timezone import timedelta

from common.models import ZosiaDefinition

SHIRT_SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('XXXL', 'XXXL'),
)

SHIRT_TYPES_CHOICES = (
    ('m', _('klasyczna')),
    ('f', _('żeńska')),
)

BUS_HOUR_CHOICES = (
    ('','obojętne'),
    ('16:00', '16:00'),
    ('18:00', '18:00')
)

BUS_FIRST_SIZE = 0
BUS_SECOND_SIZE = 0


class OrganizationManager(models.Manager):
    def get_organization_choices(self):
        l = [ (org.id, org.name)
               for org in self.get_queryset().filter(accepted=True) ]
        l = l[:20]
        l.append(('new', 'inna'))
        return tuple(l)


class Organization(models.Model):
    name     = models.CharField(max_length=64, default='')
    accepted = models.BooleanField(default=False)

    objects = OrganizationManager()

    class Meta:
        verbose_name = 'Organizacja'
        verbose_name_plural = 'Organizacje'

    def __str__(self):
        return self.name


class ParticipantManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Participant(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now)
    committee = models.BooleanField(
        _('programme committee'),
        default=False)

    objects = ParticipantManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return ' '.join((self.first_name, self.last_name))

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def has_opened_records(self):
        preference = get_object_or_404(UserPreferences.objects.select_related('state'), user=self)
        user_opening_hour = preference.state.rooming_start - timedelta(minutes=preference.minutes_early)
        return user_opening_hour <= timezone.now() <= preference.state.rooming_final


class UserPreferences(models.Model):
    # This is the only required field
    user = models.OneToOneField(Participant)
    state = models.ForeignKey('common.ZosiaDefinition')
    org = models.ForeignKey(Organization)

    # opłaty
    day_1 = models.BooleanField()
    day_2 = models.BooleanField()
    day_3 = models.BooleanField()

    breakfast_2 = models.BooleanField()
    breakfast_3 = models.BooleanField()
    breakfast_4 = models.BooleanField()

    dinner_1 = models.BooleanField()
    dinner_2 = models.BooleanField()
    dinner_3 = models.BooleanField()

    # inne
    bus         = models.BooleanField(default=False)
    vegetarian  = models.BooleanField()
    paid        = models.BooleanField(default=False)

    shirt_size  = models.CharField(max_length=5, choices=SHIRT_SIZE_CHOICES)
    shirt_type  = models.CharField(max_length=1, choices=SHIRT_TYPES_CHOICES)

    want_bus = models.BooleanField(default=False)

    minutes_early = models.IntegerField(default=0)


    # used to differ from times on which buses leave
    bus_hour = models.CharField(max_length=10, choices=BUS_HOUR_CHOICES, blank=True, null=True, default='')


    photo_url = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(_('description'), max_length=2048, blank=True)

    class Meta:
        verbose_name_plural = 'Preferencje'

    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        from common.models import ZosiaDefinition
        # at this moment object probably is different from one in
        # database - lets check if 'paid' field is different
        try:
            old = UserPreferences.objects.get(id=self.id)
            definition = ZosiaDefinition.objects.get(active_definition=True)
            rooming_time = definition.rooming_start
            if self.paid and not old.paid:
                t = loader.get_template('payment_registered_email.txt')
                send_mail( 'Wpłata została zaksięgowana.',
                             t.render(Context({'rooming_time': rooming_time - timedelta(minutes=self.minutes_early)})),
                             None,
                             [ self.user.email ],
                             fail_silently=True )
        except Exception:
            # oh, we're saving for the first time - it's ok
            # move along, nothing to see here
            pass
        super(UserPreferences, self).save(*args, **kwargs)

    @property
    def get_room(self):
        from rooms.models import UserInRoom
        if not hasattr(self, 'user_room'):
            try:
                self.user_room = UserInRoom.objects.get(locator=self.user).room
            except:
                self.user_room = 0
        return self.user_room

    @staticmethod
    def get_free_seats():
        return (BUS_SECOND_SIZE+BUS_FIRST_SIZE - UserPreferences.objects.filter(bus=True).count()) > 0

    @staticmethod
    def get_first_time():
        return (BUS_FIRST_SIZE - UserPreferences.objects.filter(bus=True, bus_hour=BUS_HOUR_CHOICES[1][0]).count()) > 0

    @staticmethod
    def get_second_time():
        return (BUS_SECOND_SIZE - UserPreferences.objects.filter(bus=True, bus_hour=BUS_HOUR_CHOICES[2][0]).count()) > 0

    def bus16_available(self):
        return UserPreferences.objects.filter(bus_hour='16:00').exclude(user=self.user).count() < self.state.bus16_limit

    def bus18_available(self):
        return UserPreferences.objects.filter(bus_hour='18:00').exclude(user=self.user).count() < self.state.bus18_limit

    def count_payment(self):
        # returns how much money user is going to pay
        # hmm, we want to work for preferences, too

        definition = get_object_or_404(ZosiaDefinition, active_definition=True)

        payment = 0

        # payments: overnight stays + board
        if self.day_1 and self.dinner_1 and self.breakfast_2:
            payment += definition.price_overnight_full
        else:
            if self.day_1:
                if self.dinner_1:
                    payment += definition.price_overnight_dinner
                elif self.breakfast_2:
                    payment += definition.price_overnight_breakfast
                else:
                    payment += definition.price_overnight

        if self.day_2 and self.dinner_2 and self.breakfast_3:
            payment += definition.price_overnight_full
        else:
            if self.day_2:
                if self.dinner_2:
                    payment += definition.price_overnight_dinner
                elif self.breakfast_3:
                    payment += definition.price_overnight_breakfast
                else:
                    payment += definition.price_overnight

        if self.day_3 and self.dinner_3 and self.breakfast_4:
            payment += definition.price_overnight_full
        else:
            if self.day_3:
                if self.dinner_3:
                    payment += definition.price_overnight_dinner
                elif self.breakfast_4:
                    payment += definition.price_overnight_breakfast
                else:
                    payment += definition.price_overnight

        # payment: transport
        if self.bus:
            payment += definition.price_transport

        # payment: organization fee
        payment += definition.price_organization
        return payment

    def get_records_time(self):
        return self.state.rooming_start - timedelta(minutes=self.minutes_early)


class Waiting(models.Model):

    user = models.OneToOneField(Participant)
    state = models.ForeignKey('common.ZosiaDefinition')

    day_1 = models.BooleanField()
    day_2 = models.BooleanField()
    day_3 = models.BooleanField()
