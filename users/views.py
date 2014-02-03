# -*- coding: UTF-8 -*-
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import base36_to_int
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import never_cache

from common.helpers import is_registration_disabled
from common.models import ZosiaDefinition
from users.forms import RegistrationForm, PreferencesForm, OrganizationForm, preferences_form_fabric

from users.models import UserPreferences, Participant
from users.utils import send_confirmation_mail, prepare_data


def register(request):
    if is_registration_disabled():
        raise Http404

    title = "Registration"
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)

    date_1, date_2, date_3, date_4 = definition.zosia_start, (definition.zosia_start + timedelta(days=1)),\
                                                 (definition.zosia_start + timedelta(days=2)),\
                                                 (definition.zosia_start + timedelta(days=3))
    user_form = RegistrationForm(request.POST or None)
    pref_form = preferences_form_fabric(definition)(request.POST or None)
    org_form = OrganizationForm(request.POST or None)

    f1 = user_form.is_valid()
    f2 = pref_form.is_valid()
    f3 = org_form.is_valid()
    if f1 and f2 and f3:
        user = user_form.save()
        org = org_form.save()

        send_confirmation_mail(request, user, definition)
        preference = pref_form.save(commit=False)
        preference.user = user
        preference.org = org
        preference.state = definition
        preference.save()

        return HttpResponseRedirect('/register/thanks/')
    return render_to_response('register_form.html', locals())


@never_cache
@login_required
def change_preferences(request):
    user = request.user
    title = "Change preferences"
    prefs = UserPreferences.objects.get(user=user)
    user_paid = prefs.paid
    free_seats = UserPreferences.get_free_seats() or prefs.bus
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)
    user_opening_hour = definition.rooming_start - timedelta(minutes=prefs.minutes_early) # for sure to change

    date_1, date_2, date_3, date_4 = definition.zosia_start, (definition.zosia_start + timedelta(days=1)),\
                                                 (definition.zosia_start + timedelta(days=2)),\
                                                 (definition.zosia_start + timedelta(days=3))
    if request.POST:
        # raise Http404 # the most nooby way of blocking evar (dreamer_)
        # bug with settings not updateble
        # after user paid
        post = prepare_data(request.POST, prefs)
        pref_form = preferences_form_fabric(definition, prefs)(post, instance=prefs)
        if pref_form.is_valid():
            prefs = pref_form.save()
            payment = prefs.count_payment()

    else:
        pref_form = preferences_form_fabric(definition, prefs)(instance=prefs)
        payment = prefs.count_payment()
    user_wants_bus = prefs.bus
    return render_to_response('change_preferences.html', locals())


def activate_user(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
        usr = get_object_or_404(Participant, id=uid_int)
    except Exception:
        return render_to_response('reactivation.html', {})
    if token_generator.check_token(usr, token):
        usr.is_active = True
        usr.save()
    else:
        return render_to_response('reactivation.html', {})
    return HttpResponseRedirect('/login/?next=/change_preferences/') # yeah, right...


def regulations(request):
    # Setting title makes "Registration" link visible on the panel.
    title = "Registration"
    try:
        definition = ZosiaDefinition.objects.get(active_definition=True)
    except Exception:
        raise Http404
    zosia_start = definition.zosia_start
    zosia_final = definition.zosia_final
    return render_to_response('regulations.html', locals())


def thanks(request):
    user = request.user
    title = "Registration"
    return render_to_response('thanks.html', locals())


@login_required
def users_status(request):
    if not ( request.user.is_staff and request.user.is_active ):
        raise Http404
    # nie no, to jest źle...
    # users = User.objects.all()
    # prefs = UserPreferences.objects.all()
    #list = zip(users,prefs)
    list = []
    return render_to_response('the_great_table.html', locals())


def register_payment(request):
    user = request.user
    if not user.is_authenticated() or not user.is_staff or not user.is_active:
        raise Http404
    if not request.POST:
        raise Http404
    pid = request.POST['id']
    prefs = UserPreferences.objects.get(id=pid)
    prefs.paid = True
    prefs.save()
    return HttpResponse("ok")
