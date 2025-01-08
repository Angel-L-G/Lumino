from django.core.management.base import BaseCommand

from subjects.models import Subject


class Command(BaseCommand):
    help = 'Gives the average mark for each subject.'

    def handle(self, *args, **options):
        subjects = Subject.objects.all()
        for subject in subjects:
            total = 0
            count = 0
            for enrollment in subject.enrollments.all().exclude(mark=None):
                total += enrollment.mark
                count += 1
            if count > 0:
                average = total / count
                self.stdout.write(f'{subject.code}: {average}')
            else:
                self.stdout.write(f'{subject.code}: No marks')
