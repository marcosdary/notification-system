from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from time import time

from app.core import LOGGER as logger
from app.config import SessionLocalAsync as SessionAsync, SessionLocalSync as SessionSync
from app.constants import StatusEmail
from app.exceptions import (
    EntityValidationError,
    UnknownError,
    NotFoundError,
    ForbiddenActionError
)
from app.schemas.email_notification_schema import (
    CreateEmailNotificationSchema,
    ReadEmailNotificationSchema,
    ListEmailNotificationSchema,
    UpdateEmailNotificationSchema,
)
from app.models import EmailNotificationsModel


class EmailNotificationRepository:


    def __init__(self):
        self.__table = "email_notification"

    async def create(self, schema: CreateEmailNotificationSchema) -> ReadEmailNotificationSchema:
        repository = "EmailNotificationRepository.create"

        async with SessionAsync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando criação de email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_CREATE_START",
                        "repository": repository,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                notif = EmailNotificationsModel(**schema.model_dump())
                session.add(notif)
                await session.commit()

                execution = time() - start

                logger.info(
                    "Email notification criada com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_CREATE_SUCCESS",
                        "repository": repository,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                return ReadEmailNotificationSchema.model_validate(notif)

            except IntegrityError as exc:
                await session.rollback()

                logger.exception(
                    "Erro de integridade ao criar email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_CREATE_ERROR_INTEGRITY",
                        "repository": repository,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise EntityValidationError("Erro de integridade nos dados.")

            except Exception as exc:
                await session.rollback()

                logger.exception(
                    "Erro inesperado ao criar email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_CREATE_ERROR",
                        "repository": repository,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise UnknownError("Erro desconhecido ao salvar dados.")

    async def select_by_id(self, idEmail: str) -> ReadEmailNotificationSchema:
        repository = "EmailNotificationRepository.select_by_id"

        async with SessionAsync() as session:
            start = time()

            try:
                logger.info(
                    "Buscando email notification por ID.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_BY_ID_START",
                        "repository": repository,
                        "idEmail": idEmail,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                stmt = await session.execute(
                    select(EmailNotificationsModel).where(
                        EmailNotificationsModel.idEmail == idEmail
                    )
                )

                notif = stmt.scalars().first()

                if not notif:
                    raise NotFoundError("Notificação não encontrada.")

                execution = time() - start

                logger.info(
                    "Email notification encontrada com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_BY_ID_SUCCESS",
                        "repository": repository,
                        "idEmail": idEmail,
                        "layer": "repository",
                        "execution_time": execution,
                        "table": self.__table,
                    }
                )

                return ReadEmailNotificationSchema.model_validate(notif)

            except Exception as exc:
                logger.exception(
                    "Erro ao buscar email notification por ID.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_BY_ID_ERROR",
                        "repository": repository,
                        "idEmail": idEmail,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise

    async def select_all(self, page: int = 1, limit: int = 5) -> ListEmailNotificationSchema:
        repository = "EmailNotificationRepository.select_all"

        async with SessionAsync() as session:
            start = time()

            try:
                logger.info(
                    "Buscando lista de email notifications.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_ALL_START",
                        "repository": repository,
                        "layer": "repository",
                        "filter_by": {"page": page, "limit": limit},
                        "table": self.__table,
                    }
                )

                offset = (page - 1) * limit

                stmt = await session.execute(
                    select(EmailNotificationsModel)
                    .order_by(EmailNotificationsModel.createdAt)
                    .offset(offset)
                    .limit(limit)
                )

                notifs = stmt.scalars().all()

                if not notifs:
                    raise NotFoundError("Nenhuma notificação encontrada.")

                execution = time() - start

                logger.info(
                    "Lista de email notifications retornada com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_ALL_SUCCESS",
                        "repository": repository,
                        "rows": len(notifs),
                        "layer": "repository",
                        "execution_time": execution,
                        "filter_by": {"page": page, "limit": limit},
                        "table": self.__table,
                    }
                )

                return ListEmailNotificationSchema(
                    notifications=[
                        ReadEmailNotificationSchema.model_validate(row)
                        for row in notifs
                    ]
                )

            except Exception as exc:
                logger.exception(
                    "Erro ao buscar lista de email notifications.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_ALL_ERROR",
                        "repository": repository,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise


    def update(self, schema: UpdateEmailNotificationSchema) -> ReadEmailNotificationSchema:
        repository = "EmailNotificationRepository.update"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Atualizando email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_UPDATE_START",
                        "repository": repository,
                        "idEmail": schema.idEmail,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                notif = session.query(EmailNotificationsModel).filter(
                    EmailNotificationsModel.idEmail == schema.idEmail
                ).first()

                if not notif:
                    raise NotFoundError("Notificação não encontrada.")

                for key, value in schema.model_dump().items():
                    setattr(notif, key, value)

                session.commit()

                execution = time() - start

                logger.info(
                    "Email notification atualizada com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_UPDATE_SUCCESS",
                        "repository": repository,
                        "idEmail": schema.idEmail,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                return ReadEmailNotificationSchema.model_validate(notif)

            except Exception as exc:
                session.rollback()

                logger.exception(
                    "Erro ao atualizar email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_UPDATE_ERROR",
                        "repository": repository,
                        "idEmail": schema.idEmail,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise


    async def delete(self, idEmail: str) -> None:
        repository = "EmailNotificationRepository.delete"

        async with SessionAsync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando deleção de email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_DELETE_START",
                        "repository": repository,
                        "idEmail": idEmail,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                stmt = await session.execute(
                    select(EmailNotificationsModel).where(
                        EmailNotificationsModel.idEmail == idEmail
                    )
                )

                notif = stmt.scalars().first()

                if not notif:
                    raise NotFoundError("Notificação não encontrada.")

                if notif.status == StatusEmail.PENDING:
                    raise ForbiddenActionError("Ação proibida para status PENDING.")

                await session.delete(notif)
                await session.commit()

                execution = time() - start

                logger.info(
                    "Email notification deletada com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_DELETE_SUCCESS",
                        "repository": repository,
                        "idEmail": idEmail,
                        "layer": "repository",
                        "execution_time": execution,
                        "table": self.__table,
                    }
                )

            except Exception as exc:
                await session.rollback()

                logger.exception(
                    "Erro ao deletar email notification.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_DELETE_ERROR",
                        "repository": repository,
                        "idEmail": idEmail,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise


    async def delete_all(self) -> None:
        repository = "EmailNotificationRepository.delete_all"

        async with SessionAsync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando deleção em massa de email notifications.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_DELETE_ALL_START",
                        "repository": repository,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                await session.execute(delete(EmailNotificationsModel))
                await session.commit()

                execution = time() - start

                logger.info(
                    "Email notifications deletadas com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_DELETE_ALL_SUCCESS",
                        "repository": repository,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

            except Exception as exc:
                await session.rollback()

                logger.exception(
                    "Erro ao deletar todas email notifications.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_DELETE_ALL_ERROR",
                        "repository": repository,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise