# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_unicode
from users.models import UserPreferences


class Command(BaseCommand):
    def handle(self, *args, **options):
        preferences = UserPreferences.objects.filter(user__is_active=True)

        for i in range(0, preferences.count(), 2):
            b = preferences[i + 1 if i + 1< preferences.count() else i]

            first_name = generate_name(preferences[i])
            second_name = generate_name(b)
            first_meals = generate_meals(preferences[i])
            second_meals = generate_meals(b)

            print smart_unicode(get_ping(preferences[i])) + smart_unicode(first_name) + smart_unicode(get_ping(b)) + smart_unicode(second_name) + smart_unicode(get_rot(preferences[i])) +\
                  smart_unicode(first_name) + smart_unicode(get_rot(b)) + smart_unicode(second_name) + " \confpinfood" + \
                  smart_unicode(first_meals) + " \confpinfood" + smart_unicode(second_meals)
            print ''


def get_ping(preference):
    if preference.org.name.strip() <> '':
        return u' \confpin'
    else:
        return u' \confpinnoorg'

def get_rot(preference):
    if preference.org.name.strip() <> '':
        return u' \confpinrot'
    else:
        return u' \confpinnoorgrot'


def generate_name(preference):
    result = u"{" + smart_unicode(preference.user.get_full_name()) + u"}"
    if preference.org.name.strip() <> '':
        result += "{ " + smart_unicode(preference.org.name.strip()) + u"}"
    return result


def generate_meals(preference):
    result = ''
    if preference.dinner_1:
        result += u'{ Czw - obiad, 20:00-21:30 ('+ str(preference.get_room) + str(is_vegetarian(preference))  +')}'
    else:
        result += u'{}'
    if preference.breakfast_2:
        result += u'{ Pią - śniadanie, 7:30-9:30 ('+ str(preference.get_room) + str(is_vegetarian(preference))  +')}'
    else:
        result += u'{}'
    if preference.dinner_2:
        result += u'{ Pią - obiad, 17:30-19:00 ('+ str(preference.get_room) + str(is_vegetarian(preference))  +')}'
    else:
        result += u'{}'
    if preference.breakfast_3:
        result += u'{ Sob - śniadanie, 7:30-9:30 ('+ str(preference.get_room) + str(is_vegetarian(preference))  +')}'
    else:
        result += u'{}'
    if preference.dinner_3:
        result += u'{ Sob - obiad, 17:30-19:00 ('+ str(preference.get_room) + str(is_vegetarian(preference))  +')}'
    else:
        result += u'{}'
    if preference.breakfast_4:
        result += u'{ Nie - śniadanie, 7:30-9:30 ('+ str(preference.get_room) + str(is_vegetarian(preference)) + ')}'
    else:
        result += u'{}'

    return result


def is_vegetarian(preference):
    if preference.vegetarian:
        return ' W '
    else:
        return ''