from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.user_edit, name='user-edit'),
    # path('certificate/', views.request_certificate, name='request-certificate'),
    # path('leave/', views.leave, name='leave'),
]
