from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    include=["app.tasks.tasks"] # Указываем где хранить задачи
)
