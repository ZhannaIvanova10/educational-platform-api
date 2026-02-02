from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models_payments import Payment
import json
from pathlib import Path

User = get_user_model()

class Command(BaseCommand):
    help = 'Загружает начальные данные в базу'
    
    def handle(self, *args, **options):
        self.stdout.write('Загрузка начальных данных...')
        
        # Загружаем группы
        groups_fixture = Path(__file__).parent.parent.parent / 'fixtures' / 'groups.json'
        if groups_fixture.exists():
            call_command('loaddata', str(groups_fixture))
            self.stdout.write(self.style.SUCCESS('Группы загружены'))
        else:
            self.stdout.write(self.style.WARNING('Файл с группами не найден'))
        
        # Создаем тестового администратора если нет
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Администратор создан'))
        
        # Создаем тестового модератора
        if not User.objects.filter(email='moderator@example.com').exists():
            moderator = User.objects.create_user(
                email='moderator@example.com',
                password='moderator123',
                first_name='Модератор',
                last_name='Тестовый'
            )
            from django.contrib.auth.models import Group
            moderators_group = Group.objects.get(name='moderators')
            moderator.groups.add(moderators_group)
            self.stdout.write(self.style.SUCCESS('Модератор создан'))
        # Создаем тестового пользователя
        if not User.objects.filter(email='user@example.com').exists():
            User.objects.create_user(
                email='user@example.com',
                password='user123',
                first_name='Пользователь',
                last_name='Тестовый',
                phone='+79999999999',
                city='Москва'
            )
            self.stdout.write(self.style.SUCCESS('Пользователь создан'))
        
        self.stdout.write(self.style.SUCCESS('Все данные успешно загружены!'))
