from django import forms

from .models import Enrollment, Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control-file'}),
        }


class EnrollSubjectsForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['subject']
        widgets = {
            'subject': forms.CheckboxSelectMultiple,
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, *args, **kwargs):
        enrollment = super().save(commit=False)
        enrollment.student = self.user
        enrollment.subject = self.cleaned_data['subject']
        enrollment.save()
        return enrollment
