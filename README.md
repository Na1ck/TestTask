# Test Task API

Бэкенд-приложение на Django + Django REST Framework с реализацией системы аутентификации.

## Функциональность

- Аутентификация через токены (Djoser + REST Framework)
- Регистрация и управление пользователями
- Мягкое удаление аккаунтов (is_active=False)
- Mock-views для демонстрации работы с бизнес-объектами
- Тесты для проверки прав доступа

## Технологии

- Python 3.9
- Django 4.2
- Django REST Framework
- Djoser (аутентификация)
- SQLite (по умолчанию)

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Na1ck/TestTask.git
cd backend/
```

### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py migrate
```
### 5. Создайте и настройте файл .env
Создайте в корне проекта файл .env и заполните все необходимые переменные окружения. Файл будет использоваться всеми сервисами. Пример необходимых переменных:

```
DJANGO_KEY=key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Запуск сервера

```bash
python manage.py runserver
```
Сервер будет доступен по адресу: http://localhost:8000/

## API Endpoints

Аутентификация (Djoser)

|Метод|URL|Описание|
|-----|---|--------|
|POST	|```/api/auth/users/```|Регистрация нового пользователя|
|POST	|```/api/auth/token/login/```|Получение токена (вход)|
|POST	|```/api/auth/token/logout/```|Выход (удаление токена)|
|GET	|```/api/auth/users/me/```|Информация о текущем пользователе|
|DELETE	|```/api/auth/users/me/```|Мягкое удаление аккаунта|
|POST	|```/api/auth/users/reset_password/```|Сброс пароля|
|POST	|```/api/auth/users/reset_password_confirm/```|Подтверждение сброса пароля|

### Примеры запросов
Регистрация пользователя
```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "password": "secure123",
    "re_password": "secure123",
    "email": "user6@example.com"
  }'
```
Получение токена (вход)
```bash
curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "secure123"
  }'
```
Мягкое удаление аккаунта
```bash
curl -X DELETE http://localhost:8000/api/auth/users/me/ \
  -H "Authorization: Token YOUR_TOKEN"
```
Получение списка проектов
```bash
curl -X GET http://localhost:8000/api/mock/projects/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Mock-объекты (для демонстрации)

```bash
# Получить список проектов
GET /api/mock/projects/

# Создать новый проект
POST /api/mock/projects/
{
    "name": "Новый проект",
    "description": "Описание проекта"
}

# Получить детали проекта
GET /api/mock/projects/{id}/

# Обновить проект
PUT /api/mock/projects/{id}/
{
    "name": "Обновленное название"
}

# Мягко удалить (архивировать) проект
DELETE /api/mock/projects/{id}/
```

## Автор

**Кудрявцев Никита**  
- GitHub: [Na1ck](https://github.com/Na1ck)
