import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

__all__ = (
    "Engine",
    "database",
)

DATABASE_URL: str = (
    "postgresql+asyncpg://"
    f"{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}"
    f"@{os.getenv("POSTGRES_ADDRESS", "localhost")}:{os.getenv("POSTGRES_PORT", "5432")}"
    f"/{os.getenv("POSTGRES_DB")}"
)

Engine: AsyncEngine = create_async_engine(DATABASE_URL)


async def database() -> AsyncGenerator[AsyncSession, None]:
    session = sessionmaker(  # type: ignore  # ignore async engine warning
        Engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with session() as db:
        yield db
