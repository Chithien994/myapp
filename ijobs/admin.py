import os
import pytz

from datetime import date, datetime, time
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import IJob

# Register your models here.
class IjobAdmin(admin.ModelAdmin):
    # ...
	list_display = ('__str__', 'name', 'content')
	list_filter = ['user__email', 'begin_date', 'end_date']
	search_fields = ['name', 'content']

admin.site.register(IJob, IjobAdmin)
