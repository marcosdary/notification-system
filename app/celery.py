from celery import Celery

from app.core.config.settings import settings

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/1",
    include=[
        "app.tasks.email_task"
    ]
)

if __name__ == "__main__":
    celery_app.start()