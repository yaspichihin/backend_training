from app.config import settings
from celery import Celery


celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    include=["app.tasks.tasks"] # Указываем где хранить задачи
)
