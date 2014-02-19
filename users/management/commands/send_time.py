from django.core.management.base import BaseCommand
from users.models import UserPreferences
from users.utils import send_time_email


class Command(BaseCommand):

    for pref in UserPreferences.objects.filter(paid=True):
        send_time_email(pref)
