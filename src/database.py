from typing import Annotated
from collections.abc import AsyncIterator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings



engine = create_async_engine(settings.DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]