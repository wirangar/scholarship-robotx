import pytest
from unittest.mock import patch
from aiogram import types
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import from the local package structure
from models_db import Base

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

@pytest.mark.asyncio
@patch('utils.db_utils.AsyncSessionLocal')
async def test_get_or_create_user_new(mock_session_local, db_session):
    """Test creating a new user."""
    mock_session_local.return_value.__aenter__.return_value = db_session

    from utils.db_utils import get_or_create_user
    from models_db import User

    tg_user = types.User(id=12345, is_bot=False, first_name="John", last_name="Doe", username="johndoe")

    user_in_db = await get_or_create_user(tg_user)

    assert user_in_db is not None
    assert user_in_db.user_id == 12345
    assert user_in_db.username == "johndoe"

    # Verify it's in the DB by querying by user_id
    from sqlalchemy import select
    stmt = select(User).where(User.user_id == 12345)
    result = await db_session.execute(stmt)
    retrieved_user = result.scalar_one()

    assert retrieved_user is not None
    assert retrieved_user.first_name == "John"

@pytest.mark.asyncio
@patch('utils.db_utils.AsyncSessionLocal')
async def test_get_or_create_user_existing(mock_session_local, db_session):
    """Test retrieving an existing user."""
    mock_session_local.return_value.__aenter__.return_value = db_session

    from utils.db_utils import get_or_create_user
    from models_db import User

    initial_user = User(user_id=54321, first_name="Jane", last_name="Doe", username="janedoe")
    db_session.add(initial_user)
    await db_session.commit()
    # The user object is expired after commit, need to refresh
    await db_session.refresh(initial_user)


    tg_user = types.User(id=54321, is_bot=False, first_name="Jane", last_name="Doe", username="janedoe")
    user_in_db = await get_or_create_user(tg_user)

    assert user_in_db is not None
    assert user_in_db.user_id == 54321
    assert user_in_db.id == initial_user.id

@pytest.mark.asyncio
@patch('utils.db_utils.AsyncSessionLocal')
async def test_get_or_create_user_update(mock_session_local, db_session):
    """Test updating an existing user's info."""
    mock_session_local.return_value.__aenter__.return_value = db_session

    from utils.db_utils import get_or_create_user
    from models_db import User

    initial_user = User(user_id=67890, first_name="OldName", username="old_username")
    db_session.add(initial_user)
    await db_session.commit()

    updated_tg_user = types.User(id=67890, is_bot=False, first_name="NewName", username="new_username")
    user_in_db = await get_or_create_user(updated_tg_user)

    assert user_in_db.first_name == "NewName"
    assert user_in_db.username == "new_username"

    await db_session.refresh(user_in_db)
    assert user_in_db.first_name == "NewName"
