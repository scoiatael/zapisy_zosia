# -*- coding: UTF-8 -*-

from django import forms
from lectures.models import Lecture


class LectureForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'duration', 'abstract', 'info')
        model = Lecture

