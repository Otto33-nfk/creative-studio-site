from django.db import models
from django.contrib.auth.models import User


class PortfolioProject(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True, verbose_name='Изображение')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    full_description = models.TextField(blank=True, verbose_name='Полное описание')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title