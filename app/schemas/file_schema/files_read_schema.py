from pydantic import RootModel
from typing import List

from app.schemas.file_schema.file_read_schema import FileReadSchema

class FilesReadSchema(RootModel[List[FileReadSchema]]):
    pass

