# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_text
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

            print(smart_text(get_ping(preferences[i])) + smart_text(first_name) + smart_text(get_ping(b)) + smart_text(second_name) + smart_text(get_rot(preferences[i])) +\
                  smart_text(first_name) + smart_text(get_rot(b)) + smart_text(second_name) + " \confpinfood" + \
                  smart_text(first_meals) + " \confpinfood" + smart_text(second_meals))
            print('')


def get_ping(preference):
    if preference.org.name.strip() != '':
        return ' \confpin'
    else:
        return ' \confpinnoorg'

def get_rot(preference):
    if preference.org.name.strip() != '':
        return ' \confpinrot'
    else:
        return ' \confpinnoorgrot'


def generate_name(preference):
    result = "{" + smart_text(preference.user.get_full_name()) + "}"
    if preference.org.name.strip() != '':
        result += "{ " + smart_text(preference.org.name.strip()) + "}"
    return result


def generate_meals(preference):
    result = ''
    if preference.dinner_1:
        result += '{ Czw - obiad, 20:00-21:30 ' + str(is_vegetarian(preference))  +'}'
    else:
        result += '{}'
    if preference.breakfast_2:
        result += '{ Pią - śniadanie, 7:30-9:30 '+ str(is_vegetarian(preference))  +'}'
    else:
        result += '{}'
    if preference.dinner_2:
        result += '{ Pią - obiad, 17:30-19:00 '+ str(is_vegetarian(preference))  +'}'
    else:
        result += '{}'
    if preference.breakfast_3:
        result += '{ Sob - śniadanie, 7:30-9:30 '+ str(is_vegetarian(preference))  +'}'
    else:
        result += '{}'
    if preference.dinner_3:
        result += '{ Sob - obiad, 17:30-19:00 '+  str(is_vegetarian(preference))  +'}'
    else:
        result += '{}'
    if preference.breakfast_4:
        result += '{ Nie - śniadanie, 7:30-9:30 '+ str(is_vegetarian(preference)) + '}'
    else:
        result += '{}'

    return result


def is_vegetarian(preference):
    if preference.vegetarian:
        return ' W '
    else:
        return ''
