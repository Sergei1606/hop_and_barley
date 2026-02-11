FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка Poetry и зависимостей
RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

# Копирование проекта
COPY . .

# Сборка статики
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]