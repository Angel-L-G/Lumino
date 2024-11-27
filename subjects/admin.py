from django.contrib import admin

# Register your models here.

from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ['name', 'code', 'teacher',]