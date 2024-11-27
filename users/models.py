from django.conf import settings
from django.db import models
from django.urls import reverse


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
    
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.user.username})


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.DO_NOTHING
    )
    subject = models.ForeignKey(
        'subjects.Subject', related_name='enrollments', on_delete=models.DO_NOTHING
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f'{self.student} enrolled in {self.subject}'
