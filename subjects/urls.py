from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('<str:code>/', views.subject_detail, name='subject-detail'),
    path('<str:code>/lessons/', lambda _: redirect('subjects:subject-detail')),
    path('<str:code>/lessons/add/', views.add_lesson, name='add-lesson'),
]
