from requests import post, ConnectionError
from requests.exceptions import MissingSchema
from datetime import datetime

from app.repositories import WebhookRepository
from app.schemas.webhook_schema import (
    CreateWebhookSchema,
    UpdateWebhookSchema,
    ReadWebhookSchema
)
from app.constants import StatusWebhook
from app.config import settings
from app.exceptions import (
    RetryableError, 
    FatalError,
    DatabaseUnknownError,
    
)
from app.utils import sign_token

class WebhookDispatcherService:

    def __init__(self) -> None:
        self._url = settings.URL_WEBHOOK
        self._webhook_secret = settings.WEBHOOK_SECRET
        self._webhook_repo = WebhookRepository()
        self._user_agent = "notification-system/1.0.0"


    def process(self, payload: dict, schema: CreateWebhookSchema) -> None:
        try:
            self.__ensure_webhook_exists(schema=schema)
            self.__dispatch(payload=payload, delivery_id=schema.idWebhook)
            self._webhook_repo.update(UpdateWebhookSchema(
                idWebhook=schema.idWebhook,
                response="Enviado com sucesso",
                status=StatusWebhook.SUCCESS
            ))
        except DatabaseUnknownError:
            raise

        except ConnectionError as exc:
            raise FatalError("(ConnectionError) Falha em estabelecer conexão com o cliente.")
        
        except MissingSchema as exc:
            raise FatalError(f"(MissingSchema) Não há a url para envio a notificação.")

        except Exception:
            raise


    def mark_failed(self, delivery_id: str, exc: Exception) -> None:
       
        message = f"{type(exc).__name__}: {str(exc)}. Error."
        self._webhook_repo.update(UpdateWebhookSchema(
            idWebhook=delivery_id,
            response=message,
            status=StatusWebhook.FAILED
        ))

      
    def mark_retry(self, delivery_id: str, exc: Exception, retries: int, delay: int) -> None:
        
        message = f"{type(exc).__name__}: {str(exc)}. Tentativa {retries} falhou. Próxima tentativa em {delay} segundos."
            
        self._webhook_repo.update(UpdateWebhookSchema(
            idWebhook=delivery_id,
            response=message,
            status=StatusWebhook.RETRYING
        ))
       

    def __dispatch(self, payload: dict, delivery_id: str) -> None:
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Secret":  self._webhook_secret,
            "User-Agent": self._user_agent,
            "X-Request-ID": delivery_id,
            "X-Timestamp": str(datetime.now().timestamp())
        } 
                
        response = post(url=self._url, json=self.__sign_payload(payload), headers=headers, timeout=10) 
                
        
        if response.status_code >= 500:
            raise RetryableError("Erro servidor")

        if response.status_code == 429:
            raise RetryableError("Rate limit")

        if response.status_code >= 400:
            raise FatalError("Erro cliente")
        
        
    def __ensure_webhook_exists(self, schema: CreateWebhookSchema) -> ReadWebhookSchema:
        try:
            return self._webhook_repo.select_by_id(idWebhook=schema.idWebhook)
        except Exception as exc:
            return self._webhook_repo.create(schema=schema)

    
    def __sign_payload(self, payload: dict) -> dict:
        return {
            "data": sign_token(key=self._webhook_secret, payload=payload)
        }