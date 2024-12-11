from django.conf import settings
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='teaching_subjects', on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_subjects',
        through='Enrollment',
    )

    def get_mark(self, user):
        if user.is_teacher():
            return None
        return self.enrollments.get(student=user).mark or None

    def __str__(self):
        return self.code


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


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
