# -*- coding: UTF-8 -*-

from .models import Sponsor


def sponsors(request):
    return {
        'sponsors': Sponsor.objects.all()
    }
