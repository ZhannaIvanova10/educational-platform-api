from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from materials.models import Course, Subscription
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_course_update_email(course_id, update_message):
    """
    Отправка email подписчикам курса об обновлении
    
    Args:
        course_id (int): ID курса
        update_message (str): Сообщение об обновлении
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        
        if not subscriptions.exists():
            logger.info(f'Нет активных подписчиков для курса {course.title}')
            return
        
        subject = f'Обновление курса: {course.title}'
        message = f'''
        Здравствуйте!
        
        Курс "{course.title}" был обновлен.
        
        {update_message}
        
        Перейдите по ссылке, чтобы ознакомиться с изменениями:
        http://localhost:8000/api/courses/{course.id}/
        
        С уважением,
        Команда образовательной платформы
        '''
        emails = [sub.user.email for sub in subscriptions if sub.user.email]
        
        if emails:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )
            logger.info(f'Отправлено {len(emails)} писем об обновлении курса {course.title}')
        else:
            logger.warning(f'Нет email адресов для отправки у подписчиков курса {course.title}')
            
    except Course.DoesNotExist:
        logger.error(f'Курс с ID {course_id} не найден')
    except Exception as e:
        logger.error(f'Ошибка при отправке email: {e}')


@shared_task
def check_inactive_users():
    """
    Проверка неактивных пользователей и их блокировка
    Пользователь блокируется, если не заходил более 30 дней
    """
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Находим активных пользователей, которые не заходили более 30 дней
        inactive_users = User.objects.filter(
            last_login__lt=thirty_days_ago,
            is_active=True
        ).exclude(is_superuser=True)  # Не блокируем суперпользователей
        
        count = inactive_users.count()
        
        if count > 0:
            # Блокируем пользователей
            inactive_users.update(is_active=False)
            # Логируем действие
            user_emails = list(inactive_users.values_list('email', flat=True))
            logger.info(f'Заблокировано {count} неактивных пользователей: {user_emails}')
            
            # Отправляем уведомление администратору (опционально)
            try:
                send_mail(
                    subject=f'Заблокировано {count} неактивных пользователей',
                    message=f'Были заблокированы пользователи, которые не заходили более 30 дней.\n\nЗаблокированные email: {", ".join(user_emails)}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass  # Игнорируем ошибки отправки email
            
            return f'Заблокировано {count} пользователей'
        else:
            logger.info('Нет неактивных пользователей для блокировки')
            return 'Нет неактивных пользователей'
            
    except Exception as e:
        logger.error(f'Ошибка при проверке неактивных пользователей: {e}')
        raise


@shared_task
def send_welcome_email(user_id):
    """
    Отправка приветственного письма новому пользователю
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Добро пожаловать на образовательную платформу!'
        message = f'''
        Здравствуйте, {user.email}!
        
        Добро пожаловать на нашу образовательную платформу!
        
        Теперь вы можете:
        1. Просматривать доступные курсы
        2. Подписываться на интересующие курсы
        3. Получать уведомления об обновлениях
        4. Оплачивать курсы через безопасную платежную систему
        
        Начните свое обучение прямо сейчас:
        http://localhost:8000/api/courses/
        
        С уважением,
        Команда образовательной платформы
        '''
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f'Отправлено приветственное письмо пользователю {user.email}')
        
    except User.DoesNotExist:
        logger.error(f'Пользователь с ID {user_id} не найден')
    except Exception as e:
        logger.error(f'Ошибка при отправке приветственного письма: {e}')
