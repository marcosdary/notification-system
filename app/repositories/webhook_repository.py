from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
 
from app.config import SessionLocalAsync as SessionAsync, SessionLocalSync as SessionSync
from app.constants import StatusWebhook
from app.models import WebhookModel
from app.exceptions import (
    EntityValidationError, 
    NotFoundError, 
    UnknownError,
    DatabaseUnknownError,
    ForbiddenActionError
)
from app.schemas.webhook_schema import (
    ReadWebhookSchema,
    CreateWebhookSchema,
    UpdateWebhookSchema,
    ListWebhookSchema
)
 
class WebhookRepository:
    def create(self, schema: CreateWebhookSchema) -> ReadWebhookSchema:
        with SessionSync() as session:
            try:
                webhook = WebhookModel(**schema.model_dump())
 
                session.add(webhook)
                session.commit()        
                return ReadWebhookSchema.model_validate(webhook)
            
            except Exception as exc:
                session.rollback()
                raise DatabaseUnknownError(f"(create) {str(exc)}")
    
    def select_by_id(self, idWebhook: str) -> ReadWebhookSchema:
        with SessionSync() as session:
            try:
                stmt = session.query(WebhookModel).filter(WebhookModel.idWebhook == idWebhook)
            
                webhook = stmt.first()
 
                if not webhook:
                    raise NotFoundError("Nenhuma notificação (webhook) por e-mail encontrada.")
                
                return ReadWebhookSchema.model_validate(webhook)
 
            except Exception as exc:
                raise DatabaseUnknownError(f"(select_by_id) {str(exc)}")
 
    def select_all(self) -> ListWebhookSchema:
        with SessionSync() as session:
            try:
                stmt = session.query(WebhookModel)
        
                webhooks = stmt.all()
 
                if not webhooks:
                    raise NotFoundError("Nenhuma notificações por e-mail encontrada.")
 
                return ListWebhookSchema(
                    info=[
                        ReadWebhookSchema.model_validate(row)
                        for row in webhooks
                    ]
                )
 
            except Exception as exc:
                raise DatabaseUnknownError(f"(select_all) {str(exc)}")
            
    def update(self, schema: UpdateWebhookSchema) -> None:
        with SessionSync() as session:
            try:
                stmt = session.query(WebhookModel).filter(WebhookModel.idWebhook == schema.idWebhook)
                
                webhook = stmt.first()
                
                if not webhook:
                    raise NotFoundError("Não foi encontrada a notificação. Ocorreu um erro.")
 
                for key, value in schema.model_dump().items():
                    if value:
                        setattr(webhook, key, value)
 
                session.add(webhook)
                session.commit()
 
            except Exception as exc:
                session.rollback()
                raise DatabaseUnknownError(f"(update) {str(exc)}")
            
    def delete(self, idWebhook: str) -> None:
        with SessionSync() as session:
            try:
                stmt = session.query(WebhookModel).filter(WebhookModel.idWebhook == idWebhook)
                
                webhook = stmt.first()
                if not webhook:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                
                if webhook.status == StatusWebhook.PENDING:
                    raise ForbiddenActionError("Ação proibida até que o status seja mudado.")
            
                session.delete(webhook)
                session.commit()

            except Exception as exc:
                session.rollback()
                raise DatabaseUnknownError(f"(delete) {str(exc)}")

    def delete_all(self) -> None:
        with SessionSync() as session:
            try:
                session.execute(delete(WebhookModel))
                session.commit()

            except Exception as exc:
                session.rollback()
                raise DatabaseUnknownError(str(exc))
            