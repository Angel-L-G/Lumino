from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from shared.decorators import student_required, teacher_required

from .forms import EnrollSubjectsForm, LessonForm, UnenrollSubjectsForm


@login_required
def subject_list(request):
    if request.user.profile.is_teacher():
        return render(
            request,
            'subjects/subject_list.html',
            {'subjects': request.user.teaching_subjects.all()},
        )

    return render(
        request,
        'subjects/subject_list.html',
        {'subjects': request.user.enrolled_subjects.all()},
    )


@login_required
@student_required
def enroll_subjects(request):
    form = EnrollSubjectsForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subjects:subject-list')

    return render(
        request, 'subjects/subject_enrollment.html', {'form': form, 'action': 'Enroll in...'}
    )


@login_required
@student_required
def unenroll_subjects(request):
    form = UnenrollSubjectsForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subjects:subject-list')

    return render(
        request, 'subjects/subject_enrollment.html', {'form': form, 'action': 'Unenroll in...'}
    )


@login_required
def subject_detail(request, code):
    if request.user.profile.is_teacher():
        subject = request.user.teaching_subjects.get(code=code)
    else:
        subject = request.user.enrolled_subjects.get(code=code)

    return render(
        request,
        'subjects/subject_detail.html',
        {'subject': subject, 'mark': subject.get_mark(request.user)},
    )


@login_required
@teacher_required
def add_lesson(request, code):
    subject = request.user.teaching_subjects.get(code=code)
    if request.method == 'POST':
        form = LessonForm(subject, request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects:subject-detail', code=code)
    else:
        form = LessonForm()

    return render(request, 'subjects/lesson_form.html', {'form': form})
