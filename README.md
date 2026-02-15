# Hop & Barley - Интернет-магазин ингредиентов для пивоварения

Проект выполнен в рамках учебного курса. Представляет собой полноценный интернет-магазин с Web-интерфейсом и REST API.

## Технологии

- **Backend**: Django 5.0.1, Django REST Framework
- **Database**: PostgreSQL (Docker) / SQLite (локально)
- **Infrastructure**: Docker, Docker Compose
- **Auth**: JWT (SimpleJWT) для API, session-based для Web
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Quality**: Poetry, Flake8, Mypy (планируется)

## Структура проекта
hop_and_barley/
- ├── config/ # Настройки проекта
- ├── products/ # Каталог товаров
- ├── orders/ # Заказы и корзина
- ├── users/ # Пользователи и профили
- ├── cart/ # Корзина на сессиях
- ├── api/ # REST API + JWT + Swagger
- ├── reviews/ # Отзывы на товары
- ├── templates/ # HTML-шаблоны
- ├── static/ # CSS, JS, изображения
- ├── scripts/ # Утилиты и скрипты
- └── docker-compose.yml

##  Быстрый старт

### Предварительные требования
- Git
- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)

### Клонирование репозитория

git clone https://github.com/Sergei1606/hop_and_barley.git
- cd hop_and_barley
- git checkout main
## 2. Запуск через Docker

### Запуск PostgreSQL
- docker-compose up -d db

### Применение миграций
- python manage.py migrate

### Запуск сервера
- python manage.py runserver
## 3. Создание суперпользователя

- python manage.py createsuperuser
-  Логин: admin
- Email: admin@example.com
- Пароль: admin123
## 4. Доступ к приложению
Главная страница http://127.0.0.1:8000/

Каталог товаров http://127.0.0.1:8000/products/

Корзина http://127.0.0.1:8000/cart/

Личный кабинет http://127.0.0.1:8000/users/profile/

Админ-панель http://127.0.0.1:8000/admin/

API документация http://127.0.0.1:8000/api/docs/

API схема http://127.0.0.1:8000/api/schema/

## REST API документация
- Swagger/OpenAPI доступен по адресу: /api/docs/

- JWT Аутентификация:

POST /api/auth/login/ - получение токена

POST /api/auth/refresh/ - обновление токена

- Основные эндпоинты:

GET /api/products/ - список товаров

GET /api/products/{id}/ - детали товара

GET /api/categories/ - список категорий

GET/POST /api/cart/ - работа с корзиной

GET/POST /api/orders/ - заказы (требуется JWT)

## Выполненные требования ТЗ

- 3.1 Каталог товаров	
- 3.2 Страница товара	
- 3.3 Корзина	
- 3.4 Оформление заказа	
- 3.5 Личный кабинет	
- 3.6 Админ-панель	
- 3.7 REST API	
- 3.8 Документация API	
- Docker + PostgreSQL	

## Лицензия
- Проект выполнен в учебных целях.