#!/bin/bash
echo "📦 СОЗДАНИЕ АРХИВА ПРОЕКТА..."
echo ""

# Имя проекта
PROJECT_NAME="educational_platform_project"

# Создаем временную директорию
TEMP_DIR=$(mktemp -d)
echo "📁 Создаем временную директорию: $TEMP_DIR"

# Копируем файлы
echo "📋 Копируем файлы проекта..."
mkdir -p "$TEMP_DIR/$PROJECT_NAME"

# Основные файлы
cp manage.py "$TEMP_DIR/$PROJECT_NAME/"
cp requirements.txt "$TEMP_DIR/$PROJECT_NAME/"
cp README.md "$TEMP_DIR/$PROJECT_NAME/"
cp INSTRUCTIONS.md "$TEMP_DIR/$PROJECT_NAME/"
cp create_test_data.py "$TEMP_DIR/$PROJECT_NAME/"
cp final_test.py "$TEMP_DIR/$PROJECT_NAME/"
cp FINAL_REPORT.txt "$TEMP_DIR/$PROJECT_NAME/"
cp .gitignore "$TEMP_DIR/$PROJECT_NAME/"

# Директории
cp -r materials_project "$TEMP_DIR/$PROJECT_NAME/"
cp -r materials "$TEMP_DIR/$PROJECT_NAME/"
cp -r users "$TEMP_DIR/$PROJECT_NAME/"

# Создаем архив
echo "📦 Создаем архив..."
cd "$TEMP_DIR"
if command -v tar >/dev/null 2>&1; then
    tar -czf "$PROJECT_NAME.tar.gz" "$PROJECT_NAME"
    mv "$PROJECT_NAME.tar.gz" "$OLDPWD/"
    echo "✅ Создан архив: $PROJECT_NAME.tar.gz"
elif command -v zip >/dev/null 2>&1; then
    zip -r "$PROJECT_NAME.zip" "$PROJECT_NAME"
    mv "$PROJECT_NAME.zip" "$OLDPWD/"
    echo "✅ Создан архив: $PROJECT_NAME.zip"
else
    echo "⚠️  Не найден tar или zip. Файлы скопированы в: $TEMP_DIR/$PROJECT_NAME"
fi

# Очистка
cd "$OLDPWD"
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 АРХИВ СОЗДАН!"
echo "Размер архива: $(du -h ${PROJECT_NAME}.* 2>/dev/null | cut -f1 || echo "N/A")"
