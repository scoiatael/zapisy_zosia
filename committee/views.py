from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from committee.forms import VoteFormset
from committee.models import Vote
from lectures.models import Lecture


@login_required
@never_cache
def lectures(request):
    if not request.user.committee:
        raise Http404

    lectures = Lecture.objects.filter(for_committe=True)
    for lecture in lectures:
        Vote.objects.get_or_create(user=request.user, lecture=lecture)

    formset = VoteFormset(queryset=Vote.objects.filter(user=request.user))

    return TemplateResponse(request, 'committee/lectures.html', locals())


@login_required
@require_POST
def vote(request):
    if not request.user.committee:
        raise Http404('There is no user.committee')

    formset = VoteFormset(request.POST)
    if not formset.is_valid():
        raise Http404('Invalid formset')
    formset.save()

    return redirect('committee:main')



