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
            'bio': forms.Textarea(attrs={'rows': 3, 'cols': 4, 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True, enctype='multipart/form-data')
        self.helper.form_class = 'w-100 h-100'
        self.helper.layout = Layout(
            FloatingField('bio', css_class='mb-3 h-100'),
            Div(
                HTML('{% include "users/include/avatar.html" with user=user size="30x30" %}'),
                Field('avatar'),
                css_class='d-flex align-items-center gap-3',
            ),
            Div(
                Submit('save', 'Save', css_class='btn btn-primary w-75 mt-2 mb-2'),
                HTML(
                    '<a class="btn btn-danger w-75 mt-2 mb-2" href="{{ user.profile.get_absolute_url }}">Cancel</a>'
                ),
                css_class='d-flex flex-column align-items-center',
            ),
        )
