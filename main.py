from app.core.storage import supabase_client
from app.core.constants import UPLOADS_DIR
from app.core.config import settings

file = "webminar.jpg"

path = UPLOADS_DIR / file

with open(path, "rb") as f:
    response = (
        supabase_client
        .storage
        .from_(settings.BUCKET_FILES_PUBLIC)
        .upload(
            path=file,
            file=f,
        )
    )   