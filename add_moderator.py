import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Создаем или получаем модератора
moderator, created = User.objects.get_or_create(
    email='moderator@example.com',
    defaults={
        'first_name': 'Модератор',
        'last_name': 'Тестовый',
        'is_staff': True
    }
)

if created:
    moderator.set_password('moderator123')
    moderator.save()
    print(f"✓ Модератор создан: {moderator.email} / moderator123")
else:
    print(f"✓ Модератор уже существует: {moderator.email}")
# Добавляем в группу модераторов
moderators_group, _ = Group.objects.get_or_create(name='moderators')
moderator.groups.add(moderators_group)
print(f"✓ Модератор добавлен в группу 'moderators'")

print("\n✅ Настройка модератора завершена!")
