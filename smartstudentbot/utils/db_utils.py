from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from aiogram import types

from config import DATABASE_URL, SQLITE_DB
from models_db import Base, User
from utils.logger import logger

# Determine the database URL
if DATABASE_URL:
    DB_URL = DATABASE_URL
    if DB_URL.startswith("postgres://"):
        DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    DB_URL = f"sqlite+aiosqlite:///./{SQLITE_DB}"

# Create the async engine
try:
    async_engine = create_async_engine(DB_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    logger.info(f"Successfully connected to the database: {async_engine.url.drivername}")
except ImportError as e:
    logger.error(f"Database driver error: {e}. Make sure 'asyncpg' or 'aiosqlite' is installed.")
    raise
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

async def get_session() -> AsyncSession:
    """Dependency to get a database session."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initializes the database by creating all tables."""
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")

async def get_or_create_user(tg_user: types.User) -> User:
    """
    Retrieves a user from the database by their Telegram ID,
    or creates a new user if they don't exist.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Query for the user by their Telegram user_id
            stmt = select(User).where(User.user_id == tg_user.id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                # Update user info if it has changed
                if (user.username != tg_user.username or
                    user.first_name != tg_user.first_name or
                    user.last_name != tg_user.last_name):
                    user.username = tg_user.username
                    user.first_name = tg_user.first_name
                    user.last_name = tg_user.last_name
                    await session.commit()
                    await session.refresh(user)
                    logger.info(f"User {tg_user.id} data updated.")
                return user

            # If user not found, create a new one
            new_user = User(
                user_id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                language_code=tg_user.language_code
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            logger.info(f"New user created: {tg_user.id} - {tg_user.username}")
            return new_user
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error while getting or creating user {tg_user.id}: {e}")
            return None
        except Exception as e:
            await session.rollback()
            logger.error(f"An unexpected error occurred for user {tg_user.id}: {e}")
            return None
