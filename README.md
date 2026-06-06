# Habit Tracker API

A concise FastAPI backend service for tracking habits.

## Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite (default)
- JWT + bcrypt

## Structure
```
app/
  core/        # security: password hashing, JWT
  routes/      # API routes (auth, habits)
  schemas/     # Pydantic request/response schemas
  services/    # business logic
  config.py    # app and environment settings
  database.py  # database engine and sessions
  models.py    # ORM models
  main.py      # FastAPI entry point
```

## Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `.env` in the project root:
   ```env
   DATABASE_URL=sqlite:///./database.db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ```
3. Start the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## API
Interactive API docs: `/docs`.

- `POST /auth/register` — register a user
- `POST /auth/login` — log in and receive a token
- `POST /habits` — create a habit (auth token required)
- `GET /habits` — get the user's habits
- `POST /habits/{habit_id}/check` — mark a habit as completed for today
- `GET /habits/{habit_id}/stats` — get current streak
