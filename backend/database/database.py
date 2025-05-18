from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from backend.models import models

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://todo_admin:todo_password@db:5432/todo"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db