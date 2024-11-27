from django.shortcuts import render, redirect
from .forms import EditProfileForm, EnrollSubjectsForm
from django.http import HttpResponseForbidden

from shared.decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

# Create your views here.
@login_required
def user_detail(request, username):
	user = get_user_model().objects.get(username=username)
	print(user.profile.role)
	return render(request, 'users/user_detail.html', {'other_user': user})

@login_required
def user_edit(request):
	user = get_user_model().objects.get(username=request.user.username)
	profile = user.profile
	form = EditProfileForm(request.POST or None, request.FILES or None, instance=profile)
	if form.is_valid():
		form.save()
		return redirect(profile.get_absolute_url())
	return render(request, 'users/user_edit.html', {'form': form})

@login_required
@student_required
def enroll_subjects(request):
	form = EnrollSubjectsForm()

	return render(request, 'users/enroll_subjects.html', {'form': form})