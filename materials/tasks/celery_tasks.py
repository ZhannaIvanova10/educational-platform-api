import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from materials.models import Course, Subscription

logger = logging.getLogger(__name__)

@shared_task
def send_course_update_email(course_id, update_message=""):
    """
    Отправляет email всем подписчикам курса при его обновлении.
    
    ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: 
    Проверяет, что курс не обновлялся более 4 часов перед отправкой уведомлений.
    """
    try:
        course = Course.objects.get(id=course_id)
        
        # ✅ ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Проверка на 4 часа
        # Проверяем, когда курс был последний раз обновлен
        four_hours_ago = timezone.now() - timedelta(hours=4)
        
        if course.updated_at and course.updated_at > four_hours_ago:
            logger.info(f"Курс '{course.title}' был обновлен менее 4 часов назад. "
                       f"Последнее обновление: {course.updated_at}. "
                       f"Уведомления не отправляются.")
            return {
                'status': 'skipped',
                'reason': 'Course updated less than 4 hours ago',
                'course_id': course_id,
                'last_updated': course.updated_at.isoformat() if course.updated_at else None
            }
        
        # Получаем всех активных подписчиков курса
        subscriptions = Subscription.objects.filter(
            course=course,
            is_active=True
        ).select_related('user')
        
        if not subscriptions.exists():
            logger.info(f"У курса '{course.title}' нет активных подписчиков.")
            return {
                'status': 'no_subscribers',
                'course_id': course_id,
                'course_title': course.title
            }
        # Формируем email
        subject = f"Обновление курса: {course.title}"
        
        email_content = f"""
        Здравствуйте!
        
        Курс "{course.title}" был обновлен.
        
        {update_message if update_message else "В курс были внесены изменения."}
        
        Перейдите по ссылке, чтобы ознакомиться с изменениями:
        {settings.BASE_URL or 'http://localhost:8000'}/api/courses/{course.id}/
        
        С уважением,
        Команда образовательной платформы
        """
        
        # Отправляем письма всем подписчикам
        sent_count = 0
        for subscription in subscriptions:
            user = subscription.user
            if user.email:
                send_mail(
                    subject=subject,
                    message=email_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(f"Отправлено письмо об обновлении курса пользователю {user.email}")
        
        logger.info(f"Отправлено {sent_count} писем об обновлении курса '{course.title}'")
        
        return {
            'status': 'success',
            'sent_count': sent_count,
            'course_id': course_id,
            'course_title': course.title,
            'check_performed': True,  # ✅ Проверка на 4 часа выполнена
            'last_updated': course.updated_at.isoformat() if course.updated_at else None
        }
    except Course.DoesNotExist:
        logger.error(f"Курс с ID {course_id} не найден.")
        return {
            'status': 'error',
            'error': 'Course not found',
            'course_id': course_id
        }
    except Exception as e:
        logger.error(f"Ошибка при отправке email для курса {course_id}: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'course_id': course_id
        }
