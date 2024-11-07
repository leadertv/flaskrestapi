
# REST API для сайта объявлений

Этот проект представляет собой REST API для создания, редактирования и удаления объявлений с аутентификацией и авторизацией пользователей. Реализован с использованием Flask и базы данных SQLite.

## Основные возможности

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление объявлений
- Защита маршрутов с помощью JSON Web Token (JWT)
- Только авторизованные пользователи могут создавать объявления
- Только владелец объявления может редактировать или удалять его

## Установка и настройка

### Предварительные требования

- Python 3.8+
- [Flask](https://flask.palletsprojects.com/) и дополнительные зависимости
- Все есть в requirements.txt

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/leadertv/flaskrestapi.git
   cd flaskrestapi
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv flaskapi
   source flaskapi/bin/activate  # Для Linux/MacOS
   flaskapi\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```


### Запуск сервера

Запустите Flask на вашем VDS сервере (или локально):
```bash
flask run --host=0.0.0.0 --port=5000
```

Сервер будет доступен по адресу `http://IP:5000`.

## Использование API

Ниже описаны основные маршруты API. Используйте такие инструменты, как Postman или расширение REST Client в VS Code, для отправки запросов.

### 1. Регистрация пользователя

**Запрос**:
```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Ответ**:
```json
{
  "message": "Пользователь зарегистрирован"
}
```

### 2. Авторизация пользователя

**Запрос**:
```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Ответ**:
```json
{
  "access_token": "<ваш_JWT_токен - скопируйте его>"
}
```

### 3. Создание объявления

**Запрос**:
```http
POST /ads
Content-Type: application/json
Authorization: Bearer <ваш_JWT_токен>

{
  "title": "Продажа велосипеда",
  "description": "Горный велосипед, отличное состояние"
}
```

**Ответ**:
```json
{
  "message": "Объявление создано",
  "ad": {
    "id": 1,
    "title": "Продажа велосипеда",
    "description": "Горный велосипед, отличное состояние",
    "created_at": "2024-01-01T12:00:00",
    "owner_id": 1
  }
}
```

### 4. Получение объявления по ID

**Запрос**:
```http
GET /ads/<ad_id>
```

**Ответ**:
```json
{
  "id": 1,
  "title": "Продажа велосипеда",
  "description": "Горный велосипед, отличное состояние",
  "created_at": "2024-01-01T12:00:00",
  "owner_id": 1
}
```

### 5. Удаление объявления

**Запрос**:
```http
DELETE /ads/<ad_id>
Authorization: Bearer <ваш_JWT_токен>
```

**Ответ**:
```json
{
  "message": "Объявление удалено"
}
```

## Дополнительно
в папке есть файл запросов, api_tests.http используйте его для тестов или на рабочем сервере http://194.58.126.236:5000/


