from django import forms
from .models import Profile
from subjects.models import Subject

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'avatar']
		widgets = {
			'bio': forms.Textarea(attrs={'rows': 3, 'class':'form-control'}),
			'avatar': forms.FileInput(attrs={'accept': 'image/*', 'class':'form-control-file'}),
		}

class EnrollSubjectsForm(forms.Form):
	subjects = forms.ModelMultipleChoiceField(
		queryset=Subject.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		label='Subjects',
	)

	def __init__(self, *args, **kwargs):
		subjects = kwargs.pop('subjects')
		super().__init__(*args, **kwargs)
		self.fields['subjects'].queryset = subjects