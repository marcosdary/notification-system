from sqlalchemy import delete


from app.core.config import SessionLocalSync as SessionSync
from app.core.constants import StatusWebhook
from app.models import WebhookModel
from app.exceptions import (
    NotFoundError,
    ForbiddenActionError,
    DatabaseUnknownError
)
from app.schemas.webhook_schema import (
    ReadWebhookSchema,
    CreateWebhookSchema,
    UpdateWebhookSchema,
    ListWebhookSchema
)


class WebhookRepository:
    def __init__(self):
        self.__table = "webhook"


    def create(self, schema: CreateWebhookSchema) -> ReadWebhookSchema:
      
        with SessionSync() as session:
           

            try:
                webhook = WebhookModel(**schema.model_dump())
                session.add(webhook)
                session.commit()

                response = ReadWebhookSchema.model_validate(webhook)

                return response

            except Exception as exc:
                session.rollback()

                raise DatabaseUnknownError(f"(create) {str(exc)}")


    def select_by_id(self, idWebhook: str) -> ReadWebhookSchema:
       

        with SessionSync() as session:
         

            try:

                webhook = session.query(WebhookModel).filter(
                    WebhookModel.idWebhook == idWebhook
                ).first()

                if not webhook:
                    raise NotFoundError("Webhook não encontrado.")

                return ReadWebhookSchema.model_validate(webhook)

            except Exception as exc:

                raise DatabaseUnknownError(f"(select_by_id) {str(exc)}")


    def select_all(self) -> ListWebhookSchema:

        with SessionSync() as session:
         

            try:
               
                webhooks = session.query(WebhookModel).all()

                if not webhooks:
                    raise NotFoundError("Nenhum webhook encontrado.")


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
                

                webhook = session.query(WebhookModel).filter(
                    WebhookModel.idWebhook == schema.idWebhook
                ).first()

                if not webhook:
                    raise NotFoundError("Webhook não encontrado.")

                for key, value in schema.model_dump().items():
                    if value:
                        setattr(webhook, key, value)

                session.add(webhook)
                session.commit()


            except Exception as exc:
                session.rollback()

                raise DatabaseUnknownError(f"(update) {str(exc)}")


    # =========================
    # DELETE
    # =========================
    def delete(self, idWebhook: str) -> None:

        with SessionSync() as session:
            try:
                webhook = session.query(WebhookModel).filter(
                    WebhookModel.idWebhook == idWebhook
                ).first()

                if not webhook:
                    raise NotFoundError("Webhook não encontrado.")

                if webhook.status == StatusWebhook.PENDING:
                    raise ForbiddenActionError("Ação proibida enquanto status for PENDING.")

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