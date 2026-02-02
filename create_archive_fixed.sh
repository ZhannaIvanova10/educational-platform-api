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
cp manage.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  manage.py не найден"
cp requirements.txt "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  requirements.txt не найден"
cp README.md "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  README.md не найден"
cp INSTRUCTIONS.md "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  INSTRUCTIONS.md не найден"
cp create_test_data.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  create_test_data.py не найден"
cp final_test.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  final_test.py не найден"
cp FINAL_REPORT.txt "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  FINAL_REPORT.txt не найден"
cp .gitignore "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  .gitignore не найден"
cp add_moderator.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  add_moderator.py не найден"
cp create_admin.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  create_admin.py не найден"
cp final_api_test.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  final_api_test.py не найден"
cp final_check_all.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  final_check_all.py не найден"
cp populate_data.py "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  populate_data.py не найден"

# Директории
cp -r config "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  Не удалось скопировать config"
cp -r materials "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  Не удалось скопировать materials"
cp -r users "$TEMP_DIR/$PROJECT_NAME/" 2>/dev/null || echo "⚠️  Не удалось скопировать users"
# Исключаем venv и db.sqlite3
echo "🗑️  Исключаем venv и db.sqlite3..."

# Создаем архив
echo "📦 Создаем архив..."
cd "$TEMP_DIR"
if command -v tar >/dev/null 2>&1; then
    tar -czf "$PROJECT_NAME.tar.gz" "$PROJECT_NAME" 2>/dev/null
    if [ -f "$PROJECT_NAME.tar.gz" ]; then
        mv "$PROJECT_NAME.tar.gz" "$OLDPWD/"
        echo "✅ Создан архив: $PROJECT_NAME.tar.gz"
    else
        echo "❌ Не удалось создать tar.gz архив"
    fi
elif command -v zip >/dev/null 2>&1; then
    zip -r "$PROJECT_NAME.zip" "$PROJECT_NAME" 2>/dev/null
    if [ -f "$PROJECT_NAME.zip" ]; then
        mv "$PROJECT_NAME.zip" "$OLDPWD/"
        echo "✅ Создан архив: $PROJECT_NAME.zip"
    else
        echo "❌ Не удалось создать zip архив"
    fi
else
    echo "⚠️  Не найден tar или zip. Файлы скопированы в: $TEMP_DIR/$PROJECT_NAME"
    echo "   Скопируйте эту папку вручную"
fi

# Очистка
cd "$OLDPWD"
rm -rf "$TEMP_DIR"

echo ""
echo "📊 РЕЗУЛЬТАТ:"
if [ -f "${PROJECT_NAME}.tar.gz" ] || [ -f "${PROJECT_NAME}.zip" ]; then
    echo "🎉 АРХИВ СОЗДАН УСПЕШНО!"
    for archive in "${PROJECT_NAME}.tar.gz" "${PROJECT_NAME}.zip"; do
        if [ -f "$archive" ]; then
            echo "📦 Архив: $archive"
            echo "📏 Размер: $(du -h "$archive" | cut -f1)"
            echo "📁 Файлов в архиве: $(tar -tzf "$archive" 2>/dev/null | wc -l || unzip -l "$archive" 2>/dev/null | tail -1 | awk '{print $2}')"
        fi
    done
else
    echo "⚠️  Архив не создан. Проверьте структуру проекта."
fi
