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
    schema = ReadEmailNotificationSchema.model_validate(payload)
    
    dispatcher = WebhookDispatcherService()

    try:
        dispatcher.process(payload=schema.model_dump(mode="json"), schema=CreateWebhookSchema(idWebhook=delivery_id))

    except DatabaseUnknownError as exc:
        logger.error(f"DatabaseUnknownError: {str(exc)}")
        return {"status": False}
    
    except RetryableError as exc:
        retries = self.request.retries + 1
        delay = get_backoff_delay(retries)

        try:
            dispatcher.mark_retry(delivery_id=delivery_id, exc=exc, retries=retries, delay=delay)
        except DatabaseUnknownError as exc:
            logger.error(f"DatabaseUnknownError: {str(exc)}")
            return {"status": False}

        logger.warning(f"RetryableError: {exc}. Tentativa {retries} falhou. Retentando em {delay} segundos.")
        raise self.retry(exc=exc, countdown=delay)

    except FatalError as exc:
        logger.error(f"FatalError: {exc}. Não será feita mais nenhuma tentativa.")
        try:
            dispatcher.mark_failed(delivery_id=delivery_id, exc=exc)
        except DatabaseUnknownError as exc:
            logger.error(f"DatabaseUnknownError: {str(exc)}")
            return {"status": False}
        
        return {"status": False, "response": str(exc)}

    return {"status": True}

