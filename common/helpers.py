# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from common.models import ZosiaDefinition
from django.http import Http404

# TODO: this module should be replaced by calls to database
from users.models import UserPreferences


def is_registration_enabled():
    # this is the only place that should be changed
    try:
        definition = ZosiaDefinition.objects.get(active_definition=True)
    except Exception:
        raise Http404
    start_date = definition.registration_start
    final_date = definition.registration_final
    assert start_date <= final_date
    return datetime.now() > start_date and datetime.now() < final_date


def is_registration_disabled():
    return not is_registration_enabled()


def is_lecture_suggesting_enabled():
    # this is the only place that should be changed
    try:
        definition = ZosiaDefinition.objects.get(active_definition=True)
    except Exception:
        raise Http404
    start_date = definition.lectures_suggesting_start
    final_date = definition.lectures_suggesting_final
    assert start_date < final_date
    return datetime.now() > start_date and datetime.now() < final_date


def is_lecture_suggesting_disabled():
    return not is_lecture_suggesting_enabled()


def is_rooming_enabled(request = None):
    if request:
        return has_user_opened_records(request.user)
    try:
        definition = ZosiaDefinition.objects.get(active_definition=True)
    except Exception:
        raise Http404
    start_date = definition.rooming_start
    final_date = definition.rooming_final

    assert start_date < final_date

    return start_date < datetime.now() < final_date


def has_user_opened_records(user):
    return user.has_opened_records


def is_rooming_disabled(request=None):
    return not is_rooming_enabled(request)

