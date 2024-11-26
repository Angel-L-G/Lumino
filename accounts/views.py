from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

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
            return redirect(next)
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


def signup(request):
    pass
