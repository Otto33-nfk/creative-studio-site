import os
from django import forms
from django.contrib.auth.models import User
from .models import Profile


ALLOWED_AVATAR_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.ru'
            }),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'city', 'about']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш город'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите немного о себе'
            }),
        }
        labels = {
            'avatar': 'Аватар',
            'city': 'Город',
            'about': 'О себе',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            ext = os.path.splitext(avatar.name)[1].lower()

            if ext not in ALLOWED_AVATAR_EXTENSIONS:
                raise forms.ValidationError(
                    'Можно загружать только JPG, PNG или WEBP. GIF для аватара запрещён.'
                )

            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    'Аватар слишком большой. Максимальный размер — 2 МБ.'
                )

        return avatar