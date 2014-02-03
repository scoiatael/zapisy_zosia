# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response

from common.forms import LoginForm
from common.helpers import *

from forms import *


def index(request):
    title = "Lectures"
    user = request.user
    sponslectures = Lecture.objects.filter(accepted=True, person_type=0).order_by('order')
    lectures = Lecture.objects.filter(accepted=True, person_type__gte=1).order_by('person_type', 'order')
    lectures_null = Lecture.objects.filter(accepted=True, person_type__gte=1).order_by('person_type', 'order')


    workshops = Lecture.objects.filter(accepted=True, person_type__gte=1, type=1).order_by('person_type', 'order')
    if is_lecture_suggesting_enabled():
        login_form = LoginForm()
        if user.is_authenticated() and user.is_active:
            lecture_proposition_form = LectureForm(request.POST or None)
            if lecture_proposition_form.is_valid():
                lecture = lecture_proposition_form.save(commit=False)
                lecture.author = request.user
                lecture.save()
                messages = [ _("thankyou") ]
                lecture_proposition_form = LectureForm()

    return render_to_response('lectures.html', locals())


def program(request):
    title = "Program"
    user = request.user
    return render_to_response('program.html', locals())

