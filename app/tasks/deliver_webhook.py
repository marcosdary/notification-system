from time import time

from app.config import celery_app, logger
from app.exceptions import (
    RetryableError, 
    FatalError,
    DatabaseUnknownError
)
from app.schemas.email_notification_schema import ReadEmailNotificationSchema
from app.schemas.webhook_schema import CreateWebhookSchema
from app.utils import get_backoff_delay
from app.services import WebhookDispatcherService


@celery_app.task(bind=True, max_retries=5)
def deliver_webhook(self, payload: dict, delivery_id: str) -> None:
    task = "task.deliver_webhook"

    logger.info(
        "Iniciando envio de webhook",
        extra={
            "event": "DELIVER_WEBHOOK_START",
            "task": task,
            "layer": "task",
            "delivery_id": delivery_id
        }
    )

    start = time()

    schema = ReadEmailNotificationSchema.model_validate(payload)
    dispatcher = WebhookDispatcherService()

    try:
        logger.debug(
            "Processando envio do webhook",
            extra={
                "event": "DELIVER_WEBHOOK_PROCESSING",
                "task": task,
                "layer": "task",
                "delivery_id": delivery_id
            }
        )

        start_processing_time = time()

        dispatcher.process(
            payload=schema.model_dump(mode="json"),
            schema=CreateWebhookSchema(idWebhook=delivery_id)
        )

        processing_time = time() - start_processing_time

        logger.info(
            "Webhook enviado com sucesso",
            extra={
                "event": "DELIVER_WEBHOOK_SUCCESS",
                "task": task,
                "layer": "task",
                "delivery_id": delivery_id,
                "processing_time": processing_time
            }
        )

    except DatabaseUnknownError as exc:
        logger.exception(
            "Erro desconhecido no banco ao enviar webhook",
            extra={
                "event": "DELIVER_WEBHOOK_DATABASE_ERROR",
                "task": task,
                "layer": "task",
                "delivery_id": delivery_id,
                "error": str(exc),
                "type_error": exc.__class__.__name__,
            }
        )
        return {"status": False}

    except RetryableError as exc:
        retries = self.request.retries + 1
        delay = get_backoff_delay(retries)

        logger.warning(
            "Erro transitório ao enviar webhook, tentativa de retry",
            extra={
                "event": "DELIVER_WEBHOOK_RETRY",
                "task": task,
                "layer": "task",
                "delivery_id": delivery_id,
                "retries": retries,
                "delay": delay,
                "error": str(exc),
                "type_error": exc.__class__.__name__,
            }
        )

        try:
            dispatcher.mark_retry(
                delivery_id=delivery_id,
                exc=exc,
                retries=retries,
                delay=delay
            )
        except DatabaseUnknownError as db_exc:
            logger.exception(
                "Erro ao registrar retry no banco",
                extra={
                    "event": "DELIVER_WEBHOOK_RETRY_DB_ERROR",
                    "task": task,
                    "layer": "task",
                    "delivery_id": delivery_id,
                    "error": str(db_exc),
                    "type_error": db_exc.__class__.__name__,
                }
            )
            return {"status": False}

        raise self.retry(exc=exc, countdown=delay)

    except FatalError as exc:
        logger.error(
            "Erro fatal ao enviar webhook, não haverá retry",
            extra={
                "event": "DELIVER_WEBHOOK_FATAL_ERROR",
                "task": task,
                "layer": "task",
                "delivery_id": delivery_id,
                "error": str(exc),
                "type_error": exc.__class__.__name__,
            }
        )

        try:
            dispatcher.mark_failed(delivery_id=delivery_id, exc=exc)
        except DatabaseUnknownError as db_exc:
            logger.exception(
                "Erro ao marcar webhook como failed no banco",
                extra={
                    "event": "DELIVER_WEBHOOK_FAIL_DB_ERROR",
                    "task": task,
                    "layer": "task",
                    "delivery_id": delivery_id,
                    "error": str(db_exc),
                    "type_error": db_exc.__class__.__name__,
                }
            )
            return {"status": False}

        return {"status": False, "response": str(exc)}

    execution = time() - start

    logger.info(
        "Finalização da task de webhook",
        extra={
            "event": "DELIVER_WEBHOOK_FINISH",
            "task": task,
            "layer": "task",
            "delivery_id": delivery_id,
            "execution": execution
        }
    )

    return {"status": True}