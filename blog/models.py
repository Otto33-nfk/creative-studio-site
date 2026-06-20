from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')

    image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    content = models.TextField(verbose_name='Содержание')

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    views = models.PositiveIntegerField(
        default=0,
        verbose_name='Просмотры'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ArticleLike(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Статья'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='article_likes',
        verbose_name='Пользователь'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк статьи'
        verbose_name_plural = 'Лайки статей'
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'user'],
                name='unique_article_like'
            )
        ]

    def __str__(self):
        return f'{self.user.username} лайкнул {self.article.title}'


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    text = models.TextField(verbose_name='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username} — {self.article.title}'