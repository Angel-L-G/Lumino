from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Div, Field, Submit
from django import forms

from .models import Profile


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
