import strawberry
from typing import List

from api.repositories import NotificationsRepository

from api.graphql.types import NotificationType, ApiResponseType, ApiErrorType
from api.graphql.utils import build_response

@strawberry.type
class Query:
    
    @strawberry.field
    def selectById(self, idSend: str) -> ApiResponseType[NotificationType, ApiErrorType]:
        try:
            notification_repository = NotificationsRepository()
        
            return build_response(
                success=True,
                data=notification_repository.select_by_id(idSend)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.field
    def selectAll(self) -> ApiResponseType[List[NotificationType], ApiErrorType]:
        try:
            notification_repository = NotificationsRepository()
            return build_response(
                success=True,
                data=notification_repository.select_all()
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

