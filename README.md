# todo

docker-compose up -d --build


# FastAPI Task Manager

## 🚀 Запуск проекта

### Локально
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### В Docker
```bash
docker-compose up -d
```

## 📝 API Endpoints
Документация доступна после запуска:
- Swagger UI: `http://localhost:4014/docs`
- ReDoc: `http://localhost:4014/redoc`

## 🔧 Переменные окружения
Создайте `.env` файл:
```ini
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
```
