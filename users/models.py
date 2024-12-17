from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def is_teacher(self):
    return self.profile.role == Profile.Role.TEACHER


User.add_to_class('is_teacher', is_teacher)


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    role = models.CharField(max_length=1, choices=Role, default=Role.STUDENT)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/noavatar.png')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'username': self.user.username})
