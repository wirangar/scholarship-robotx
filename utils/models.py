# -*- coding: utf-8 -*-
"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """
    Represents a registered user in the database.
    """
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True) # Telegram User ID
    full_name = Column(String, nullable=False)
    age = Column(Integer)
    country = Column(String)
    major = Column(String)
    email = Column(String, unique=True, index=True)
    language = Column(String, default='fa')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RoommateProfile(Base):
    """
    Represents a user's roommate profile.
    """
    __tablename__ = "roommate_profiles"

    user_id = Column(BigInteger, primary_key=True, index=True) # Foreign key to User.id
    username = Column(String) # Telegram username
    budget = Column(Integer, index=True)
    location = Column(String)
    habits = Column(String)
    bio = Column(String)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
