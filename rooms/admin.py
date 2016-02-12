from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *


class NewroomsAdmin(ImportExportModelAdmin):
    list_display = ['number','capacity','locators']
    resource_class = RoomResource

    def locators(self,obj):
        return ",".join([])

admin.site.register(Room, NewroomsAdmin)


class UserInRoomAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname','room']

admin.site.register(UserInRoom, UserInRoomAdmin)
