from django.db import models
from django.conf import settings
from django.core.validators import URLValidator


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='Владелец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['id']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание')
    video_link = models.URLField(verbose_name='Ссылка на видео',
                                 validators=[URLValidator()])
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='lessons', verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='Владелец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']

    def __str__(self):
        return self.title

class Subscription(models.Model):
    """Модель подписки на обновления курса"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return f'{self.user.email if hasattr(self.user, "email") else self.user_id} -> {self.course.title}'
