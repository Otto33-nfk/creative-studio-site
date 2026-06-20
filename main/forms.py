from django import forms
from .models import PortfolioProject


class ProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'image', 'short_description', 'full_description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название проекта'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Подробное описание проекта'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Название',
            'image': 'Изображение',
            'short_description': 'Краткое описание',
            'full_description': 'Полное описание',
        }