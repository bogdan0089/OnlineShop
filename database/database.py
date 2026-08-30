from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

async_session_maker = sessionmaker(class_=AsyncSession, bind=async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise




