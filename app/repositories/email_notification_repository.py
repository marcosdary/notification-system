from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, and_, func
from time import time
from datetime import datetime

from app.core import LOGGER as logger
from app.config import SessionLocalAsync as SessionAsync, SessionLocalSync as SessionSync
from app.constants import StatusEmail, SendType
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
from app.schemas import PaginationSchema, DateRangeSchema
from app.models import EmailNotificationsModel


class EmailNotificationRepository:


    def __init__(self):
        self.__table = "email_notification"

    def _build_filters(
        self,
        date_range: DateRangeSchema | None,
        status_email: StatusEmail | None,
        send_type: SendType | None,
        date: datetime | None
    ) -> list:
        filters = []
                
        if date_range:
            filters.append(
                EmailNotificationsModel.createdAt.between(
                date_range.startDate,
                date_range.endDate
            )
        )

        if status_email:
            filters.append(EmailNotificationsModel.status == status_email)
                
        if send_type:
            filters.append(EmailNotificationsModel.sendType == send_type)

        if date:
            filters.append(func.date(EmailNotificationsModel.createdAt) == date)

        return filters

    async def _count(self, session, filters: list) -> int:
        count_query = select(func.count()).select_from(EmailNotificationsModel)
        if filters:
            count_query = count_query.where(and_(*filters))
        return await session.scalar(count_query)
    
    def _build_query(self, filters: list, pagination: PaginationSchema):
        query = select(EmailNotificationsModel)

        if filters:
            query = query.where(and_(*filters))

        if filters:
            query = query.where(and_(*filters))

        if not pagination.all_:
            offset = (pagination.page - 1) * pagination.limit
            query = query.offset(offset).limit(pagination.limit)

        return query.order_by(EmailNotificationsModel.createdAt.desc())

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

    async def select_filter_all(
        self, 
        pagination: PaginationSchema, 
        date_range: DateRangeSchema = None,
        status_email: StatusEmail = None, 
        send_type: SendType = None,
        date: datetime = None
    ) -> ListEmailNotificationSchema:
        repository = "EmailNotificationRepository.select_filter_all"

        logger.info(
            "Buscando lista de email notifications.",
            extra={
                "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_ALL_START",
                "repository": repository,
                "layer": "repository",
                "filter_by": {
                    "pagination": pagination.model_dump(),
                    "date_range": date_range.model_dump() if date_range else None,
                    "send_type": send_type,
                    "status_email": status_email
                },
                "table": self.__table,
            }
        )

        async with SessionAsync() as session:
            try:
                start = time()    

                filters = self._build_filters(date_range, status_email, send_type, date)          

                total = await self._count(session, filters)
                
                query = self._build_query(filters, pagination)

                stmt = await session.execute(query)
                records = stmt.scalars().all()

                if not records:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                
                execution = time() - start

                logger.info(
                    "Lista de email notifications retornada com sucesso.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_FILTER_ALL_SUCCESS",
                        "repository": repository,
                        "rows": len(records),
                        "layer": "repository",
                        "execution_time": execution,
                        "filter_by": {
                            "pagination": pagination.model_dump(),
                            "date_range": date_range.model_dump() if date_range else None,
                            "send_type": send_type,
                            "status_email": status_email
                        },
                        "table": self.__table,
                    }
                )

                return ListEmailNotificationSchema(
                        items=[
                            ReadEmailNotificationSchema.model_validate(row)
                            for row in records
                        ],
                        limit=pagination.limit,
                        page=pagination.page,
                        total=total,
                        hasNextPage=(pagination.page * pagination.limit) < total
                )
            
            except Exception as exc:
                logger.exception(
                    "Erro ao buscar lista de email notifications.",
                    extra={
                        "event": "EMAIL_NOTIFICATION_REPOSITORY_SELECT_FILTER_ALL_ERROR",
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