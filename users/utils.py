# -*- coding: UTF-8 -*-
from django.contrib.sites.models import RequestSite
from django.core.mail import send_mail
from django.template import loader, Context
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import int_to_base36


def send_confirmation_mail(request, user, definition):
        t = loader.get_template("activation_email.txt")
        c = {
            'site_name': RequestSite(request),
            'uid': int_to_base36(user.id),
            'token': token_generator.make_token(user),
            'payment_deadline': definition.payment_deadline,
            }
        send_mail( u'Potwierdź założenie konta na zosia.org',
            t.render(Context(c)),
            'ksi@cs.uni.wroc.pl',
            [ user.email ],
            fail_silently=True )


def prepare_data(post, preference):
    if preference.paid:
        rewritten_post = {}
        for k in post.keys():
            rewritten_post[k] = post[k]
        for k in [ 'day_1', 'day_2', 'day_3',
                   'breakfast_2', 'breakfast_3', 'breakfast_4',
                   'dinner_1', 'dinner_3', 'dinner_2', 'bus', 'vegetarian' ]:
            if preference.__dict__[k]:
                rewritten_post[k] = u'on'
            elif k in rewritten_post:
                del rewritten_post[k]
        rewritten_post['shirt_type'] = preference.__dict__['shirt_type']
        rewritten_post['shirt_size'] = preference.__dict__['shirt_size']

        return rewritten_post

    return post