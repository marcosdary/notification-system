from datetime import datetime
from pydantic import BaseModel
from json import dumps

from api.schemas import (
    NotificationSchema,
    PasswordChangeSchema,
    PasswordResetSchema,
    RegisterSchema,
    TwoFactorAuthSchema
)
from api.repositories import NotificationsRepository
from api.constants import Status
from api.services import EmailService, LoadTemplate
from api.queues import NotificationQueue

class EmailWorker:
    def __init__(
        self,
        queue: NotificationQueue,
        repo: NotificationsRepository,
        email_service: EmailService,
        load_template: LoadTemplate,
    ) -> None:
        self.queue = queue
        self.repo = repo
        self.email_service = email_service
        self.load_template = load_template

    SCHEMA_MAP: dict[str, type[BaseModel]] = {
        "PASSWORD_CHANGE": PasswordChangeSchema,
        "PASSWORD_RESET": PasswordResetSchema,
        "REGISTER": RegisterSchema,
        "TWO_FACTOR_AUTH": TwoFactorAuthSchema,
    }

    def _get_template(self, name_template: str, **kwargs) -> str: 
        return self.load_template.load(name_template, kwargs)

    def _load_queue_item(self) -> NotificationSchema:
        return self.queue.get_end_notification()

    def _send_email(self, to_email: str, subject: str, template: str) -> dict:
        email_service = self.email_service(to_email)
        return  email_service.send(
            subject=subject, 
            body=template
        )
    
    def _load_schema(self, schema: NotificationSchema) -> BaseModel:
        name_send = schema.typeSend.value
        schema_class = self.SCHEMA_MAP.get(name_send)

        if not schema_class:
            raise ValueError(f"TypeSend '{name_send}' não suportado.")

        return schema_class(**schema.info)

    def _finalize_schema(self, schema: NotificationSchema, response: dict) -> None:
        schema.status = Status.DONE
        schema.endIn = datetime.now()
        schema.responseServer = dumps(response)
        self.repo.create(schema=schema)

    def perform_action(self):
        schema = self._load_queue_item()

        if not schema:
            return

        try:
            info = self._load_schema(schema)
            template = self._get_template(schema.templateName.value, **info.model_dump())
            response = None # self._send_email(info.to_email, info.subject, template)
            schema.status = Status.DONE

        except Exception as e:
            schema.status = Status.ERROR
            response = {"error": str(e)}
            raise
        
        finally:
            schema.endIn = datetime.now()
            schema.responseServer = response
            self.repo.create(schema=schema)

