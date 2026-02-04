from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription
import logging

logger = logging.getLogger(__name__)


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
            return 'Нет активных подписчиков'
        
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
            return f'Отправлено {len(emails)} писем'
        else:
            logger.warning(f'Нет email адресов для отправки у подписчиков курса {course.title}')
            return 'Нет email адресов'
            
    except Course.DoesNotExist:
        logger.error(f'Курс с ID {course_id} не найден')
        return 'Курс не найден'
    except Exception as e:
        logger.error(f'Ошибка при отправке email: {e}')
        return f'Ошибка: {str(e)}'
