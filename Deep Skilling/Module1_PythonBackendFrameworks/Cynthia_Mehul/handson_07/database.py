from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL="sqlite+aiosqlite:///./courses.db"
engine=create_async_engine(DATABASE_URL, echo=True)
Base=declarative_base()

sessionLocal=async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
