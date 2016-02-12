# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext as _
from django.shortcuts import render

from common.helpers import *

from .forms import *


def index(request):
    title = "Lectures"
    sponslectures = Lecture.objects.filter(accepted=True, person_type=0).order_by('order')
    lectures = Lecture.objects.filter(accepted=True, person_type__gte=1).order_by('person_type', 'order')
    lectures_null = Lecture.objects.filter(accepted=True, person_type__gte=1).order_by('person_type', 'order')
    if request.user.is_authenticated():
        my_lectures = Lecture.objects.filter(author=request.user)

    workshops = Lecture.objects.filter(accepted=True, person_type__gte=1, type=1).order_by('person_type', 'order')
    if is_lecture_suggesting_enabled():
        if request.user.is_authenticated() and request.user.is_active:
            lecture_proposition_form = LectureForm(request.POST or None)
            if lecture_proposition_form.is_valid():
                lecture = lecture_proposition_form.save(commit=False)
                lecture.author = request.user
                lecture.save()
                messages = [ _("thankyou") ]
                lecture_proposition_form = LectureForm()

    return render(request, 'lectures.html', locals())
