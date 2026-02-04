import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('config')

# Загружаем настройки из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()

# Настройка периодических задач (Celery Beat)
app.conf.beat_schedule = {
    'check-inactive-users-every-day': {
        'task': 'users.tasks.check_inactive_users',
        'schedule': crontab(hour=3, minute=0),  # Каждый день в 3:00 ночи
        'args': (),
    },
}

# Настройка таймзоны
app.conf.timezone = 'Europe/Moscow'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
