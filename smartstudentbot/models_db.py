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
