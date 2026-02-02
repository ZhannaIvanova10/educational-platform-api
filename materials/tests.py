from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Course, Lesson, Subscription


User = get_user_model()


class MaterialsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com',
            password='testpass123',
            username='admin'
        )
        
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            username='user'
        )
        
        self.course1 = Course.objects.create(
            title='Курс 1',
            description='Описание курса 1',
            owner=self.admin_user
        )
        
        self.lesson1 = Lesson.objects.create(
            title='Урок 1',
            description='Описание урока 1',
            video_link='https://www.youtube.com/watch?v=test1',
            course=self.course1,
            owner=self.admin_user
        )
    def test_create_lesson_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'video_link': 'https://www.youtube.com/watch?v=newlesson',
            'course': self.course1.id
        }
        
        response = self.client.post('/api/v1/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_lesson_by_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        
        data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'video_link': 'https://www.youtube.com/watch?v=newlesson',
            'course': self.course1.id
        }
        
        response = self.client.post('/api/v1/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_youtube_url_validator(self):
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'title': 'Урок с некорректной ссылкой',
            'description': 'Описание',
            'video_link': 'https://vimeo.com/12345',
            'course': self.course1.id
        }

        response = self.client.post('/api/v1/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_subscription_flow(self):
        self.client.force_authenticate(user=self.regular_user)
        
        data = {'course_id': self.course1.id}
        response = self.client.post('/api/v1/materials/subscription/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        
        self.assertTrue(
            Subscription.objects.filter(
                user=self.regular_user,
                course=self.course1
            ).exists()
        )
        
        response = self.client.post('/api/v1/materials/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
    
    def test_get_subscriptions(self):
        Subscription.objects.create(user=self.regular_user, course=self.course1)
        
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/v1/materials/subscription/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_pagination(self):
        self.client.force_authenticate(user=self.regular_user)
        
        response = self.client.get('/api/v1/materials/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_course_with_subscription_flag(self):
        Subscription.objects.create(user=self.regular_user, course=self.course1)
        
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/v1/materials/courses/{self.course1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])
