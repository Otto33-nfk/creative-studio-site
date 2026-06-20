import os
from django import forms
from .models import Article


ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок статьи'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Текст статьи'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'image': 'Изображение',
            'content': 'Текст статьи',
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