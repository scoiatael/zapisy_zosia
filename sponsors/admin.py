# -*- coding: UTF-8 -*-

from django.contrib import admin
from .models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Sponsor, SponsorAdmin)