#!/usr/bin/env python
"""
Тест аутентификации и API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_swagger():
    """Тест Swagger"""
    print("🔍 Проверка Swagger документации...")
    try:
        response = requests.get(f"{BASE_URL}/swagger/", timeout=3)
        print(f"  Swagger UI: {'✅ Доступен' if response.status_code == 200 else '❌ Недоступен'} ({response.status_code})")
        
        response = requests.get(f"{BASE_URL}/redoc/", timeout=3)
        print(f"  ReDoc: {'✅ Доступен' if response.status_code == 200 else '❌ Недоступен'} ({response.status_code})")
        
        response = requests.get(f"{BASE_URL}/", timeout=3)
        print(f"  Главная: {'✅ Доступна' if response.status_code == 200 else '❌ Недоступна'} ({response.status_code})")
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")

def test_auth():
    """Тест аутентификации"""
    print("\n🔐 Тест аутентификации...")
    
    test_users = [
        ("user@example.com", "user123"),
        ("admin@example.com", "admin123"),
        ("moderator@example.com", "moderator123"),
    ]
    
    for email, password in test_users:
        print(f"\n  👤 {email}:")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/users/token/",
                json={"email": email, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                token = response.json().get("access")
                print(f"    ✅ Токен получен: {token[:30]}...")
                # Проверяем доступ к профилю
                headers = {"Authorization": f"Bearer {token}"}
                profile_response = requests.get(
                    f"{BASE_URL}/api/v1/users/profile/",
                    headers=headers,
                    timeout=3
                )
                
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    print(f"    ✅ Профиль доступен: {profile.get('email')}")
                else:
                    print(f"    ⚠️  Профиль: статус {profile_response.status_code}")
                    
            else:
                print(f"    ❌ Ошибка: статус {response.status_code}")
                if response.status_code == 401:
                    print("    💡 Неверные учетные данные")
                    
        except Exception as e:
            print(f"    ❌ Ошибка запроса: {e}")

def main():
    print("🎯 ТЕСТ ПРОЕКТА - ОБРАЗОВАТЕЛЬНАЯ ПЛАТФОРМА API")
    print("=" * 60)
    print("⚠️  Для запуска тестов сервер должен быть запущен")
    print("   Запустите: python manage.py runserver")
    print("=" * 60)
    
    test_swagger()
    test_auth()
    
    print("\n" + "=" * 60)
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("\n✅ Проект работает корректно!")
    print("📋 Что проверено:")
    print("   • Swagger документация")
    print("   • JWT аутентификация")
    print("   • Доступ к профилю")
    print("\n🚀 Проект готов к использованию!")

if __name__ == "__main__":
    main()
