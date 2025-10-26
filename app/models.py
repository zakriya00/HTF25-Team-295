# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_admin = Column(Integer, default=0)
    messages = relationship("Message", back_populates="user")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    admin_username = Column(String, nullable=True)  # First user becomes admin

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    file_path = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    mentioned_users = Column(String, nullable=True)  # Comma-separated usernames
    is_deleted = Column(Integer, default=0)
    deleted_by = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="messages")

class MutedUser(Base):
    __tablename__ = "muted_users"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    username = Column(String)
    muted_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    study_streak = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    total_files_shared = Column(Integer, default=0)
    total_mentions = Column(Integer, default=0)
    total_helpful_answers = Column(Integer, default=0)
    last_active_date = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    user = relationship("User")

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)  # Emoji or icon name
    points_required = Column(Integer, default=0)
    criteria = Column(String)  # JSON string describing how to earn

class UserBadge(Base):
    __tablename__ = "user_badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    earned_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
    badge = relationship("Badge")

class DailyChallenge(Base):
    __tablename__ = "daily_challenges"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    title = Column(String)
    description = Column(String)
    challenge_type = Column(String)  # "trivia", "participation", "helpful"
    points_reward = Column(Integer, default=10)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("daily_challenges.id"))
    submission_data = Column(String)  # JSON string
    is_correct = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
    challenge = relationship("DailyChallenge")