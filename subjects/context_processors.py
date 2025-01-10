from subjects.models import Subject


def subjects(request) -> dict:
    try:
        if not request.user.is_authenticated:
            return {}
        if request.user.is_teacher():
            return {'subjects': request.user.teaching_subjects.all()}

        return {'subjects': request.user.enrolled_subjects.all()}
    except Subject.DoesNotExist:
        return {}
