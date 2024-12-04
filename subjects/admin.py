from django.contrib import admin

# Register your models here.
from .models import Enrollment, Subject


class EnrollmentInline(admin.StackedInline):
    model = Enrollment
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'code',
        'teacher',
    ]
    inlines = [EnrollmentInline]
