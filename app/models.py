import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Boolean, Integer, Float, DateTime, ForeignKey, Text, Enum, Date
)
from sqlalchemy.orm import relationship
from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # null if Google-only account
    google_id = Column(String, unique=True, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    theme = Column(String, default="dark")
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    timetable_entries = relationship("TimetableEntry", back_populates="owner", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="owner", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="owner", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="owner", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    research_items = relationship("ResearchItem", back_populates="owner", cascade="all, delete-orphan")
    startup_ideas = relationship("StartupIdea", back_populates="owner", cascade="all, delete-orphan")
    reading_items = relationship("ReadingItem", back_populates="owner", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="owner", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    priority = Column(String, default="medium")  # low | medium | high
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="tasks")


class TimetableEntry(Base):
    __tablename__ = "timetable"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    day_of_week = Column(Integer, nullable=True)  # 0=Mon..6=Sun, null for one-off
    date = Column(Date, nullable=True)
    start_time = Column(String, nullable=False)  # "HH:MM"
    end_time = Column(String, nullable=False)
    color = Column(String, default="#7C3AED")
    recurrence = Column(String, default="weekly")  # daily | weekly | monthly | once

    owner = relationship("User", back_populates="timetable_entries")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)  # e.g. AI, Web, Cloud
    level = Column(String, default="beginner")  # beginner | intermediate | advanced
    progress_percent = Column(Integer, default=0)
    learning_hours = Column(Float, default=0)
    milestones = Column(Text, nullable=True)  # JSON-encoded list
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="skills")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    icon = Column(String, default="check")
    target_per_day = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    logs = Column(Text, nullable=True)  # JSON-encoded list of completed dates
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="habits")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    term = Column(String, default="daily")  # daily | weekly | monthly | yearly | long_term | short_term
    target_date = Column(Date, nullable=True)
    completion_percent = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="goals")


class JournalEntry(Base):
    __tablename__ = "journal"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=datetime.utcnow)
    todays_learning = Column(Text, nullable=True)
    problems_faced = Column(Text, nullable=True)
    ideas = Column(Text, nullable=True)
    tomorrow_plan = Column(Text, nullable=True)
    mood = Column(String, nullable=True)  # great | good | neutral | bad | terrible
    tags = Column(String, nullable=True)  # comma separated

    owner = relationship("User", back_populates="journal_entries")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="planning")  # planning | in_progress | completed | archived
    github_link = Column(String, nullable=True)
    demo_link = Column(String, nullable=True)
    tech_stack = Column(String, nullable=True)  # comma separated
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="projects")


class ResearchItem(Base):
    __tablename__ = "research"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)
    paper_title = Column(String, nullable=True)
    link = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    ideas = Column(Text, nullable=True)
    is_bookmarked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="research_items")


class StartupIdea(Base):
    __tablename__ = "startup_ideas"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    problem = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    market = Column(Text, nullable=True)
    competitors = Column(Text, nullable=True)
    revenue_model = Column(Text, nullable=True)
    mvp = Column(Text, nullable=True)
    status = Column(String, default="idea")  # idea | validating | building | launched
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="startup_ideas")


class ReadingItem(Base):
    __tablename__ = "reading_list"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, default="book")  # book | blog | paper | video
    link = Column(String, nullable=True)
    completion_percent = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="reading_items")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    badge_key = Column(String, nullable=False)  # e.g. "30_day_streak"
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="achievements")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(String, default="task_reminder")  # task_reminder | goal_reminder | quote | achievement
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="notifications")
