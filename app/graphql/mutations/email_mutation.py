import strawberry
from strawberry.exceptions import StrawberryGraphQLError

from app.graphql.inputs import EmailInput
from app.schemas.email_schema import EmailSchema, EmailResponseSchema
from app.graphql.types import EmailResponseType
from app.tasks import process_send_email

@strawberry.type
class EmailMutation:

    @strawberry.mutation
    async def send(
        self,
        schema: EmailInput
    ) -> EmailResponseType:
        try:
            data: EmailSchema = schema.to_pydantic()
            task = process_send_email.delay(data.model_dump())
            return EmailResponseSchema(
                id_task=task.id
            )

        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))

