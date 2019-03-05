from django.contrib import admin
from polls.models import Question, Choice

# Register your models here.

#class ChoiceInline(admin.StackedInline):									# 1
class ChoiceInline(admin.TabularInline):									# 2
    model = Choice
    extra = 2
    
class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']									# 3
    fieldsets = [													        # 4
        (None, {'fields': ['question_text']}),
        #('Date Information', {'fields':['pub_date']}),
        ('Date Information', {'fields':['pub_date'], 'classes':['collapse']}), # 5
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')							# 6
    list_filter = ['pub_date']											   # 7
    search_fields = ['question_text']									   # 8

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)