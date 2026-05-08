from pydantic import RootModel
from typing import List

from app.schemas.file_schema.file_upload_schema import FileUploadSchema

class FilesUploadSchema(RootModel[List[FileUploadSchema]]):
    pass

