import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Проверяем, существует ли уже администратор
    if User.objects.filter(email='admin@example.com').exists():
        admin = User.objects.get(email='admin@example.com')
        admin.set_password('admin123')
        admin.save()
        print(f"✓ Пароль администратора обновлен: {admin.email} / admin123")
    else:
        # Создаем нового администратора
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        print(f"✓ Суперпользователь создан: {admin.email} / admin123")
    
    # Создаем тестового пользователя
    if not User.objects.filter(email='user@example.com').exists():
        user = User.objects.create_user(
            email='user@example.com',
            password='user123',
            first_name='Тестовый',
            last_name='Пользователь',
            phone='+79999999999',
            city='Москва'
        )
        print(f"✓ Пользователь создан: {user.email} / user123")
    
    print("\n✅ Тестовые пользователи созданы успешно!")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
