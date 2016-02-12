from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .forms import *

def thanks(request):
    title = "Bye!"
    return render(request, 'bye.html', locals())


@login_required
def password_change(request):
    title = "Change password"
    pc_form = ValidatedPasswordChangeForm(request.user, request.POST or None)
    if pc_form.is_valid():
        pc_form.save()
        return HttpResponseRedirect("done/")
    return render(request, "change_password.html", locals())

@login_required
def password_change_done(request):
    title = "Change password"
    return render(request, "change_password_done.html", locals())

