import strawberry
from strawberry.exceptions import StrawberryGraphQLError

from app.graphql.types import EmailResponseType

from app.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailQuery:
    
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def select_by_id(self, id: str) -> EmailResponseType:
        try:
            return {}
        
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc))

        
   



