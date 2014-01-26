# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from polls.forms import PollForm
from polls.models import Poll


@require_POST
@login_required
@never_cache
def vote(request):
    poll = get_object_or_404(Poll, id=request.POST.get('poll_id', None))
    form = PollForm(request.POST, user=request.user, poll=poll)

    if form.is_valid():
        form.save()

        return redirect('polls:thanks')

    raise Http404

@login_required
def thanks(request):
    title = 'Polls'
    return TemplateResponse(request, 'polls/thanks.html', locals())

@login_required
@never_cache
def main(request):
    title = 'Polls'
    polls = Poll.filtered.open_for_user(request.user)

    for poll in polls:
        poll.form = PollForm(poll=poll, user=request.user)

    return TemplateResponse(request, 'polls/main.html', locals())