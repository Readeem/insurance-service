from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

__all__ = (
    "Engine",
    "database",
)

# DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/insurance"
DATABASE_URL = "sqlite+aiosqlite:///database.db"

Engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


async def database() -> AsyncGenerator[AsyncSession, None]:
    session = sessionmaker(  # type: ignore  # ignore async engine warning
        Engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with session() as db:
        yield db
