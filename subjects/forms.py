from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Div, Field, Row, Submit
from django import forms
from django.core.exceptions import ValidationError

from .models import Enrollment, Lesson, Subject


class EnrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
            pk__in=user.enrolled_subjects.all()
        )

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_show_labels = False
        self.helper.form_class = 'd-flex flex-column form-controll'
        self.helper.layout = Layout(
            Field('subjects'),
            Div(
                Submit('save', 'Enroll', css_class='btn btn-primary w-75 mt-2 mb-2'),
                css_class='d-flex justify-content-center',
            ),
        )

    def save(self, *args, **kwargs):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            self.user.enrolled_subjects.add(subject)
        return subjects


class UnenrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['subjects'].queryset = user.enrolled_subjects.all()

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_show_labels = False
        self.helper.form_class = 'd-flex flex-column form-controll'
        self.helper.layout = Layout(
            Field('subjects'),
            Div(
                Submit('save', 'Unenroll', css_class='btn btn-primary w-75 mt-2 mb-2'),
                css_class='d-flex justify-content-center',
            ),
        )

    def save(self, *args, **kwargs):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            self.user.enrolled_subjects.remove(subject)
        return subjects


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subject = subject

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_show_labels = False
        self.helper.form_class = 'd-flex flex-column form-controll'
        self.helper.layout = Layout(
            FloatingField('title'),
            HTML('<label>Content</label>'),
            Field('content'),
            Div(
                Submit('add', 'Add', css_class='btn btn-primary w-75 mt-2 mb-2'),
                css_class='d-flex justify-content-center',
            ),
        )

    def save(self, *args, **kwargs):
        lesson = super().save(commit=False)
        lesson.subject = self.subject
        return lesson.save()


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subject = subject

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_show_labels = False
        self.helper.form_class = 'd-flex flex-column form-controll'
        self.helper.layout = Layout(
            FloatingField('title'),
            HTML('<label>Content</label>'),
            Field('content'),
            Div(
                Submit('edit', 'Edit', css_class='btn btn-primary w-75 mt-2 mb-2'),
                HTML(
                    '<a href="{{lesson.get_absolute_url}}" class="btn btn-danger w-75 mt-2 mb-2">Cancel</a>'
                ),
                css_class='d-flex justify-content-center',
            ),
        )

    def save(self, *args, **kwargs):
        lesson = super().save(commit=False)
        lesson.subject = self.subject
        return lesson.save()


class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mark']

    def clean_mark(self):
        mark = self.cleaned_data['mark']
        if mark >= 10 or mark <= 0:
            raise ValidationError('The mark must be between 0 and 10')
        return mark


class EditMarkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                HTML(
                    '{% load subject_extras %} <div class="col-md-2">{% student_label formset forloop.counter0 %}</div>'
                ),
                Field('mark', wrapper_class='col-md-2'),
                css_class='align-items-baseline',
            )
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))
