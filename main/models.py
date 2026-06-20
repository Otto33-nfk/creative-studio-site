from django.db import models
from django.contrib.auth.models import User


class PortfolioProject(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(
        upload_to='portfolio/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    short_description = models.CharField(
        max_length=300,
        verbose_name='Краткое описание'
    )
    full_description = models.TextField(
        blank=True,
        verbose_name='Полное описание'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProjectLike(models.Model):
    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Проект'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_likes',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк проекта'
        verbose_name_plural = 'Лайки проектов'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_like'
            )
        ]

    def __str__(self):
        return f'{self.user.username} лайкнул {self.project.title}'


class ProjectComment(models.Model):
    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Проект'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий к проекту'
        verbose_name_plural = 'Комментарии к проектам'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username} — {self.project.title}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=150, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Сообщение с сайта'
        verbose_name_plural = 'Сообщения с сайта'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'