from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .paginators import LessonPagination, CoursePagination
from .permissions import IsModerator, IsOwner, IsOwnerOrModerator, IsNotModerator

User = get_user_model()


# Простая главная страница
def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Materials API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>📚 Materials API</h1>
        <p>Добро пожаловать в API для управления курсами и уроками!</p>

        <h2>🔗 Доступные endpoints:</h2>
        <div class="endpoint">
            <strong>GET</strong> <code>/api/v1/materials/courses/</code> - Список курсов
        </div>
        <div class="endpoint">
            <strong>GET</strong> <code>/api/v1/materials/lessons/</code> - Список уроков
        </div>
        <div class="endpoint">
            <strong>GET/POST</strong> <code>/api/v1/materials/subscription/</code> - Управление подписками
        </div>
        <div class="endpoint">
            <strong>POST</strong> <code>/api/v1/users/register/</code> - Регистрация
        </div>
        <div class="endpoint">
            <strong>POST</strong> <code>/api/v1/users/token/</code> - Получение JWT токена
        </div>
        <div class="endpoint">
            <strong>POST</strong> <code>/api/v1/users/token/refresh/</code> - Обновление JWT токена
        </div>
        <div class="endpoint">
            <strong>GET</strong> <code>/admin/</code> - Админ-панель
        </div>

        <h2>🔐 Права доступа:</h2>
        <ul>
            <li><strong>Администраторы:</strong> Полный доступ ко всему</li>
            <li><strong>Модераторы:</strong> Могут просматривать и редактировать любые курсы/уроки, но не могут создавать/удалять</li>
            <li><strong>Обычные пользователи:</strong> Только свои курсы/уроки</li>
        </ul>
        <hr>
        <p><small>Проект выполнен в рамках домашнего задания</small></p>
    </body>
    </html>
    """
    return HttpResponse(html)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        """Разграничение прав доступа - ИСПРАВЛЕННЫЙ ВАРИАНТ"""
        if self.action == 'create':
            # Создавать могут только администраторы и не-модераторы
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['update', 'partial_update']:
            # Обновлять могут владельцы, модераторы и администраторы
            permission_classes = [IsAuthenticated, IsOwnerOrModerator | IsAdminUser]
        elif self.action == 'destroy':
            # Удалять могут только владельцы и администраторы (но не модераторы)
            permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
        else:
            # Просматривать могут все аутентифицированные
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Фильтрация queryset в зависимости от прав пользователя"""
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        # Администраторы видят все
        if user.is_superuser:
            return Course.objects.all()

        # Модераторы видят все
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()

        # Обычные пользователи видят только свои курсы
        return Course.objects.filter(owner=user)

    def retrieve(self, request, *args, **kwargs):
        """Добавляем флаг подписки в детальную информацию о курсе"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        # Добавляем флаг подписки
        if request.user.is_authenticated:
            is_subscribed = Subscription.objects.filter(
                user=request.user,
                course=instance
            ).exists()
            data['is_subscribed'] = is_subscribed
        else:
            data['is_subscribed'] = False

        return Response(data)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']

    def get_permissions(self):
        """Разграничение прав доступа - ИСПРАВЛЕННЫЙ ВАРИАНТ"""
        if self.action == 'create':
            # Создавать могут только администраторы и не-модераторы
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['update', 'partial_update']:
            # Обновлять могут владельцы, модераторы и администраторы
            permission_classes = [IsAuthenticated, IsOwnerOrModerator | IsAdminUser]
        elif self.action == 'destroy':
            # Удалять могут только владельцы и администраторы (но не модераторы)
            permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
        else:
            # Просматривать могут все аутентифицированные
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Фильтрация queryset в зависимости от прав пользователя"""
        user = self.request.user

        if not user.is_authenticated:
            return Lesson.objects.none()

        # Администраторы видят все
        if user.is_superuser:
            return Lesson.objects.all()

        # Модераторы видят все
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "course_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(
            user=user,
            course=course_item
        )

        if subscription.exists():
            subscription.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)