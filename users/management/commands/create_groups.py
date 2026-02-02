from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson
from users.models import Payment  # Исправляем импорт


class Command(BaseCommand):
    help = 'Создает группы пользователей и назначает права'
    
    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Группа модераторов создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа модераторов уже существует'))
        # Получаем разрешения для моделей
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)
        payment_content_type = ContentType.objects.get_for_model(Payment)
        
        # Права для модераторов (просмотр и изменение, но не создание/удаление)
        course_permissions = Permission.objects.filter(
            content_type=course_content_type,
            codename__in=['view_course', 'change_course']
        )
        
        lesson_permissions = Permission.objects.filter(
            content_type=lesson_content_type,
            codename__in=['view_lesson', 'change_lesson']
        )
        
        payment_permissions = Permission.objects.filter(
            content_type=payment_content_type,
            codename__in=['view_payment']
        )
        # Добавляем права группе модераторов
        moderators_group.permissions.set(
            list(course_permissions) + list(lesson_permissions) + list(payment_permissions)
        )
        
        self.stdout.write(self.style.SUCCESS('Права назначены группе модераторов'))
        
        # Создаем группу студентов (опционально)
        students_group, created = Group.objects.get_or_create(name='students')
        
        if created:
            student_permissions = Permission.objects.filter(
                codename__in=['view_course', 'view_lesson']
            )
            students_group.permissions.set(student_permissions)
            self.stdout.write(self.style.SUCCESS('Группа студентов создана'))
        
        self.stdout.write(self.style.SUCCESS('Все группы созданы успешно!'))
