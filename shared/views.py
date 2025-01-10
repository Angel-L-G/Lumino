from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import translation

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('subjects:subject-list')

    return render(request, 'homepage.html')


def setlang(request, lang):
    next = request.GET.get('next', '/')
    translation.activate(lang)
    response = redirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
