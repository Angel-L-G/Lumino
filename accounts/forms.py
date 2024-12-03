from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from users.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            Div(
                Submit('login', 'Login', css_class='btn btn-primary w-75 mt-2 mb-2'),
                HTML(
                    '<a href="{% url \'signup\' %}" class="mt-3">¿No tienes cuenta? Regístrate aquí</a>'
                ),
                css_class='d-flex flex-column align-items-center',
            ),
        )


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        required_fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = dict(password=forms.PasswordInput)
        help_texts = dict(username=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required_fields:
            self.fields[field].required = True

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            Div(
                FloatingField('first_name'),
                FloatingField('last_name'),
                css_class='d-flex gap-1',
            ),
            FloatingField('email'),
            Div(
                Submit('signup', 'Register', css_class='btn btn-primary w-75 mt-2 mb-2'),
                HTML(
                    '<a href="{% url \'login\' %}" class="mt-3">¿Ya tienes cuenta? Inicia sesión aquí</a>'
                ),
                css_class='d-flex flex-column align-items-center',
            ),
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if self._meta.model.objects.filter(email=email).count() > 0:
            raise ValidationError('A user with that email already exists.')
        return email

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        Profile.objects.create(user=user)
        return user
