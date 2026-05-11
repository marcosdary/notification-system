from sqlalchemy import delete

from app.celery import celery_app
from app.core.storage import get_sync_client_supabase
from app.models import FileModel
from app.repositories import FileRepository

from app.core.config import settings
from app.core.constants import StatusFile
from app.core.config.database import SessionLocalSync

@celery_app.task
def process_files_delete():
    with SessionLocalSync() as session:
        file_repo = FileRepository(session)
       
        files = file_repo.get_all()
        paths = [
            file.path
            for file in files
        ]

        if paths:
            client_supabase = get_sync_client_supabase()
            storage = client_supabase.storage.from_(settings.BUCKET_FILES_PUBLIC)
            
            storage.remove(paths=paths)
            
           
        session.execute(
            delete(FileModel).where(FileModel.status == StatusFile.used)
        )

        session.commit()


       
        

        