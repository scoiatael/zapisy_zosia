from django.contrib import admin

from .models import Agenda

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    pass
