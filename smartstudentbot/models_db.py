import datetime
from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all database models.
    Includes support for asynchronous attributes.
    """
    pass

class User(Base):
    """
    Represents a user in the database.
    This table stores information about the users interacting with the bot.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, comment="Telegram User ID")
    username: Mapped[str] = mapped_column(String(32), nullable=True, comment="Telegram Username")
    first_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="Telegram First Name")
    last_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="Telegram Last Name")
    language_code: Mapped[str] = mapped_column(String(10), nullable=True, comment="Telegram Language Code")

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="Timestamp of user creation"
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp of last user update"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, user_id={self.user_id}, username='{self.username}')>"

class Feedback(Base):
    """
    Represents user feedback in the database.
    """
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, comment="Telegram User ID of the feedback provider")
    rating: Mapped[int] = mapped_column(nullable=True, comment="A numeric rating, e.g., 1-5")
    text: Mapped[str] = mapped_column(String(1024), nullable=True, comment="The feedback text content")

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="Timestamp of feedback submission"
    )

from sqlalchemy import ForeignKey

    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, user_id={self.user_id}, rating={self.rating})>"

class UserPoints(Base):
    """
    Stores the points for each user.
    """
    __tablename__ = "user_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), unique=True, index=True)
    points: Mapped[int] = mapped_column(default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<UserPoints(user_id={self.user_id}, points={self.points})>"

class Badge(Base):
    """
    Defines the available badges in the system.
    """
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="e.g., 'First Feedback'")
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str] = mapped_column(String(10), nullable=False, comment="An emoji for the badge")

    def __repr__(self) -> str:
        return f"<Badge(name='{self.name}')>"

class UserBadge(Base):
    """
    Association table linking users to the badges they have earned.
    """
    __tablename__ = "user_badges"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), index=True)
    badge_id: Mapped[int] = mapped_column(ForeignKey("badges.id"), index=True)

    awarded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
