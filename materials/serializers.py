from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import youtube_url_validator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[youtube_url_validator])
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_link', 'course', 'owner', 
                  'created_at', 'updated_at']
        read_only_fields = ['owner']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner', 'lessons_count', 
                  'lessons', 'is_subscribed', 'created_at', 'updated_at']
        read_only_fields = ['owner']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False
