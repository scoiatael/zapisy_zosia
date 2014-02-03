# -*- coding: UTF-8 -*-
from datetime import timedelta
from django.core.mail import send_mail

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from django.utils import timezone
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
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
    ('m', _(u'klasyczna')),
    ('f', _(u'żeńska')),
)

BUS_HOUR_CHOICES = (
    ('brak',''),
    ('16:00', '16:00'),
    ('18:00', '18:00'),
    ('obojetne', 'obojętne'),
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
#


class Organization(models.Model):
    name     = models.CharField(max_length=64, default='')
    accepted = models.BooleanField(default=False)

    objects = OrganizationManager()

    class Meta:
        verbose_name = u'Organizacja'
        verbose_name_plural = u'Organizacje'

    def __unicode__(self):
        return u"%s" % self.name


class ParticipantManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=ParticipantManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Participant(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    first_name = models.TextField()
    last_name = models.TextField()
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = ParticipantManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    @property
    def is_staff(self):
        return self.is_superuser

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return smart_unicode(full_name)

    def get_short_name(self):
        "Returns the short name for the user."
        return smart_unicode(self.first_name)

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class UserPreferences(models.Model):
    # This is the only required field
    user = models.ForeignKey(Participant, unique=True)
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

    # used for opening rooms faster per-user;
    # e.g. 5 means room registration will open 5 minutes before global datetime
    # e.g. -5 means room registration will open 5 minutes after global datetime
    # FIXME needs actual implementation, so far it's only a stub field
    minutes_early = models.IntegerField(default=0)


    # used to differ from times on which buses leave
    bus_hour = models.CharField(max_length=10, choices=BUS_HOUR_CHOICES, null=True, default=None)


    photo_url = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=2048, blank=True, verbose_name=u'Opis')

    class Meta:
        verbose_name_plural = u'Preferencje'

    def __unicode__(self):
        return u"%s" % (self.user.first_name,)

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
                send_mail( u'Wpłata została zaksięgowana.',
                             t.render(Context({'rooming_time': rooming_time - timedelta(minutes=self.minutes_early)})),
                             'from@example.com',
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
