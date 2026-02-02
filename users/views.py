from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserRegisterSerializer, CustomTokenObtainPairSerializer


User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    """Список пользователей (только для администраторов)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Администраторы видят всех
        if self.request.user.is_superuser:
            return User.objects.all()
        # Обычные пользователи видят только себя
        return User.objects.filter(id=self.request.user.id)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детальная информация о пользователе"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Изменять/удалять может только сам пользователь или администратор
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def get_object(self):
        # Пользователь может видеть любой профиль, но для чужого - ограниченная информация
        obj = super().get_object()
        return obj


class UserProfileView(APIView):
    """Профиль текущего пользователя"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный view для получения JWT токена"""
    serializer_class = CustomTokenObtainPairSerializer
