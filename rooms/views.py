from django.views.decorators.cache import cache_page
from django.http import *
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.crypto import get_random_string
from django.utils import timezone

from datetime import timedelta
import json as json_lib

from .models import *
from common.helpers import *

@login_required
def index(request):
    """

    """
    if not request.user.has_opened_records:
        raise Http404

    user = request.user
    title = "Rooms"
    return render(request, 'rooms.html',locals())


#@login_required
@cache_page(30)
@csrf_exempt
def json_rooms_list(request):
    if not request.user.has_opened_records:
        raise Http404('there is no opened records for user')
    json = Room.objects.to_json(request)
    return HttpResponse(json, content_type='application/json')

def dict_to_json(d):
    ret = []
    for k,v in list(d.items()): ret.append('"%s":"%s"'%(k,v))
    return '{%s}'%(','.join(ret))


def get_in_room(usr,room,own=False):
    occupation = UserInRoom( locator=usr,
                             room=room,
                             ownership=own
                           )
    occupation.save()

def get_room_locators(room):
    # return html
    occs = UserInRoom.objects.filter(room=room)
    if not occs:
        return ''
    else:
        lst =  ','.join( [ " %s"%o.locator for o in occs ] )
        return "Mieszkają tu: %s<br/>" % lst

@login_required
def trytogetin_room(request):
    if not request.POST: raise Http404
    if not has_user_opened_records(request.user): return HttpResponse('fail')
    room = Room.objects.filter(hidden=False).get(id=int(request.POST['rid']))
    if room.password == request.POST['key']:
        get_in_room(request.user, room)
        return HttpResponse('ok')
    return HttpResponse('fail')

@login_required
@csrf_exempt
def open_room(request):
    if not request.POST: raise Http404
    if not has_user_opened_records(request.user): return HttpResponse('fail')
    occupation = UserInRoom.objects.get(locator=request.user)
    if occupation.ownership:
        room = occupation.room
        if room.password == request.POST['key']:
            occupation.room.short_unlock_time = timezone.now()
            occupation.room.save()
            return HttpResponse('ok')

@login_required
@csrf_exempt
def close_room(request):
    if not request.POST: raise Http404
    if not has_user_opened_records(request.user): return HttpResponse('fail')
    occupation = UserInRoom.objects.get(locator=request.user)
    if occupation.ownership:
        room = occupation.room
        no_locators = 0
        if room.password == request.POST['key']:
            no_locators = UserInRoom.objects.filter(room=room).count()
        if no_locators == 1: # user is still alone in this room
                timeout = timedelta(0,4*60*60,0)
                occupation.room.short_unlock_time = timezone.now() + timeout
                occupation.room.save()
                return HttpResponse('ok')


CONST_LEAVE_ROOM_BTN = '''<button onclick=\"window.location='leave/'\">Opuść pokój</button>'''
CONST_OK_BTN = '<button onclick=\'hideDialog()\'>OK</button>'
CONST_OK2_BTN = '<button onclick=\'hideDialog()\'>Zostań w pokoju</button>'
# CONST_LEAVE_OPEN_ROOM_BTN = u'<button onclick=\'Rooms.hideDialog(1)\'>Otwórz pokój</button>'
# CONST_USE_KEY_BTN = u'<button>Zamknij pokój</button>'
def leave_open_room_btn(key): return '<button onclick=\'Rooms.hideDialog(%s)\'>Wejdź i nie zamykaj</button>' % key
def close_room_btn(key): return '<button onclick=\'Rooms.closeRoom(%s)\'>Wejdź i zamknij kluczem</button>' % key
CONST_FORM = """<form><input type=\'submit\' value=\'Ustaw hasło\'/></form>"""


@login_required
@csrf_exempt
def leave_room(request):
    try:
        prev_occupation = UserInRoom.objects.get(locator=request.user)
        prev_occupation.delete()
    except Exception: pass
    # finally: TODO check which versions of Python support 'finally' keyword
    return HttpResponseRedirect('/rooms/')


