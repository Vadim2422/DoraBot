from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declarative_base

Base = declarative_base()

# url = config.postgres.get_url()
# docker
postgres_url = "postgresql+asyncpg://admin:admin@postgres/postgres"
# localhost
# url = "postgresql+asyncpg://admin:admin@localhost:8084/db"

sqlite_url = "sqlite+aiosqlite:///db/dora.db"


def create_async_engine_(url):
    return create_async_engine(url, echo=True)


engine = create_async_engine_(sqlite_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


