# Habit Tracker API

Лаконичный backend-сервис для отслеживания привычек на FastAPI.

## Стек
- Python
- FastAPI
- SQLAlchemy
- SQLite (по умолчанию)
- JWT + bcrypt

## Структура
```
app/
  core/        # безопасность: хеширование паролей, JWT
  routes/      # API-роуты (auth, habits)
  schemas/     # Pydantic-схемы запросов/ответов
  services/    # бизнес-логика
  config.py    # настройки приложения и env
  database.py  # подключение к БД и сессии
  models.py    # ORM-модели
  main.py      # точка входа FastAPI
```

## Запуск
1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создать `.env` в корне проекта:
   ```env
   DATABASE_URL=sqlite:///./database.db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ```
3. Запустить приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

## API
Подробная интерактивная документация: `/docs`.

- `POST /auth/register` — регистрация пользователя
- `POST /auth/login` — вход и получение токена
- `POST /habits` — создание привычки (нужен Bearer-токен)
- `GET /habits` — список привычек пользователя
- `POST /habits/{habit_id}/check` — отметить привычку за сегодня
- `GET /habits/{habit_id}/stats` — получить текущий streak
