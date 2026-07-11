from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL="sqlite+aiosqlite:///./users.db"
engine=create_async_engine(DATABASE_URL, echo=True)

sessionLocal=async_sessionmaker(bind=engine, 
            class_=AsyncSession, expire_on_commit=False)

