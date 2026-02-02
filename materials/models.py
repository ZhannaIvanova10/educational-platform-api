from django.db import models
from django.conf import settings
from django.core.validators import URLValidator


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='Владелец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['id']  # ДОБАВЛЕНО: сортировка по умолчанию

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
        ordering = ['id']  # ДОБАВЛЕНО: сортировка по умолчанию

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='subscriptions', verbose_name='Курс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']
        ordering = ['-created_at']  # ДОБАВЛЕНО: сортировка по дате создания (новые сначала)

    def __str__(self):
        return f'{self.user} подписан на {self.course}'