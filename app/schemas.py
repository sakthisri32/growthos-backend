from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Auth / Users ----------

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str


class GoogleAuth(BaseModel):
    id_token: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    is_verified: bool
    theme: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserUpdate(BaseModel):
    name: Optional[str] = None
    theme: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


# ---------- Tasks ----------

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = "medium"
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    completed: bool
    created_at: datetime


# ---------- Timetable ----------

class TimetableBase(BaseModel):
    title: str
    day_of_week: Optional[int] = None
    date: Optional[date] = None
    start_time: str
    end_time: str
    color: Optional[str] = "#7C3AED"
    recurrence: Optional[str] = "weekly"


class TimetableCreate(TimetableBase):
    pass


class TimetableUpdate(BaseModel):
    title: Optional[str] = None
    day_of_week: Optional[int] = None
    date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    color: Optional[str] = None
    recurrence: Optional[str] = None


class TimetableOut(TimetableBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


# ---------- Skills ----------

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    level: Optional[str] = "beginner"
    progress_percent: Optional[int] = 0
    learning_hours: Optional[float] = 0
    milestones: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    progress_percent: Optional[int] = None
    learning_hours: Optional[float] = None
    milestones: Optional[str] = None


class SkillOut(SkillBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime


# ---------- Habits ----------

class HabitBase(BaseModel):
    name: str
    icon: Optional[str] = "check"
    target_per_day: Optional[int] = 1


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    target_per_day: Optional[int] = None


class HabitOut(HabitBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    current_streak: int
    longest_streak: int
    logs: Optional[str] = None
    created_at: datetime


# ---------- Goals ----------

class GoalBase(BaseModel):
    title: str
    term: Optional[str] = "daily"
    target_date: Optional[date] = None


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    term: Optional[str] = None
    target_date: Optional[date] = None
    completion_percent: Optional[int] = None
    completed: Optional[bool] = None


class GoalOut(GoalBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    completion_percent: int
    completed: bool
    created_at: datetime


# ---------- Journal ----------

class JournalBase(BaseModel):
    date: Optional[date] = None
    todays_learning: Optional[str] = None
    problems_faced: Optional[str] = None
    ideas: Optional[str] = None
    tomorrow_plan: Optional[str] = None
    mood: Optional[str] = None
    tags: Optional[str] = None


class JournalCreate(JournalBase):
    pass


class JournalUpdate(JournalBase):
    pass


class JournalOut(JournalBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


# ---------- Projects ----------

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "planning"
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    tech_stack: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    tech_stack: Optional[str] = None


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime


# ---------- Research ----------

class ResearchBase(BaseModel):
    topic: str
    paper_title: Optional[str] = None
    link: Optional[str] = None
    notes: Optional[str] = None
    ideas: Optional[str] = None
    is_bookmarked: Optional[bool] = False


class ResearchCreate(ResearchBase):
    pass


class ResearchUpdate(BaseModel):
    topic: Optional[str] = None
    paper_title: Optional[str] = None
    link: Optional[str] = None
    notes: Optional[str] = None
    ideas: Optional[str] = None
    is_bookmarked: Optional[bool] = None


class ResearchOut(ResearchBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime


# ---------- Startup Ideas ----------

class StartupBase(BaseModel):
    title: str
    problem: Optional[str] = None
    solution: Optional[str] = None
    market: Optional[str] = None
    competitors: Optional[str] = None
    revenue_model: Optional[str] = None
    mvp: Optional[str] = None
    status: Optional[str] = "idea"


class StartupCreate(StartupBase):
    pass


class StartupUpdate(BaseModel):
    title: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    market: Optional[str] = None
    competitors: Optional[str] = None
    revenue_model: Optional[str] = None
    mvp: Optional[str] = None
    status: Optional[str] = None


class StartupOut(StartupBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime


# ---------- Reading List ----------

class ReadingBase(BaseModel):
    title: str
    type: Optional[str] = "book"
    link: Optional[str] = None
    completion_percent: Optional[int] = 0


class ReadingCreate(ReadingBase):
    pass


class ReadingUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    link: Optional[str] = None
    completion_percent: Optional[int] = None


class ReadingOut(ReadingBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime


# ---------- Achievements ----------

class AchievementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    badge_key: str
    title: str
    description: Optional[str] = None
    unlocked_at: datetime


# ---------- Notifications ----------

class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    type: str
    message: str
    is_read: bool
    created_at: datetime


# ---------- Analytics ----------

class AnalyticsSummary(BaseModel):
    total_tasks: int
    completed_tasks: int
    task_completion_rate: float
    total_skills: int
    avg_skill_progress: float
    total_learning_hours: float
    habit_count: int
    best_habit_streak: int
    goals_completed: int
    goals_total: int
    daily_hours: List[dict]
    weekly_progress: List[dict]
    skill_breakdown: List[dict]


# ---------- AI Coach ----------

class AICoachRequest(BaseModel):
    hours_available: float
    focus_area: Optional[str] = None
    message: Optional[str] = None


class AICoachResponse(BaseModel):
    plan: str
    suggested_tasks: List[str]
