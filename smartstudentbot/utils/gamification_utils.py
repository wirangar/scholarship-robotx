from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from utils.db_utils import AsyncSessionLocal
from models_db import UserPoints, Badge, UserBadge
from utils.logger import logger

async def add_points(user_id: int, points_to_add: int):
    """
    Adds a specified number of points to a user's score.
    Creates a points record if one does not exist.
    """
    if not AsyncSessionLocal:
        logger.error("Database not initialized. Cannot add points.")
        return

    async with AsyncSessionLocal() as session:
        try:
            # Find the user's points record
            stmt = select(UserPoints).where(UserPoints.user_id == user_id)
            result = await session.execute(stmt)
            user_points = result.scalar_one_or_none()

            if user_points:
                user_points.points += points_to_add
            else:
                # If no record exists, create one
                user_points = UserPoints(user_id=user_id, points=points_to_add)
                session.add(user_points)

            await session.commit()
            logger.info(f"Awarded {points_to_add} points to user {user_id}. New total: {user_points.points}")

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error while adding points for user {user_id}: {e}")

async def award_badge(user_id: int, badge_name: str):
    """
    Awards a badge to a user if they don't already have it.
    """
    if not AsyncSessionLocal:
        logger.error("Database not initialized. Cannot award badge.")
        return

    async with AsyncSessionLocal() as session:
        try:
            # First, find the badge ID from its name
            badge_stmt = select(Badge).where(Badge.name == badge_name)
            badge_result = await session.execute(badge_stmt)
            badge = badge_result.scalar_one_or_none()

            if not badge:
                logger.warning(f"Attempted to award non-existent badge: {badge_name}")
                return

            # Check if the user already has this badge
            user_badge_stmt = select(UserBadge).where(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge.id
            )
            user_badge_result = await session.execute(user_badge_stmt)
            existing_user_badge = user_badge_result.scalar_one_or_none()

            if existing_user_badge:
                # User already has the badge, do nothing
                return

            # Award the new badge
            new_user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
            session.add(new_user_badge)
            await session.commit()
            logger.info(f"Awarded badge '{badge_name}' to user {user_id}")

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error while awarding badge for user {user_id}: {e}")

async def get_user_profile(user_id: int) -> (int, list):
    """
    Retrieves a user's points and the names/icons of the badges they have earned.
    """
    if not AsyncSessionLocal:
        return 0, []

    async with AsyncSessionLocal() as session:
        try:
            # Get points
            points_stmt = select(UserPoints.points).where(UserPoints.user_id == user_id)
            points_result = await session.execute(points_stmt)
            points = points_result.scalar_one_or_none() or 0

            # Get badges
            badge_stmt = select(Badge.name, Badge.icon).join(UserBadge).where(UserBadge.user_id == user_id)
            badge_result = await session.execute(badge_stmt)
            badges = badge_result.all() # Returns a list of Row objects

            return points, badges
        except Exception as e:
            logger.error(f"Database error while fetching profile for user {user_id}: {e}")
            return 0, []
