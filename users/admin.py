# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.utils.encoding import smart_text
from .models import UserPreferences, SHIRT_TYPES_CHOICES, Organization, Participant, Waiting


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email')


class RoomsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'posiada pokój'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'room'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Yes', 'Tak'),
            ('No', 'Nie'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'Yes':
            return queryset.annotate(num_rooms=Count('user__userinroom')).filter(num_rooms=1)
        if self.value() == 'No':
            return queryset.annotate(num_rooms=Count('user__userinroom')).filter(num_rooms=0)


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
        'minutes_early', 'date_joined',
    'last_login')
    list_filter = ['bus_hour', 'paid', 'bus', 'want_bus', RoomsFilter, 'breakfast_2', 'breakfast_3',
                   'breakfast_4', 'dinner_1', 'dinner_2', 'dinner_3', 'day_1', 'day_2', 'day_3', 'shirt_size', 'shirt_type', 'org']
    list_editable = ('minutes_early', 'paid')
    list_select_related = ('user',)

    def user_name(self, item):
        return smart_text(item.user.get_full_name())

    def user_email(self, item):
        return str(item.user.email)

    def date_joined(self, obj):
        return obj.user.date_joined
    date_joined.short_description = 'date_joined'
    date_joined.admin_order_field = 'user__date_joined'

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = 'last_login'
    last_login.admin_order_field = 'user__last_login'

    def anim_icon(self,id):
        return '<img src="/static/images/macthrob-small.png" alt="loading" id="anim%s" style="display:none"/>'%id
    yes_icon = '<img src="/static/images/icon-yes.gif" alt="Yes" />'
    no_icon  = '<img src="/static/images/icon-no.gif" alt="No" />'
    def onclick(self,id,obj):
        return """if(confirm('Do you want to register payment from %s?')) {
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
        return """if(confirm('Do you want to register transport payment from %s?')) {
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
            return "%s %s&nbsp;z\u0142" % ( self.yes_icon, obj.count_payment() )
        else:
            return '<a href="#" onclick="{%s}">%s %s&nbsp;z\u0142</a> %s' % (
                    self.onclick(obj.id,obj), self.no_icon, obj.count_payment(), self.anim_icon(obj.id))
    ZOSIA_cost.allow_tags = True

    def bus_cost(self, obj):
        # if user doesn't wanna get but, so he shouldn't
        if not obj.bus:
            return "%s&nbsp;-" % self.no_icon
        elif obj.paid_for_bus:
            return "%s %s&nbsp;z\u0142" % ( self.yes_icon, "40" )
        else:
            return '<a href="#" onclick="{%s}">%s %s&nbsp;z\u0142</a>' % ( self.bus_onclick(obj), self.no_icon, "40" )
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

class WaitingAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_1', 'day_2', 'day_3')

admin.site.unregister(Group)
admin.site.register(Waiting, WaitingAdmin)
admin.site.register(UserPreferences, UserPreferencesAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Participant, ParticipantAdmin)
