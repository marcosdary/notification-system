from typing import List

from app.schemas.webhook_schema.base import BaseWebhookSchema
from app.schemas.webhook_schema.read import ReadWebhookSchema

class ListWebhookSchema(BaseWebhookSchema):
    info: List[ReadWebhookSchema] | None = [] 