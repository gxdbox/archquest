"""
SQLAlchemy 数据库模型定义
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """玩家用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    avatar = Column(String(100), default="🧑‍💻")
    title = Column(String(100), default="初级架构师")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    progress = relationship("Progress", back_populates="user", uselist=False)
    skills = relationship("Skill", back_populates="user")


class Progress(Base):
    """玩家进度表"""
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_level = Column(Integer, default=1)  # 当前关卡 1-4
    current_stage = Column(Integer, default=1)  # 当前阶段
    experience = Column(Integer, default=0)
    player_level = Column(Integer, default=1)  # 玩家等级 1-20
    total_score = Column(Integer, default=0)
    quests_completed = Column(Integer, default=0)
    game_state = Column(JSON, default=dict)  # 存储游戏状态
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = relationship("User", back_populates="progress")


class Skill(Base):
    """玩家技能表"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    skill_level = Column(Integer, default=0)
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime, nullable=True)
    
    # 关联
    user = relationship("User", back_populates="skills")


class GameLog(Base):
    """游戏日志表"""
    __tablename__ = "game_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer, nullable=False)
    stage = Column(Integer, nullable=False)
    player_answer = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    score = Column(Integer, default=0)
    passed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
