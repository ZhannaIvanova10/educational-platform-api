from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView

app_name = 'materials'  # Добавляем пространство имен

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')  # Добавляем basename
router.register(r'lessons', LessonViewSet, basename='lessons')  # Добавляем basename

urlpatterns = [
    path('', include(router.urls)),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]
