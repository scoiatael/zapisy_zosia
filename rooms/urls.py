from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list.json$', views.json_rooms_list, name='json_rooms_list'),
    url(r'^modify/$', views.modify_room, name='modify'),
    url(r'^open/$', views.open_room, name='open'),
    url(r'^close/$', views.close_room, name='close'),
    url(r'^trytogetin/$', views.trytogetin_room, name='trytogetin'),
    url(r'^leave/$', views.leave_room, name='leave'),
]
