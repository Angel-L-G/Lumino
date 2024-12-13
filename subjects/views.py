from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from shared.decorators import student_required, subject_owner_required, teacher_required

from .forms import (
    AddLessonForm,
    EditLessonForm,
    EnrollSubjectsForm,
    UnenrollSubjectsForm,
)


@login_required
def subject_list(request):
    if request.user.is_teacher():
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
    if request.user.is_teacher():
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
        form = AddLessonForm(subject, request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects:subject-detail', code=code)
    else:
        form = AddLessonForm(subject)

    return render(request, 'subjects/lessons/add_lesson.html', {'form': form})


@login_required
def lesson_detail(request, code, pk):
    subject = request.user.teaching_subjects.get(code=code)
    lesson = subject.lessons.get(pk=pk)
    return render(
        request, 'subjects/lessons/lesson_detail.html', {'lesson': lesson, 'subject': subject}
    )


@login_required
@teacher_required
def edit_lesson(request, code, pk):
    subject = request.user.teaching_subjects.get(code=code)
    lesson = subject.lessons.get(pk=pk)
    if request.method == 'POST':
        form = EditLessonForm(subject, request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('subjects:lesson-detail', code=code, pk=pk)
    else:
        form = EditLessonForm(subject, instance=lesson)

    return render(request, 'subjects/lessons/edit_lesson.html', {'form': form})


@login_required
@teacher_required
def delete_lesson(request, code, pk):
    subject = request.user.teaching_subjects.get(code=code)
    lesson = subject.lessons.get(pk=pk)
    lesson.delete()
    return redirect('subjects:subject-detail', code=code)


@login_required
@subject_owner_required
def mark_list(request, code):
    subject = request.user.teaching_subjects.get(code=code)
    enrollments = subject.enrollments.all()
    student_dict = {enrollment.student: enrollment.mark for enrollment in enrollments}
    return render(
        request, 'marks/mark_list.html', {'subject': subject, 'student_dict': student_dict}
    )


# @login_required
# @subject_owner_required
def edit_marks(request, code):
    pass
    # subject = request.user.teaching_subjects.get(code=code)
    # form = EditMarkForm(subject.enrollments.all(), request.POST or None)
    # helper = EditMarkFormSetHelper()
    # if request.method == 'POST':
    #     return redirect('subjects:mark-list', code=code)

    # return render(
    #     request, 'marks/edit_marks.html', {'subject': subject, 'formset': form, 'helper': helper}
    # )
