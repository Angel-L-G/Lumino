from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from shared.decorators import (
    all_marks_required,
    student_required,
    subject_owner_required,
    user_has_subject,
)

from .forms import (
    AddLessonForm,
    EditLessonForm,
    EditMarkForm,
    EditMarkFormSetHelper,
    EnrollSubjectsForm,
    UnenrollSubjectsForm,
)
from .models import Enrollment, Subject
from .tasks import deliver_certificate


@login_required
def subject_list(request):
    if request.user.is_teacher():
        return render(
            request,
            'subjects/subject_list.html',
        )

    cases = 0
    if request.user.enrolled.count() <= 0:
        cases = 1
    elif request.user.enrolled.count() == Subject.objects.count():
        cases = 2

    return render(
        request,
        'subjects/subject_list.html',
        {
            'cases': cases,
            'all_marks_assigned': request.user.enrolled.filter(enrollments__mark=None).count() <= 0,
        },
    )


@login_required
@student_required
def enroll_subjects(request):
    form = EnrollSubjectsForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        messages.add_message(
            request, messages.SUCCESS, 'Successfully enrolled in the chosen subjects.'
        )
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
        messages.add_message(
            request, messages.SUCCESS, 'Successfully unenrolled from the chosen subjects.'
        )
        return redirect('subjects:subject-list')

    return render(
        request, 'subjects/subject_enrollment.html', {'form': form, 'action': 'Unenroll in...'}
    )


@login_required
@user_has_subject
def subject_detail(request, code):
    if request.user.is_teacher():
        subject = request.user.teaching_subjects.get(code=code)
    else:
        subject = request.user.enrolled.get(code=code)

    return render(
        request,
        'subjects/subject_detail.html',
        {'subject': subject, 'mark': subject.get_mark(request.user)},
    )


@login_required
@subject_owner_required
def add_lesson(request, code):
    subject = request.user.teaching_subjects.get(code=code)
    if request.method == 'POST':
        form = AddLessonForm(subject, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Lesson was successfully added.')
            return redirect('subjects:subject-detail', code=code)
    else:
        form = AddLessonForm(subject)

    return render(request, 'subjects/lessons/add_lesson.html', {'form': form})


@login_required
@user_has_subject
def lesson_detail(request, code, pk):
    subject = None
    if request.user.is_teacher():
        subject = request.user.teaching_subjects.get(code=code)
    else:
        subject = request.user.enrolled.get(code=code)
    lesson = subject.lessons.get(pk=pk)
    return render(
        request, 'subjects/lessons/lesson_detail.html', {'lesson': lesson, 'subject': subject}
    )


@login_required
@subject_owner_required
def edit_lesson(request, code, pk):
    subject = request.user.teaching_subjects.get(code=code)
    lesson = subject.lessons.get(pk=pk)
    if request.method == 'POST':
        form = EditLessonForm(subject, request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Changes were successfully saved.')
            return render(request, 'subjects/lessons/edit_lesson.html', {'form': form})
    else:
        form = EditLessonForm(subject, instance=lesson)

    return render(request, 'subjects/lessons/edit_lesson.html', {'form': form})


@login_required
@subject_owner_required
def delete_lesson(request, code, pk):
    subject = request.user.teaching_subjects.get(code=code)
    lesson = subject.lessons.get(pk=pk)
    lesson.delete()
    messages.add_message(request, messages.SUCCESS, 'Lesson was successfully deleted.')
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


@login_required
@subject_owner_required
def edit_marks(request, code: str):
    subject = Subject.objects.get(code=code)

    # breadcrumbs = Breadcrumbs()
    # breadcrumbs.add('My subjects', reverse('subjects:subject-list'))
    # breadcrumbs.add(subject.code, reverse('subjects:subject-detail', args=[subject.code]))
    # breadcrumbs.add('Marks', reverse('subjects:mark-list', args=[subject.code]))
    # breadcrumbs.add('Edit marks')

    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrollments.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.add_message(request, messages.SUCCESS, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit-marks', kwargs={'code': code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarkFormSetHelper()
    return render(
        request,
        'marks/edit_marks.html',
        dict(subject=subject, formset=formset, helper=helper),  # breadcrumbs=breadcrumbs),
    )


@login_required
@all_marks_required
def certificate(request):
    deliver_certificate.delay(request.build_absolute_uri(''), request.user)
    messages.add_message(
        request,
        messages.SUCCESS,
        f'You will get the grade certificate quite soon at ${request.user.email}.',
    )
    return render(request, 'certificates/certificate_feedback.html')
