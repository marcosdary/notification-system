from celery import Celery
from celery.schedules import crontab

from app.core.config.settings import settings

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/1",
    include=[
        "app.tasks.email_task",
        "app.tasks.file_task"
    ]
)

celery_app.conf.beat_schedule = {
    'files-delete': {
        "task": "app.tasks.file_task.process_files_delete",
        "schedule": 20,
        "args": ()
    }
}

if __name__ == "__main__":
    celery_app.start()