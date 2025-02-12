"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import accounts.views
import shared.views
import users.views

urlpatterns = [
    path('', shared.views.index, name='home'),
    path('admin/', admin.site.urls),
    path('login/', accounts.views.user_login, name='login'),
    path('logout/', accounts.views.user_logout, name='logout'),
    path('signup/', accounts.views.user_signup, name='signup'),
    path('users/<str:username>/', users.views.user_detail, name='user-detail'),
    path('user/', include('users.urls')),
    path('subjects/', include('subjects.urls')),
    path('setlang/<str:lang>/', shared.views.setlang, name='setlang'),
    path('__reload__/', include('django_browser_reload.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
