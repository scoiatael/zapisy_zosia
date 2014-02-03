# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.encoding import smart_unicode
from models import UserPreferences, SHIRT_TYPES_CHOICES, Organization, Participant


class ParticipantAdmin(admin.ModelAdmin):
    pass


class UserPreferencesAdmin(admin.ModelAdmin):
    list_per_page = 400
    list_display = ('user_name', 'user_email', 'org',
        'days',
        'breakfasts',
        'dinners',
        'vegetarian',
        'shirt',
        'bus',
        'want_bus',
        'ZOSIA_cost',
        'paid',
        'minutes_early',)
    list_filter = ['bus_hour', 'paid', 'bus', 'want_bus', 'breakfast_2', 'breakfast_3',
                   'breakfast_4', 'dinner_1', 'dinner_2', 'dinner_3', 'day_1', 'day_2', 'day_3', 'shirt_size', 'shirt_type', 'org']
    list_editable = ('minutes_early', 'paid')

    def user_name(self, item):
        return smart_unicode(item.user.get_full_name())

    def user_email(self, item):
        return str(item.user.email)

    def anim_icon(self,id):
        return '<img src="/static_media/images/macthrob-small.png" alt="loading" id="anim%s" style="display:none"/>'%id
    yes_icon = '<img src="/static_media/images/icon-yes.gif" alt="Yes" />'
    no_icon  = '<img src="/static_media/images/icon-no.gif" alt="No" />'
    def onclick(self,id,obj):
        return u"""if(confirm('Do you want to register payment from %s?')) {
        document.getElementById('anim%s').style.display='inline';
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState  == 4) {
                document.getElementById('anim%s').style.display='none';
                if( xhr.status == 200) {
                    window.location.reload();
                }
            }
        };
        xhr.open('POST', '/admin/register_payment/', true);
        xhr.send('id=%s');
        }""" % (obj, id, id, id)
    def bus_onclick(self,obj):
        id = obj.id
        return u"""if(confirm('Do you want to register transport payment from %s?')) {
        //document.getElementById('anim%s').style.display='inline';
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState  == 4) {
                //document.getElementById('anim%s').style.display='none';
                if( xhr.status == 200) {
                    window.location.reload();
                }
            }
        };
        xhr.open('POST', '/admin/register_bus_payment/', true);
        xhr.send('id=%s');
        }""" % (obj, id, id, id)


    def ZOSIA_cost(self, obj):
        if obj.paid:
            return u"%s %s&nbsp;z\u0142" % ( self.yes_icon, obj.count_payment() )
        else:
            return u'<a href="#" onclick="{%s}">%s %s&nbsp;z\u0142</a> %s' % (
                    self.onclick(obj.id,obj), self.no_icon, obj.count_payment(), self.anim_icon(obj.id))
    ZOSIA_cost.allow_tags = True

    def bus_cost(self, obj):
        # if user doesn't wanna get but, so he shouldn't
        if not obj.bus:
            return "%s&nbsp;-" % self.no_icon
        elif obj.paid_for_bus:
            return u"%s %s&nbsp;z\u0142" % ( self.yes_icon, "40" )
        else:
            return u'<a href="#" onclick="{%s}">%s %s&nbsp;z\u0142</a>' % ( self.bus_onclick(obj), self.no_icon, "40" )
    bus_cost.allow_tags = True

    shirt_types = {}
    for i in 0,1:
        v = SHIRT_TYPES_CHOICES.__getitem__(i)
        shirt_types[v.__getitem__(0)] = v.__getitem__(1)
    def shirt(self, obj):
        return "%s (%s)" % (
                self.shirt_types[obj.shirt_type],
                obj.shirt_size)

    def f(self,o):
        def g(x):
            if o.__dict__[x]: return self.yes_icon
            else: return self.no_icon
        return g
    # note: these three methods should not be separated
    # but generated through lamba function
    # do it in spare time
    def breakfasts(self,obj):
        lst = ['breakfast_2', 'breakfast_3', 'breakfast_4']
        return "&nbsp;".join(map(self.f(obj),lst))
    breakfasts.allow_tags = True

    def dinners(self,obj):
        lst = ['dinner_1', 'dinner_2', 'dinner_3']
        return "&nbsp;".join(map(self.f(obj),lst))
    dinners.allow_tags = True

    def days(self,obj):
        lst = ['day_1', 'day_2', 'day_3']
        return "&nbsp;".join(map(self.f(obj),lst))
    days.allow_tags = True


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'accepted')

admin.site.unregister(Group)
admin.site.register(UserPreferences, UserPreferencesAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Participant, ParticipantAdmin)