from celery import Celery
import ssl

from api.config.settings import settings

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/0"
)

celery_app.conf.broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}

celery_app.conf.redis_backend_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
}