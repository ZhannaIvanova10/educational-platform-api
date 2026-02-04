from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Course, Lesson, Subscription
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseWithPriceSerializer,
)
from .permissions import IsOwnerOrStaff

# Пробуем импортировать Celery задачи
try:
    from materials.tasks import send_course_update_email
    CELERY_AVAILABLE = True
    print("✅ Celery задачи доступны")
except ImportError as e:
    CELERY_AVAILABLE = False
    print(f"⚠️  Celery задачи недоступны: {e}")


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с курсами с поддержкой подписок и уведомлений
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_published']
    ordering_fields = ['title', 'price', 'created_at']
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        """
        Выбираем сериализатор в зависимости от действия
        """
        if self.action == 'list' or self.action == 'retrieve':
            return CourseWithPriceSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Переопределяем метод обновления для отправки уведомлений
        """
        instance = serializer.save()

        # Дополнительное задание: проверяем, обновлялся ли курс за последние 4 часа
        four_hours_ago = timezone.now() - timedelta(hours=4)

        if CELERY_AVAILABLE and instance.updated_at < four_hours_ago:
            # Отправляем уведомление асинхронно
            update_message = f"Курс '{instance.title}' был обновлен. Проверьте новые материалы!"

            try:
                # Запускаем Celery задачу асинхронно
                send_course_update_email.delay(
                    course_id=instance.id,
                    update_message=update_message
                )
                print(f"✅ Задача на отправку уведомлений для курса '{instance.title}' отправлена в Celery")
            except Exception as e:
                print(f"❌ Ошибка при отправке задачи в Celery: {e}")
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """
        Подписка на курс
        """
        course = self.get_object()
        user = request.user

        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course,
            defaults={'is_active': True}
        )

        if not created:
            subscription.is_active = not subscription.is_active
            subscription.save()

        message = 'подписка оформлена' if subscription.is_active else 'подписка отменена'

        return Response({
            'message': f'{message} на курс "{course.title}"',
            'subscription_id': subscription.id,
            'is_active': subscription.is_active
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_subscriptions(self, request):
        """
        Список курсов, на которые подписан текущий пользователь
        """
        subscriptions = Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).select_related('course')

        courses = [sub.course for sub in subscriptions]
        serializer = self.get_serializer(courses, many=True)

        return Response(serializer.data)
class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с уроками с поддержкой уведомлений
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['course']
    ordering_fields = ['title', 'order']
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Переопределяем метод обновления урока для отправки уведомлений
        """
        instance = serializer.save()
        course = instance.course

        if not CELERY_AVAILABLE:
            return

        # Проверяем, обновлялся ли курс за последние 4 часа
        four_hours_ago = timezone.now() - timedelta(hours=4)

        if course.updated_at < four_hours_ago:
            # Обновляем время обновления курса
            course.updated_at = timezone.now()
            course.save()
            # Отправляем уведомление асинхронно
            update_message = f"В курсе '{course.title}' был обновлен урок: '{instance.title}'"

            try:
                # Запускаем Celery задачу асинхронно
                send_course_update_email.delay(
                    course_id=course.id,
                    update_message=update_message
                )
                print(f"✅ Задача на отправку уведомлений для курса '{course.title}' отправлена в Celery")
            except Exception as e:
                print(f"❌ Ошибка при отправке задачи в Celery: {e}")
