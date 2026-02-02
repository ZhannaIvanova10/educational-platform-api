from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User без username"""

    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с email и паролем"""
        if not email:
            raise ValueError('Пользователь должен иметь email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя с авторизацией по email"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Упрощенная модель платежей с IntegerField для избежания циклических зависимостей"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')

    # Используем IntegerField вместо ForeignKey чтобы избежать циклических зависимостей
    course_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='ID курса')
    lesson_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='ID урока')

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

    @property
    def course(self):
        """Получаем объект курса если course_id указан"""
        if self.course_id:
            try:
                from materials.models import Course
                return Course.objects.get(id=self.course_id)
            except:
                return None
        return None

    @property
    def lesson(self):
        """Получаем объект урока если lesson_id указан"""
        if self.lesson_id:
            try:
                from materials.models import Lesson
                return Lesson.objects.get(id=self.lesson_id)
            except:
                return None
        return None