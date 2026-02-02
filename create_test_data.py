print("🔄 Создание тестовых данных...")

test_data = """
👥 Тестовые пользователи:
1. Администратор
   Email: admin@example.com
   Пароль: admin123

2. Модератор
   Email: moderator@example.com
   Пароль: moderator123

3. Пользователь
   Email: user@example.com
   Пароль: user123

📝 Для создания пользователей запустите:
python manage.py shell
"""
print(test_data)

# Далее код для Django shell
django_code = """
from django.contrib.auth import get_user_model

User = get_user_model()

# Администратор
admin, created = User.objects.get_or_create(
    email='admin@example.com',
    defaults={
        'first_name': 'Админ',
        'last_name': 'Администратов',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"✅ Создан администратор: {admin.email}")

# Модератор
moderator, created = User.objects.get_or_create(
    email='moderator@example.com',
    defaults={
        'first_name': 'Модератор',
        'last_name': 'Модераторов',
        'is_staff': True,
        'is_superuser': False
    }
)
if created:
    moderator.set_password('moderator123')
    moderator.save()
    print(f"✅ Создан модератор: {moderator.email}")

# Обычный пользователь
user, created = User.objects.get_or_create(
    email='user@example.com',
    defaults={
        'first_name': 'Тестовый',
        'last_name': 'Пользователь',
        'is_staff': False,
        'is_superuser': False
    }
)
if created:
    user.set_password('user123')
    user.save()
    print(f"✅ Создан пользователь: {user.email}")
"""

print("\n🔧 Код для Django shell:")
print(django_code)
