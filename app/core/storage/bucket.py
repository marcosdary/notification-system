from supabase import create_async_client, AsyncClient, acreate_client, create_client

from app.core.config import settings

def get_sync_client_supabase():
    return create_client(
        supabase_key=settings.SUPABASE_KEY,
        supabase_url=settings.SUPABASE_URL
    )

async def get_client_supabase():
    return await acreate_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY
    )