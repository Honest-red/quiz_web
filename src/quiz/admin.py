from django.contrib import admin

from .forms import ChoicesInlineFormset
from .forms import QuestionInlineFormset
from .models import Choice
from .models import Exam
from .models import Question
from .models import Result


class ChoicesInline(admin.TabularInline):
    model = Choice
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0
    formset = ChoicesInlineFormset


class ListChoice(admin.ModelAdmin):
    list_display = [
        'question',
        'text',
        'is_correct'
        ]


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoicesInline, )


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_num')
    show_change_link = True
    extra = 0
    ordering = ('order_num', )
    formset = QuestionInlineFormset


class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid']
    inlines = (QuestionInline, )


admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ListChoice)
admin.site.register(Result)
