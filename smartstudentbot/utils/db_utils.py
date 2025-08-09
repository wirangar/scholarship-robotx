from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from aiogram import types

from config import DATABASE_URL, SQLITE_DB
from models_db import Base, User
from utils.logger import logger

# This is the simpler implementation that is easier to test
DB_URL = DATABASE_URL if DATABASE_URL else f"sqlite+aiosqlite:///./{SQLITE_DB}"
if "postgres://" in DB_URL:
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)

try:
    async_engine = create_async_engine(DB_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    logger.info(f"Successfully connected to the database: {async_engine.url.drivername}")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    async_engine = None
    AsyncSessionLocal = None

async def init_db():
    """Initializes the database by creating all tables."""
    if not async_engine:
        logger.error("Database engine not initialized. Skipping DB initialization.")
        return
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully.")

async def get_or_create_user(tg_user: types.User) -> User | None:
    if not AsyncSessionLocal:
        logger.error("Database not initialized. Cannot get or create user.")
        return None
    async with AsyncSessionLocal() as session:
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
            return user

        from utils.gamification_utils import add_points
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
        logger.info(f"New user created: {tg_user.id}")

        # Award points for registering
        await add_points(tg_user.id, 10) # e.g., 10 points for joining

        return new_user

async def update_user_language(user_id: int, lang_code: str):
    if not AsyncSessionLocal:
        logger.error("Database not initialized. Cannot update language.")
        return
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.user_id == user_id)
        user = await session.scalar(stmt)
        if user:
            user.language_code = lang_code
            await session.commit()
            logger.info(f"Updated language for user {user_id} to {lang_code}")

async def get_user_language(user_id: int) -> str:
    """
    Retrieves the language_code for a specific user.
    Defaults to 'en' if the user or language code is not found.
    """
    if not AsyncSessionLocal:
        logger.error("Database not initialized. Defaulting language to 'en'.")
        return 'en'
    async with AsyncSessionLocal() as session:
        stmt = select(User.language_code).where(User.user_id == user_id)
        lang_code = await session.scalar(stmt)
        return lang_code if lang_code else 'en'

async def save_feedback(user_id: int, rating: int, text: str):
    """
    Saves a new feedback entry to the database.
    """
    if not AsyncSessionLocal:
        logger.error("Database not initialized. Cannot save feedback.")
        return

    new_feedback = Feedback(user_id=user_id, rating=rating, text=text)
    async with AsyncSessionLocal() as session:
        try:
            session.add(new_feedback)
            await session.commit()
            logger.info(f"Saved feedback from user {user_id}")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error while saving feedback for user {user_id}: {e}")
