from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок статьи'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Текст статьи'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'image': 'Изображение',
            'content': 'Текст статьи',
        }