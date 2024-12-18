from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.user_edit, name='user-edit'),
    path('leave/', views.leave, name='leave'),
]
