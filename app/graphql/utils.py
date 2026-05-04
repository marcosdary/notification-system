from fastapi import Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_session

async def get_context(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    return {
        "request": request,
        "response": response,
        "session": session
    }