from django.utils.timezone import timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import base36_to_int
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import never_cache

from common.helpers import is_registration_disabled, is_free_rooms
from common.models import ZosiaDefinition
from users.forms import RegistrationForm, PreferencesForm, OrganizationForm, preferences_form_fabric, WaitingForm

from users.models import UserPreferences, Participant
from users.utils import send_confirmation_mail, prepare_data


def register(request):
    if is_registration_disabled():
        raise Http404('Registration is disabled')

    if not is_free_rooms():
        return HttpResponseRedirect('/waiting/')

    title = "Registration"
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)

    date_1 = definition.zosia_start
    date_2 = date_1 + timedelta(days=1)
    date_3 = date_2 + timedelta(days=1)
    date_4 = date_3 + timedelta(days=1)

    login_form = None
    user_form = RegistrationForm(request.POST or None)
    pref_form = preferences_form_fabric(definition)(request.POST or None)
    org_form = OrganizationForm(request.POST or None)

    f1 = user_form.is_valid()
    f2 = pref_form.is_valid()
    f3 = org_form.is_valid()
    if not (f1 and f2 and f3):
        return render(request, 'register_form.html', locals())
    
    user = user_form.save()
    org = org_form.save()

    send_confirmation_mail(request, user, definition)
    preference = pref_form.save(commit=False)
    preference.user = user
    preference.org = org
    preference.state = definition
    preference.save()

    return HttpResponseRedirect('/register/thanks/')


def waiting_list(request):
    title = "Registration"
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)

    date_1 = definition.zosia_start
    date_2 = date_1 + timedelta(days=1)
    date_3 = date_2 + timedelta(days=1)
    date_4 = date_3 + timedelta(days=1)

    if request.POST:
        form = WaitingForm(request.POST)
        user_form = RegistrationForm(request.POST)

        f1 = form.is_valid()
        f2 = user_form.is_valid()

        if f1 and f2:
            user = user_form.save()
            send_confirmation_mail(request, user, definition)

            waiting = form.save(commit=False)
            waiting.state = definition
            waiting.user = user
            waiting.save()

            return HttpResponseRedirect('/register/thanks/')

    form = WaitingForm(request.POST)
    user_form = RegistrationForm(request.POST)

    return render(request, 'waiting.html', {'pref_form': form, 'user_form': user_form,
                                               'date_1': date_1, 'date_2': date_2, 'date_3': date_3, 'date_4': date_4,
                                               'definition': definition})

@never_cache
@login_required
def change_preferences(request):
    title = "Change preferences"
    try:
        prefs = UserPreferences.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/waiting/')

    user_paid = prefs.paid
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
    return render(request, 'change_preferences.html', locals())


def activate_user(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
        usr = get_object_or_404(Participant, id=uid_int)
    except Exception:
        return render(request, 'reactivation.html', {})
    if token_generator.check_token(usr, token):
        usr.is_active = True
        usr.save()
    else:
        return render(request, 'reactivation.html', {})
    return HttpResponseRedirect('/login/?next=/change_preferences/') # yeah, right...


def regulations(request):
    # Setting title makes "Registration" link visible on the panel.
    title = "Registration"
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)
    zosia_start = definition.zosia_start
    zosia_final = definition.zosia_final
    return render(request, 'regulations.html', locals())


def thanks(request):
    title = "Registration"
    return render(request, 'thanks.html', locals())


@login_required
def users_status(request):
    if not ( request.user.is_staff and request.user.is_active ):
        raise Http404('User is not staff memeber or is not active')
    # nie no, to jest źle...
    # users = User.objects.all()
    # prefs = UserPreferences.objects.all()
    #list = zip(users,prefs)
    list = []
    return render(request, 'the_great_table.html', locals())


def register_payment(request):
    if not request.POST:
        raise Http404('POST only')
    if not request.user.is_authenticated() or not request.user.is_staff or not request.user.is_active:
        raise Http404('User is not authenticated or is not staff memeber or is not active')
    pid = request.POST['id']
    prefs = UserPreferences.objects.get(id=pid)
    prefs.paid = True
    prefs.save()
    return HttpResponse('ok')
