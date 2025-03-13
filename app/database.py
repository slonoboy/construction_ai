from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import Base


DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./sql_app.db"
DATABASE_URL_SYNC = "sqlite:///./sql_app.db"


engine = create_async_engine(DATABASE_URL_ASYNC)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session


Base.metadata.create_all(bind=create_engine(DATABASE_URL_SYNC))
