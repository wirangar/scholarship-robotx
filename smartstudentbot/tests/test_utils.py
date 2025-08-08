import pytest
from unittest.mock import patch, MagicMock
from aiogram import types
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import from the local package structure
from models_db import Base
from utils.db_utils import get_or_create_user, update_user_language

# In-memory SQLite database URL for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="module")
async def test_engine():
    """Create an in-memory SQLite engine for the test module."""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(test_engine):
    """Create a new session for each test, with rollback."""
    Session = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
        await session.rollback()

# This patch will replace the engine creation in db_utils for all tests in this module
@pytest.fixture(scope="module", autouse=True)
def patch_db_engine(test_engine):
    """Patches the db_utils.async_engine with the test engine."""
    with patch('utils.db_utils.async_engine', test_engine):
        yield

@pytest.mark.asyncio
async def test_get_or_create_user_new(db_session):
    """Test creating a new user."""
    from models_db import User
    # Since we've patched the engine, db_utils will use it.
    # We need to ensure the session used by the function is our test session.
    with patch('utils.db_utils.AsyncSessionLocal', return_value=db_session):
        tg_user = types.User(id=12345, is_bot=False, first_name="John", last_name="Doe", username="johndoe")
        user_in_db = await get_or_create_user(tg_user)

        assert user_in_db is not None
        assert user_in_db.user_id == 12345

        # Verify in DB
        from sqlalchemy import select
        stmt = select(User).where(User.user_id == 12345)
        result = await db_session.execute(stmt)
        retrieved_user = result.scalar_one()
        assert retrieved_user.first_name == "John"

@pytest.mark.asyncio
async def test_get_or_create_user_existing(db_session):
    """Test retrieving an existing user."""
    from models_db import User
    initial_user = User(user_id=54321, first_name="Jane", username="janedoe")
    db_session.add(initial_user)
    await db_session.commit()
    await db_session.refresh(initial_user)

    with patch('utils.db_utils.AsyncSessionLocal', return_value=db_session):
        tg_user = types.User(id=54321, is_bot=False, first_name="Jane", username="janedoe")
        user_in_db = await get_or_create_user(tg_user)
        assert user_in_db.id == initial_user.id

@pytest.mark.asyncio
async def test_get_or_create_user_update(db_session):
    """Test updating an existing user's info."""
    from models_db import User
    initial_user = User(user_id=67890, first_name="OldName", username="old_username")
    db_session.add(initial_user)
    await db_session.commit()

    with patch('utils.db_utils.AsyncSessionLocal', return_value=db_session):
        updated_tg_user = types.User(id=67890, is_bot=False, first_name="NewName", username="new_username")
        user_in_db = await get_or_create_user(updated_tg_user)
        assert user_in_db.first_name == "NewName"
        await db_session.refresh(user_in_db)
        assert user_in_db.first_name == "NewName"
