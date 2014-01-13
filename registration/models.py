# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import Context, loader
from common.models import ZosiaDefinition
from datetime import timedelta

# this is small hack to make user
# more meaningfull (we're using email as
# user id anyway)
User.__unicode__ = User.get_full_name


# converts organizations in database into
# choices for option fields
def getOrgChoices():
    list = [ (org.id, org.name)
           for org in Organization.objects.filter(accepted=True) ]
    list = list[:20]
    list.append( ('new', 'inna') )
    return tuple(list)
#
# class UserPreferences(models.Model):
#     # This is the only required field
#     user = models.ForeignKey(User, unique=True)
#
#     # ? anonimowy - nie chce zeby jego imie/nazwisko/mail pojawialy sie na stronie
#
#
#     def __unicode__(self):
#         return u"%s %s" % (self.user.first_name, self.user.last_name)
#
#     def save(self):
#         # at this moment object probably is different from one in
#         # database - lets check if 'paid' field is different
#         try:
#             old = UserPreferences.objects.get(id=self.id)
#             definition = ZosiaDefinition.objects.get(active_definition=True)
#             rooming_time = definition.rooming_start
#             if self.paid and not old.paid:
#                 t = loader.get_template('payment_registered_email.txt')
#                 send_mail( u'Wpłata została zaksięgowana.',
#                              t.render(Context({'rooming_time': rooming_time - timedelta(minutes=self.minutes_early)})),
#                              'from@example.com',
#                              [ self.user.email ],
#                              fail_silently=True )
#         except Exception:
#             # oh, we're saving for the first time - it's ok
#             # move along, nothing to see here
#             pass
#         super(UserPreferences, self).save()
#
#     @property
#     def get_room(self):
#         from rooms.models import UserInRoom
#         if not hasattr(self, 'user_room'):
#             try:
#                 self.user_room = UserInRoom.objects.get(locator=self.user).room
#             except:
#                 self.user_room = 0
#         return self.user_room
#
#     @staticmethod
#     def get_free_seats():
#         return (BUS_SECOND_SIZE+BUS_FIRST_SIZE - UserPreferences.objects.filter(bus=True).count()) > 0
#
#     @staticmethod
#     def get_first_time():
#         return  (BUS_FIRST_SIZE - UserPreferences.objects.filter(bus=True, bus_hour=BUS_HOUR_CHOICES[1][0]).count()) > 0
#
#     @staticmethod
#     def get_second_time():
#         return  (BUS_SECOND_SIZE - UserPreferences.objects.filter(bus=True, bus_hour=BUS_HOUR_CHOICES[2][0]).count()) > 0
#
#
#
