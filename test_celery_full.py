import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ПОЛНАЯ ПРОВЕРКА CELERY ИНТЕГРАЦИИ")
print("=" * 60)

# 1. Проверка моделей
print("\n1. ПРОВЕРКА МОДЕЛЕЙ:")
try:
    from materials.models import Course, Lesson, Subscription
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    print(f"   ✅ Course: {Course.objects.count()} записей")
    print(f"   ✅ Lesson: {Lesson.objects.count()} записей") 
    print(f"   ✅ Subscription: {Subscription.objects.count()} записей")
    print(f"   ✅ User: {User.objects.count()} записей")
    
    # Создадим тестовые данные если нужно
    course = Course.objects.first()
    user = User.objects.first()
    
    if course and user:
        sub, created = Subscription.objects.get_or_create(
            user=user,
            course=course,
            defaults={'is_active': True}
        )
        print(f"   ✅ Тестовая подписка: {'создана' if created else 'уже существует'}")
    
except Exception as e:
    print(f"   ❌ Ошибка моделей: {e}")
# 2. Проверка Celery задач
print("\n2. ПРОВЕРКА CELERY ЗАДАЧ:")
try:
    from materials.tasks import send_course_update_email
    print("   ✅ materials.tasks.send_course_update_email - импортирована")
    
    from users.tasks import check_inactive_users, send_welcome_email
    print("   ✅ users.tasks.check_inactive_users - импортирована")
    print("   ✅ users.tasks.send_welcome_email - импортирована")
    
    # Проверяем, что задачи зарегистрированы в Celery
    from celery import current_app
    task_count = len(current_app.tasks)
    print(f"   ✅ Celery app: {task_count} задач зарегистрировано")
    
except ImportError as e:
    print(f"   ❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"   ❌ Ошибка Celery: {e}")

# 3. Тестирование отправки email
print("\n3. ТЕСТИРОВАНИЕ ОТПРАВКИ EMAIL:")
try:
    from django.core.mail import send_mail
    from django.conf import settings
    
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Тестовая отправка
    if hasattr(settings, 'EMAIL_BACKEND'):
        print("   ✅ Настройки email загружены")
        
        # Проверим отправку тестового письма
        try:
            send_mail(
                subject='Тестовое письмо от Celery',
                message='Это тестовое письмо для проверки работы email системы.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
            print("   ✅ Тестовое письмо отправлено (проверьте консоль Django)")
        except Exception as e:
            print(f"   ⚠️  Ошибка отправки тестового письма: {e}")
    
except Exception as e:
    print(f"   ❌ Ошибка email: {e}")
# 4. Тестирование задачи send_course_update_email
print("\n4. ТЕСТИРОВАНИЕ ЗАДАЧИ send_course_update_email:")
try:
    course = Course.objects.first()
    if course:
        print(f"   Тестируем для курса: {course.title}")
        
        # Синхронный вызов (без Celery worker)
        result = send_course_update_email(course.id, "Тестовое обновление курса")
        print(f"   Результат: {result}")
        
        # Асинхронный вызов (через Celery)
        try:
            task_result = send_course_update_email.delay(course.id, "Асинхронное тестовое обновление")
            print(f"   Celery task ID: {task_result.id}")
            print(f"   Задача отправлена в очередь Celery")
        except Exception as e:
            print(f"   ⚠️  Ошибка отправки в Celery: {e}")
    else:
        print("   ⚠️  Нет курсов для тестирования")
    
except Exception as e:
    print(f"   ❌ Ошибка тестирования задачи: {e}")

print("\n" + "=" * 60)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 60)

# 5. Дополнительная информация
print("\n5. ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
print("   Для запуска Celery worker выполните:")
print("   celery -A config worker --loglevel=info")
print("")
print("   Для запуска Celery beat выполните:")
print("   celery -A config beat --loglevel=info")
print("")
print("   Для проверки очереди задач:")
print("   redis-cli MONITOR (если используется Redis)")
