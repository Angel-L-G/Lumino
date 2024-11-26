from django.conf import settings
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='teching_subjects', on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_subjects',
        through='users.Enrollment',
    )

    def __str__(self):
        return self.code


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
