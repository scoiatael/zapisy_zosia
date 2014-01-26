# -*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import Question, UserAnswer


class PollForm(forms.Form):
    answer = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.RadioSelect, empty_label=None, label=u'Odpowiedź')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.poll = kwargs.pop('poll', None)

        if not self.user or not self.poll:
            raise Http404

        super(PollForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = Question.objects.filter(poll=self.poll)
        try:
            answer = UserAnswer.objects.get(user=self.user, question__poll=self.poll)
            self.fields['answer'].initial = answer.question.id
        except ObjectDoesNotExist:
            pass

    def save(self):
        try:
            answer = UserAnswer.objects.get(user=self.user, question__poll=self.poll)
        except ObjectDoesNotExist:
            answer = UserAnswer(user=self.user)

        answer.question=self.cleaned_data['answer']
        answer.save()