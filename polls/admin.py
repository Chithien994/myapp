from django.contrib import admin

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('__str__', 'question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)