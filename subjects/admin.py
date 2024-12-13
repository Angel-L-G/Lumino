from django.contrib import admin

# Register your models here.
from .models import Enrollment, Lesson, Subject


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


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'title',
    ]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'student',
        'mark',
    ]
