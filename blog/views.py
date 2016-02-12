from django.shortcuts import (
    get_object_or_404, render
)

from common.models import ZosiaDefinition
from .models import *

def index(request):
    title      = 'Blog'
    blog_posts = BlogPost.objects.order_by('-pub_date')
    definition = get_object_or_404(ZosiaDefinition, active_definition=True)
    return render(request, 'blog.html', locals())
