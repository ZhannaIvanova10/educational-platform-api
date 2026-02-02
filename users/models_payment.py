from django.db import models
from django.conf import settings


class Payment(models.Model):
    """Модель платежей"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    
    # Временно убираем ForeignKey, добавим их позже
    course_id = models.IntegerField(null=True, blank=True, verbose_name='ID курса')
    lesson_id = models.IntegerField(null=True, blank=True, verbose_name='ID урока')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты'
    )
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f'{self.user} - {self.amount} - {self.payment_date}'
