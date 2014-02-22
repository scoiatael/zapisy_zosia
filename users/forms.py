# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
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
                  'bus', 'vegetarian', 'shirt_size', 'shirt_type', 'bus_hour')
        model = UserPreferences

    def __init__(self, *args, **kwargs):
        options = [('', u'obojętne')]
        preference = kwargs.get('instance', None)
        super(PreferencesForm,self).__init__(*args, **kwargs)
        if preference:
            if preference.bus16_available():
                options += [('16:00', '16:00')]
            if preference.bus18_available():
                options += [('18:00', '18:00')]
            
            self.fields['bus_hour'].choices = options



class PreferencesNoBusForm(ModelForm):

    class Meta:
        fields = ('day_1', 'day_2', 'day_3',
                  'breakfast_2', 'breakfast_3', 'breakfast_4',
                  'dinner_1', 'dinner_2', 'dinner_3',
                  'want_bus', 'vegetarian', 'shirt_size', 'shirt_type')
        model = UserPreferences


def preferences_form_fabric(definition, preferences=None):
    if definition.bus_is_full and (not preferences or not preferences.bus):
        return PreferencesNoBusForm
    else:
        return PreferencesForm


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
