from django.conf import settings
from django.db import models


class Profile(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    ROLE_CHOICES = {
        STUDENT: 'Student',
        TEACHER: 'Teacher',
    }
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=STUDENT)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return self.user.username


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.DO_NOTHING
    )
    subject = models.ForeignKey(
        'subjects.Subject', related_name='enrollments', on_delete=models.DO_NOTHING
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.student} enrolled in {self.subject}'
