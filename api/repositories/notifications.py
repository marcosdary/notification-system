from sqlalchemy.exc import IntegrityError
from json import dumps
from typing import List

from api.constants import Session
from api.exceptions import EntityValidationError, UnknownError, NotFoundError
from api.schemas import NotificationSchema
from api.models.notifications import NotificationsModel


class NotificationsRepository:

    def create(self, schema: NotificationSchema) -> NotificationSchema:
        
        with Session() as session:
            try:
                notification = NotificationsModel()
                notification.status = schema.status
                notification.info = dumps(schema.info)
                notification.typeSend = schema.typeSend
                notification.responseServer = dumps(schema.responseServer)
                notification.createdAt = schema.createdAt
                notification.endIn = schema.endIn

                session.add(notification)
                session.commit()        
                return schema
            
            except IntegrityError as exc:
                session.rollback()
                raise EntityValidationError(f"Erro de integridade: {str(exc)}")
            
            except Exception as exc:
                session.rollback()
                raise UnknownError(f"Erro desconhecido: {str(exc)}")

    def select_by_id(self, idSend: str) -> NotificationSchema:
        with Session() as session:
            try:
                notification = session.query(NotificationsModel).filter(NotificationsModel.idSend == idSend).first()

                if not notification:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                
                return NotificationSchema.model_validate(notification)

            except Exception as exc:
                raise exc

    def select_all(self) -> List[NotificationSchema]:
        with Session() as session:
            try:
                notifications = session.query(NotificationsModel).all()

                if not notifications:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                
                schemas = []
                for row in notifications:
                    schemas.append(NotificationSchema.model_validate(row))
                return schemas

            except Exception as exc:
                raise exc
            
    def delete(self, idSend: str) -> None:
        with Session() as session:
            try:
                notification = session.query(NotificationsModel).filter(NotificationsModel.idSend == idSend).first()

                if not notification:
                    raise NotFoundError("Nenhuma notificação encontrada.")
            
                session.delete(notification)
                session.commit()

            except Exception as exc:
                session.rollback()
                raise exc

            
        