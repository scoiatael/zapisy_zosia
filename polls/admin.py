# -*- coding: UTF-8 -*-
from django.contrib import admin
from polls.models import Poll, Question, UserAnswer


class PollAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'question', 'votes')
    list_filter = ['poll__title']

    def votes(self, item):
        return UserAnswer.objects.filter(question=item).count()


class UserAnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)