# -*- coding: UTF-8 -*-
from datetime import timedelta
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite
from django.core.mail import send_mail
from django.forms import ModelForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, Context
from django.utils.http import int_to_base36
from django.utils.translation import ugettext as _
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import base36_to_int, int_to_base36
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import never_cache

from common.helpers import is_registration_disabled
from common.models import ZosiaDefinition

from users.models import UserPreferences, Participant, Organization


class RegistrationForm(ModelForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)

    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        fields = ('email', 'first_name', 'last_name')
        model = Participant

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Hasła są różne', code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(ModelForm, self).save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PreferencesForm(ModelForm):

    class Meta:
        fields = ('day_1', 'day_2', 'day_3',
                  'breakfast_2', 'breakfast_3', 'breakfast_4',
                  'dinner_1', 'dinner_2', 'dinner_3',
                  'bus', 'vegetarian', 'shirt_size', 'shirt_type')
        model = UserPreferences


class OrganizationForm(ModelForm):
    organization_1 = forms.ChoiceField(choices=Organization.objects.get_organization_choices())
    organization_2 = forms.CharField(required=False, max_length=255)

    class Meta:
        fields = ()
        model = Organization

    def save(self, commit=True):
        try:
            org1 = self.cleaned_data['organization_1']
            org2 = self.cleaned_data['organization_2']

            if org1 == 'new':
                org = Organization(name=org2, accepted=False)
            else:
                org = Organization.objects.get(id=org1)
        except:
            org = Organization("fail",accepted=False)

        if commit:
            org.save()

        return org


def send_confirmation_mail(request, user, definition):
        t = loader.get_template("activation_email.txt")
        c = {
            'site_name': RequestSite(request),
            'uid': int_to_base36(user.id),
            'token': token_generator.make_token(user),
            'payment_deadline': definition.payment_deadline,
            }
        send_mail( u'Potwierdź założenie konta na zosia.org',
            t.render(Context(c)),
            'ksi@cs.uni.wroc.pl',
            [ user.email ],
            fail_silently=True )

def prepare_data(post, preference):
    if preference.paid:
        rewritten_post = {}
        for k in post.keys():
            rewritten_post[k] = post[k]
        for k in [ 'day_1', 'day_2', 'day_3',
                   'breakfast_2', 'breakfast_3', 'breakfast_4',
                   'dinner_1', 'dinner_3', 'dinner_2', 'bus', 'vegetarian' ]:
            if preference.__dict__[k]:
                rewritten_post[k] = u'on'
            elif k in rewritten_post:
                del rewritten_post[k]
        rewritten_post['shirt_type'] = preference.__dict__['shirt_type']
        rewritten_post['shirt_size'] = preference.__dict__['shirt_size']

        return rewritten_post

    return post

def register(request):
    if is_registration_disabled():
        raise Http404

    title = "Registration"
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)

    date_1, date_2, date_3, date_4 = definition.zosia_start, (definition.zosia_start + timedelta(days=1)),\
                                                 (definition.zosia_start + timedelta(days=2)),\
                                                 (definition.zosia_start + timedelta(days=3))
    user_form = RegistrationForm(request.POST or None)
    pref_form = PreferencesForm(request.POST or None)
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
        pref_form = PreferencesForm(post, instance=prefs)
        if pref_form.is_valid():
            prefs = pref_form.save()
            payment = prefs.count_payment()

    else:
        pref_form = PreferencesForm(instance=prefs)
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
