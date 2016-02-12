from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views, forms

urlpatterns = [
    # login / logout
    url(
        r'^login/$',
        auth_views.login,
        {'template_name': 'login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/logout/bye/'},
        name='logout'
    ),
    url(r'^logout/bye/$', views.thanks),

    # urls required for password change/reset
    url(r'^password_change/$', views.password_change),
    url(r'^password_change/done/$', views.password_change_done),

    url(
        r'^password_reset/$',
        auth_views.password_reset,
        {'template_name': 'password_reset_form.html'},
        name='password_reset'
    ),
    url(
        r'^password_reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'password_reset_done.html'},
        name='password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'
    ),
]
