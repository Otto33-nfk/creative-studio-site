from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'city', 'about']
        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'background: #334155; color: #e2e8f0; border-color: #475569;'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': 'background: #334155; color: #e2e8f0; border-color: #475569;'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'background: #334155; color: #e2e8f0; border-color: #475569;'
            }),
        }
        labels = {
            'avatar': 'Аватар',
            'city': 'Город',
            'about': 'О себе',
        }