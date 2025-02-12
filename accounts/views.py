from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import LoginForm, SignupForm

# Create your views here.


def user_login(request):
    FALLBACK_REDIRECT = reverse('home')

    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)

    login_error = False
    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            if next:
                return redirect(next)
            return redirect('home')
        else:
            form = LoginForm()
            login_error = True
    else:
        next = request.GET.get('next', FALLBACK_REDIRECT)
        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        dict(
            form=form,
            next=next,
            login_error=login_error,
        ),
    )


def user_logout(request):
    logout(request)
    return redirect('home')


def user_signup(request):
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome to Lumino. Nice to see you!.')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', dict(form=form))
