from django.http import HttpResponseForbidden

from subjects.models import Subject

def student_required(func):
	def wrapper(request, *args, **kwargs):
		if request.user.profile.is_teacher():
			return HttpResponseForbidden('Only students allowed.')
		return func(*args, **kwargs)
	return wrapper

def teacher_required(func):
	def wrapper(request, *args, **kwargs):
		if not request.user.profile.is_teacher():
			return HttpResponseForbidden('Only teachers allowed.')
		return func(*args, **kwargs)
	return wrapper

def subject_owner_required(func):
	def wrapper(request, code, *args, **kwargs):
		subject = Subject.objects.get(code=code)
		if request.user.profile.is_teacher() and subject.teacher != request.user:
			return HttpResponseForbidden('Only the subject owner can perform this action.')
		return func(*args, **kwargs)
	return wrapper