from pydantic import RootModel
from typing import List

from app.schemas.email_schema.attachment_schema import AttachmentSchema

class AttachmentsSchema(RootModel[List[AttachmentSchema]]): pass