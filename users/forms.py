from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Div, Field, Submit
from django import forms

from subjects.models import Subject

from .models import Enrollment, Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True, enctype='multipart/form-data')
        self.helper.layout = Layout(
            FloatingField('bio'),
            Field('avatar'),
            Div(
                Submit('save', 'Save', css_class='btn btn-primary w-75 mt-2 mb-2'),
                HTML('<a href="{{ user.profile.get_absolute_url }}">Cancel</a>'),
                css_class='d-flex flex-column align-items-center',
            ),
        )


class EnrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        enrolls = Enrollment.objects.filter(student=user)
        enrolled_subject_ids = enrolls.values_list('subject_id')
        self.fields['subjects'].queryset = Subject.objects.exclude(id__in=enrolled_subject_ids)

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_class = 'd-flex flex-column form-controll'
        self.helper.layout = Layout(
            Field('subjects'),
            Div(
                Submit('save', 'Save', css_class='btn btn-primary w-75 mt-2 mb-2'),
                css_class='d-flex justify-content-center',
            ),
        )

    def save(self, *args, **kwargs):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            Enrollment.objects.create(student=self.user, subject=subject)
