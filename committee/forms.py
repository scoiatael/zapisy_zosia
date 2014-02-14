# -*- coding: UTF-8 -*-
from django import forms
from django.forms.models import modelformset_factory
from committee.models import Vote


VoteFormset = modelformset_factory(Vote, fields=('value', 'text'), extra=0)