@require_POST
@login_required
@csrf_exempt
def modify_room(request):
    # get correct room based on rid
    room_number = request.POST['rid'][1:]
    room = Room.objects.filter(hidden=False).get(number=room_number)
    status = room.get_status(request)
    json = { "room_number":room_number, "buttons":'', 'msg':'', 'form':'' }
    prev_occupation = None
    try:
        prev_occupation = UserInRoom.objects.get(locator=request.user)
    except Exception:
        pass
    if not status:
        #
        # this room is open
        #
        msg = ''
        no_locators = room.get_no_locators()
        if not no_locators:
            #
            # case when room is empty
            #
            if prev_occupation:
                json['msg'] = "<br/>Jeśli chcesz się dopisać do tego pokoju,<br/>musisz najpierw wypisać się z pokoju %s.<br/>" % prev_occupation.room
                json['buttons'] = CONST_OK_BTN
            else:
                get_in_room(request.user, room, True)
                timeout = timedelta(0,120,0) # 2 minutes
                room.short_unlock_time = timezone.now() + timeout
                import string
                room.password = get_random_string(6, string.digits)
                room.save()
                json['msg'] = "<br/>Przekaż klucz swoim znajomym, aby<br/>mogli dołączyć do tego pokoju.<br/><br/>"
                json['form'] = "Klucz do pokoju: <strong>{}</strong><br/>".format(room.password)
                json['buttons'] = close_room_btn(room.password) + leave_open_room_btn(room.password) + CONST_LEAVE_ROOM_BTN
        else:
            #
            # case when room is not empty
            #
            if (prev_occupation is not None) and (prev_occupation.room == room):
                json['msg'] = 'Mieszkasz w tym pokoju.'
                json['buttons'] = CONST_OK_BTN + CONST_LEAVE_ROOM_BTN
            elif (prev_occupation is None):
                get_in_room(request.user, room)
                json['msg'] = "<br/>Właśnie dołączyłeś do tego pokoju<br/>"
                json['buttons'] = CONST_OK2_BTN + CONST_LEAVE_ROOM_BTN
            else: # prev_occ and not in this room
                json['msg'] = "<br/>Jeśli chcesz się dopisać do tego pokoju,<br/>musisz najpierw opuścić pokój %s.<br/>" % prev_occupation.room
                json['buttons'] = CONST_OK_BTN
    elif status == 1:
        #
        # this room is locked or has password
        #
        if prev_occupation and (prev_occupation.room == room):
            json['msg'] = "<br/>Zamknięty kluczem: <strong>%s</strong><br/>" % room.password
            json['buttons'] = CONST_OK_BTN + CONST_LEAVE_ROOM_BTN
        elif not prev_occupation:
            json['msg'] = "<br/>Ten pokój jest zamknięty.<br/><input id='in_key' type='text' maxlength='6' size='6'></input><button onclick=\'Rooms.tryGetIn(%s)\'>Dopisz się</button>" % room.id
            json['buttons'] = "<button onclick=\'hideDialog()\'>Anuluj</button>"
        else: # prev_occ and not in this room
            json['msg'] = "<br/>Ten pokój jest zamknięty kluczem. Ponadto jeśli chcesz się do niego dopisać musisz najpierw opuścić pokój %s.<br/>" % prev_occupation.room
            json['buttons'] = CONST_OK_BTN
    elif status == 2: # room is full
        #
        # TODO: opcja do wypisania sie?
        #
        json['msg'] = "<br/>Ten pokój jest już pełny.<br/>"
        json['buttons'] = CONST_OK_BTN
        if prev_occupation and (prev_occupation.room == room):
            json['buttons'] = CONST_OK_BTN + CONST_LEAVE_ROOM_BTN

    elif status == 3:
        json['msg'] = "<br/>Zapisy na pokoje są zamknięte.<br/>"
        json['buttons'] = CONST_OK_BTN
    json['locators'] = get_room_locators(room)
    return HttpResponse(json_lib.dumps(json), content_type='application/json')
