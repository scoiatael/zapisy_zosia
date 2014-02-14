from django.contrib import admin
from committee.models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'value', 'text', 'user')
    list_filter = ['lecture__title', 'user']


admin.site.register(Vote, VoteAdmin)