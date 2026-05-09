import strawberry

from app.graphql.permissions import ApiKeyPermission
from app.graphql.mutations.email_process_mutation import EmailProcessMutation

@strawberry.type
class EmailMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def emails(
        self
    ) -> EmailProcessMutation:
       return EmailProcessMutation()

