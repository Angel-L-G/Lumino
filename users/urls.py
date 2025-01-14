from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.edit_profile, name='user-edit'),
    path('leave/', views.leave, name='leave'),
    path('reset_image/', views.reset_image, name='reset-image'),
]
