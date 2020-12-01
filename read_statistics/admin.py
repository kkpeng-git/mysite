from django.contrib import admin

# Register your models here.
from read_statistics.models import ReadNum, ReadDetaill


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')


@admin.register(ReadDetaill)
class ReadDetaillAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')
