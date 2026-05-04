from celery import Celery
from celery.utils.log import get_task_logger
import ssl

from app.config.settings import settings

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_URL_LOCALHOST_ASYNC}/0",
    backend=f"{settings.REDIS_URL_LOCALHOST_ASYNC}/0"
)
"""
celery_app.conf.broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}

celery_app.conf.redis_backend_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}
"""
logger = get_task_logger(__name__)