import os
from django import forms
from .models import PortfolioProject, ContactMessage


ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'image', 'short_description', 'full_description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название проекта'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание проекта'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Подробное описание проекта'
            }),
        }
        labels = {
            'title': 'Название',
            'image': 'Изображение',
            'short_description': 'Краткое описание',
            'full_description': 'Полное описание',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError(
                    'Можно загружать только JPG, PNG или WEBP. GIF не поддерживается.'
                )

            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Файл слишком большой. Максимальный размер изображения — 5 МБ.'
                )

        return image


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.ru'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема обращения'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Расскажите о вашей задаче...'
            }),
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Email',
            'subject': 'Тема',
            'message': 'Сообщение',
        }