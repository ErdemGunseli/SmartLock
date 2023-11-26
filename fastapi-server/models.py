# Data models inherit from Base and correspond to database tables:
from database import Base

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    admin = Column(Boolean, default=False)
    key = Column(String, unique=True, index=True)

    # Declaring the relationship between user and action_log:
    action_logs = relationship("ActionLog", back_populates="user")


class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="action_logs")