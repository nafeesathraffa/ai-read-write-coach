from sqlalchemy import String, Text, Boolean, DateTime, func, ForeignKey, Integer, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
  is_demo: Mapped[bool]  = mapped_column(Boolean, default=False)
  goals: Mapped[str | None] = mapped_column(Text, nullable=True)
  current_focus: Mapped[str | None] = mapped_column(Text, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class PracticeSession(Base):
  __tablename__ = "practice_sessions"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
  kind: Mapped[str] = mapped_column(String(30), nullable=False)
  subtype: Mapped[str | None] = mapped_column(String(30), nullable=True)
  started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Attempt(Base):
  __tablename__ = "attempts"

  id: Mapped[int] = mapped_column(primary_key=True) 
  practice_session_id: Mapped[int] = mapped_column(ForeignKey('practice_sessions.id'), nullable=False)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
  parent_attempt_id: Mapped[int | None] = mapped_column(ForeignKey('attempts.id'), nullable=True)
  role: Mapped[str] = mapped_column(String(20), nullable=False)
  input_text: Mapped[str] = mapped_column(Text, nullable=False)
  input_method: Mapped[str] = mapped_column(String(20), nullable=False)
  prep_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
  speak_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
  target_criterion: Mapped[str | None] = mapped_column(String(50), nullable=True)
  crisis_flag: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Evaluation(Base):
  __tablename__ = "evaluations"

  id: Mapped[int] = mapped_column(primary_key=True)
  attempt_id: Mapped[int] = mapped_column(ForeignKey('attempts.id'), unique=True, nullable=False)
  rubric_version: Mapped[str] = mapped_column(String(20), nullable=False)
  prompt_version: Mapped[str] = mapped_column(String(20), nullable=False)
  schema_version: Mapped[str] = mapped_column(String(20), nullable=False)
  model_id: Mapped[str] = mapped_column(String(100), nullable=False)  
  temperature: Mapped[float | None] = mapped_column(nullable=True)
  criteria_json: Mapped[dict] = mapped_column(JSON, nullable=False)
  raw_model_output: Mapped[str | None] = mapped_column(Text, nullable=True)
  deterministic_metrics_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class UsageEvent(Base):
  __tablename__ = "usage_events"

  id: Mapped[int] = mapped_column(primary_key=True)
  model_id: Mapped[str] = mapped_column(String(100), nullable=False)
  prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
  completion_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
  purpose: Mapped[str] = mapped_column(String(50), nullable=False)
  user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class CrisisEvent(Base):
  __tablename__ = "crisis_events"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
  attempt_id: Mapped[int] = mapped_column(ForeignKey('attempts.id'), nullable=False)
  category: Mapped[str] = mapped_column(String(50), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  