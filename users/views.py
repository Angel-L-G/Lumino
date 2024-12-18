from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from shared.decorators import student_required

from .forms import EditProfileForm


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
def leave(request):
    get_user_model().objects.get(username=request.user.username).delete()
    logout(request)
    return redirect('home')
