from celery import Celery
from api.config.settings import settings

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/1"
)