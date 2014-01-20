# -*- coding: UTF-8 -*-

from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template.response import TemplateResponse

from common.forms import LoginForm
from common.models import ZosiaDefinition
from models import *


def index(request):
    user = request.user
    blog_posts = BlogPost.objects.order_by('-pub_date')
    user       = request.user
    title      = "Blog"
    login_form = LoginForm()

    try:
        definition = ZosiaDefinition.objects.get(active_definition=True)
    except Exception:
        raise Http404

    return TemplateResponse(request, 'blog.html', locals())

