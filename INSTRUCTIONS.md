# 📋 ИНСТРУКЦИИ ПО ЗАПУСКУ ПРОЕКТА

## 1. Установка
```bash
# Установите зависимости
pip install -r requirements.txt
```

## 2. Настройка базы данных
```bash
# Примените миграции
python manage.py migrate

# Создайте тестовых пользователей
python manage.py shell
# В интерактивной консоли выполните код из create_test_data.py
```

## 3. Запуск
```bash
# Запустите сервер разработки
python manage.py runserver
```

## 4. Тестирование API

### Получение токена:
```bash
curl -X POST http://localhost:8000/api/v1/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "user123"}'
```

### Получение списка курсов:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/materials/courses/
```

## 5. Тестовые пользователи
- Администратор: admin@example.com / admin123
- Модератор: moderator@example.com / moderator123
- Пользователь: user@example.com / user123

## 6. Доступ к админ-панели
http://localhost:8000/admin/
Используйте учетные данные администратора

## 7. Документация API
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
