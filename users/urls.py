from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterAPIView, 
    UserListView, 
    UserDetailView, 
    UserProfileView,
    CustomTokenObtainPairView
)
from .views_payments import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
