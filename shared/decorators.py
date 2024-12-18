from django.http import HttpResponseForbidden

from subjects.models import Subject


def student_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_teacher():
            return HttpResponseForbidden('Only students allowed.')
        return func(request, *args, **kwargs)

    return wrapper


def teacher_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_teacher():
            return HttpResponseForbidden('Only teachers allowed.')
        return func(request, *args, **kwargs)

    return wrapper


def subject_owner_required(func):
    def wrapper(request, code, *args, **kwargs):
        subject = Subject.objects.get(code=code)
        if request.user.is_teacher() and subject.teacher != request.user:
            return HttpResponseForbidden('Only the subject owner can perform this action.')
        return func(request, code, *args, **kwargs)

    return wrapper


def all_marks_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.enrollments.filter(mark=None).count() > 0 or request.user.is_teacher():
            return HttpResponseForbidden('You do not have all the marks assigned.')
        return func(request, *args, **kwargs)

    return wrapper
