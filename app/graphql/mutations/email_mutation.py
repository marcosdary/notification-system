import strawberry
from strawberry.exceptions import StrawberryGraphQLError

from app.graphql.inputs import EmailInput
from app.core.constants import StatusEmail
from app.schemas.email_schema import EmailSchema, ResponseSchema
from app.graphql.types import EmailResponseType
from app.graphql.permissions import ApiKeyPermission
from app.tasks import process_send_email

@strawberry.type
class EmailMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def send(
        self,
        schema: EmailInput
    ) -> EmailResponseType:
        try:
            data: EmailSchema = schema.to_pydantic()
            task = process_send_email.delay(data.model_dump())
            return ResponseSchema(
                id=task.id,
                status=task.state,
                message="Enviado ao destinatário."
            )

        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))

    