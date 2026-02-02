import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from materials.models import Course, Lesson, Subscription
from users.models import Payment

User = get_user_model()

print("📦 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
print("="*60)

try:
    # Получаем пользователей
    admin = User.objects.get(email='admin@example.com')
    user = User.objects.get(email='user@example.com')
    moderator = User.objects.get(email='moderator@example.com')
    
    print(f"✅ Найдены пользователи:")
    print(f"   - Админ: {admin.email}")
    print(f"   - Пользователь: {user.email}")
    print(f"   - Модератор: {moderator.email}")
    
    # Создаем курсы
    print(f"\n📚 Создание курсов...")
    
    course1, created = Course.objects.get_or_create(
        title='Python для начинающих',
        defaults={
            'description': 'Изучение Python с нуля. Основы программирования.',
            'owner': admin
        }
    )
    if created:
        print(f"   ✅ Создан курс: {course1.title} (ID: {course1.id})")
    
    course2, created = Course.objects.get_or_create(
        title='Django REST Framework',
        defaults={
            'description': 'Создание REST API на Django REST Framework',
            'owner': admin
        }
    )
    if created:
        print(f"   ✅ Создан курс: {course2.title} (ID: {course2.id})")
    # Создаем уроки
    print(f"\n📖 Создание уроков...")
    
    lesson1, created = Lesson.objects.get_or_create(
        title='Введение в Python',
        defaults={
            'description': 'Основы языка Python: синтаксис, типы данных',
            'video_link': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
            'course': course1,
            'owner': admin
        }
    )
    if created:
        print(f"   ✅ Создан урок: {lesson1.title} (ID: {lesson1.id})")
    
    lesson2, created = Lesson.objects.get_or_create(
        title='Установка Django',
        defaults={
            'description': 'Как установить Django и настроить виртуальное окружение',
            'video_link': 'https://www.youtube.com/watch?v=UmljXZIypDc',
            'course': course2,
            'owner': admin
        }
    )
    if created:
        print(f"   ✅ Создан урок: {lesson2.title} (ID: {lesson2.id})")
    
    # Создаем подписку
    print(f"\n📌 Создание подписки...")
    
    subscription, created = Subscription.objects.get_or_create(
        user=user,
        course=course1
    )
    if created:
        print(f"   ✅ Создана подписка: {user.email} → {course1.title}")
    
    # Создаем платежи
    print(f"\n💰 Создание платежей...")
    
    payment1, created = Payment.objects.get_or_create(
        user=user,
        course_id=course1.id,
        defaults={
            'amount': 1000.00,
            'payment_method': 'transfer'
        }
    )
    if created:
        print(f"   ✅ Создан платеж: {user.email} - курс {course1.title} - 1000.00 руб")
    
    payment2, created = Payment.objects.get_or_create(
        user=user,
        lesson_id=lesson1.id,
        defaults={
            'amount': 500.00,
            'payment_method': 'cash'
        }
    )
    if created:
        print(f"   ✅ Создан платеж: {user.email} - урок {lesson1.title} - 500.00 руб")
    print(f"\n" + "="*60)
    print("✅ ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ!")
    print("="*60)
    
    print(f"\n📊 ИТОГО СОЗДАНО:")
    print(f"   Курсов: {Course.objects.count()}")
    print(f"   Уроков: {Lesson.objects.count()}")
    print(f"   Подписок: {Subscription.objects.count()}")
    print(f"   Платежей: {Payment.objects.count()}")
    
    print(f"\n🔗 ДЛЯ ТЕСТИРОВАНИЯ:")
    print(f"   Курс ID для подписки: {course1.id}")
    print(f"   Урок ID: {lesson1.id}")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
