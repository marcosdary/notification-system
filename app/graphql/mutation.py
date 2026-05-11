import strawberry

from app.graphql.permissions import ApiKeyPermission
from app.graphql.mutations import EmailMutation

@strawberry.type
class Mutation(EmailMutation):

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def emails(
        self
    ) -> EmailMutation:
       return EmailMutation()