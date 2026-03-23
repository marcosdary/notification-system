from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime

from api.config import SessionLocal as Session
from api.constants import Status
from api.exceptions import EntityValidationError, UnknownError, NotFoundError, ForbiddenActionError
from api.schemas.email_notification_schemas import (
    CreateEmailNotificationSchema,
    ReadEmailNotificationSchema
)
from api.models import EmailNotificationsModel


class EmailNotificationRepository:

    def create(self, schema: CreateEmailNotificationSchema) -> ReadEmailNotificationSchema:
        
        with Session() as session:
            try:
                notification = EmailNotificationsModel(**schema.model_dump(exclude=["actionLink", "code", "expiresAt"]))

                session.add(notification)
                session.commit()        
                return ReadEmailNotificationSchema.model_validate(notification)
            
            except IntegrityError as exc:
                session.rollback()
                raise EntityValidationError(f"Erro de integridade: {str(exc)}")
            
            except Exception as exc:
                session.rollback()
                raise UnknownError(f"Erro desconhecido: {str(exc)}")

    def select_by_id(self, idEmail: str) -> ReadEmailNotificationSchema:
        with Session() as session:
            try:
                notification = session.query(EmailNotificationsModel).filter(EmailNotificationsModel.idEmail == idEmail).first()

                if not notification:
                    raise NotFoundError("Nenhuma notificação por e-mail encontrada.")
                
                return ReadEmailNotificationSchema.model_validate(notification)

            except Exception as exc:
                raise exc

    def select_all(self) -> List[ReadEmailNotificationSchema]:
        with Session() as session:
            try:
                notifications = session.query(EmailNotificationsModel).all()

                if not notifications:
                    raise NotFoundError("Nenhuma notificações por e-mail encontrada.")
                
                schemas = []
                for row in notifications:
                    schemas.append(ReadEmailNotificationSchema.model_validate(row))

                return schemas

            except Exception as exc:
                raise exc

    def update_order_status(self, idEmail: str, status: Status, providerResponse: str, processedAt: datetime) -> None:
        with Session() as session:
            try:
                notification = session.query(EmailNotificationsModel).filter(EmailNotificationsModel.idEmail == idEmail).first()
                
                if not notification:
                    raise NotFoundError("Não foi encontrada a notificação. Ocorreu um erro.")
            
                notification.status = status.value
                notification.providerResponse = providerResponse
                notification.processedAt = processedAt
                
                session.commit()

            except Exception as exc:
                session.rollback()
                raise 
            
    def delete(self, idEmail: str) -> None:
        with Session() as session:
            try:
                notification = session.query(EmailNotificationsModel).filter(EmailNotificationsModel.idEmail == idEmail).first()

                if not notification:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                
                if notification.status == Status.PENDING:
                    raise ForbiddenActionError("Ação proibida até que o status seja mudado.")
            
                session.delete(notification)
                session.commit()

            except Exception as exc:
                session.rollback()
                raise 

    def delete_all(self) -> None:
        with Session() as session:
            try:
                notifications = session.query(EmailNotificationsModel).all()
            
                for notification in notifications:
                    session.delete(notification)
                    
                session.commit()

            except Exception as exc:
                session.rollback()
                raise exc


            
        