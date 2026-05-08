from supabase import create_async_client, AsyncClient, acreate_client

from app.core.config import settings

async def get_client_supabase():
    return await acreate_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY
    )