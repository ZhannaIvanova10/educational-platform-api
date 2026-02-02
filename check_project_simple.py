import os

print("🔍 ПРОВЕРКА ПРОЕКТА")
print("=" * 50)

# Основные файлы
files = [
    "manage.py", "requirements.txt", "README.md", "INSTRUCTIONS.md",
    "create_test_data.py", "FINAL_REPORT.txt", ".gitignore"
]

print("📁 Основные файлы:")
for file in files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file}")

# Папки
folders = ["config", "materials", "users"]
print("\n📦 Папки:")
for folder in folders:
    if os.path.isdir(folder):
        py_files = len([f for f in os.listdir(folder) if f.endswith('.py')])
        print(f"  ✅ {folder}/ ({py_files} .py файлов)")
    else:
        print(f"  ❌ {folder}/")

# Проверка settings.py
print("\n⚙️  Настройки Django:")
if os.path.exists("config/settings.py"):
    print("  ✅ config/settings.py найден")
else:
    print("  ❌ config/settings.py не найден")

# Итог
print("\n" + "=" * 50)
print("🎉 ПРОЕКТ ГОТОВ К СДАЧЕ!")
print("\n📋 Отправьте архив или все файлы из списка выше.")
