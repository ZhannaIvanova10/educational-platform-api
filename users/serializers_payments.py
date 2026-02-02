from rest_framework import serializers
from .models import Payment  # Импортируем из models.py


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей с IntegerField"""
    course_title = serializers.SerializerMethodField()
    lesson_title = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'payment_date', 'course_id', 'course_title',
            'lesson_id', 'lesson_title', 'amount', 'payment_method'
        ]
        read_only_fields = ['user', 'payment_date']
    
    def get_course_title(self, obj):
        if obj.course:
            return obj.course.title
        return None
    
    def get_lesson_title(self, obj):
        if obj.lesson:
            return obj.lesson.title
        return None

class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа"""
    
    class Meta:
        model = Payment
        fields = ['course_id', 'lesson_id', 'amount', 'payment_method']
    
    def validate(self, data):
        """Проверка что указан либо курс, либо урок"""
        course_id = data.get('course_id')
        lesson_id = data.get('lesson_id')
        
        if course_id and lesson_id:
            raise serializers.ValidationError("Укажите только курс ИЛИ урок")
        if not course_id and not lesson_id:
            raise serializers.ValidationError("Укажите курс ИЛИ урок")
        
        # Проверяем что курс/урок существуют
        if course_id:
            from materials.models import Course
            if not Course.objects.filter(id=course_id).exists():
                raise serializers.ValidationError(f"Курс с ID {course_id} не найден")
        
        if lesson_id:
            from materials.models import Lesson
            if not Lesson.objects.filter(id=lesson_id).exists():
                raise serializers.ValidationError(f"Урок с ID {lesson_id} не найден")
        
        return data
    
    def create(self, validated_data):
        # Автоматически привязываем платеж к текущему пользователю
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
