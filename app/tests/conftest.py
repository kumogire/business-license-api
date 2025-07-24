import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import pytest_asyncio

from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.core.config import settings

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session"""
    async with test_engine.begin() as conn:
        await conn.execute("DROP TABLE IF EXISTS business_licenses")
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def override_get_db(db_session: AsyncSession):
    """Override the get_db dependency"""
    async def _override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac