from app import models, schemas
from app.routers.crud_factory import make_crud_router

tasks_router = make_crud_router(
    prefix="/api/tasks", tag="Tasks",
    model=models.Task, create_schema=schemas.TaskCreate,
    update_schema=schemas.TaskUpdate, out_schema=schemas.TaskOut,
    search_fields=["title", "description"], filter_fields=["priority"],
)

timetable_router = make_crud_router(
    prefix="/api/timetable", tag="Timetable",
    model=models.TimetableEntry, create_schema=schemas.TimetableCreate,
    update_schema=schemas.TimetableUpdate, out_schema=schemas.TimetableOut,
    search_fields=["title"], filter_fields=["recurrence"],
)

skills_router = make_crud_router(
    prefix="/api/skills", tag="Skills",
    model=models.Skill, create_schema=schemas.SkillCreate,
    update_schema=schemas.SkillUpdate, out_schema=schemas.SkillOut,
    search_fields=["name", "category"], filter_fields=["level"],
)

goals_router = make_crud_router(
    prefix="/api/goals", tag="Goals",
    model=models.Goal, create_schema=schemas.GoalCreate,
    update_schema=schemas.GoalUpdate, out_schema=schemas.GoalOut,
    search_fields=["title"], filter_fields=["term"],
)

journal_router = make_crud_router(
    prefix="/api/journal", tag="Journal",
    model=models.JournalEntry, create_schema=schemas.JournalCreate,
    update_schema=schemas.JournalUpdate, out_schema=schemas.JournalOut,
    search_fields=["todays_learning", "ideas"], filter_fields=["mood"],
)

projects_router = make_crud_router(
    prefix="/api/projects", tag="Projects",
    model=models.Project, create_schema=schemas.ProjectCreate,
    update_schema=schemas.ProjectUpdate, out_schema=schemas.ProjectOut,
    search_fields=["title", "description"], filter_fields=["status"],
)

research_router = make_crud_router(
    prefix="/api/research", tag="Research",
    model=models.ResearchItem, create_schema=schemas.ResearchCreate,
    update_schema=schemas.ResearchUpdate, out_schema=schemas.ResearchOut,
    search_fields=["topic", "paper_title", "notes"], filter_fields=[],
)

startup_router = make_crud_router(
    prefix="/api/startup-ideas", tag="Startup Ideas",
    model=models.StartupIdea, create_schema=schemas.StartupCreate,
    update_schema=schemas.StartupUpdate, out_schema=schemas.StartupOut,
    search_fields=["title", "problem", "solution"], filter_fields=["status"],
)

reading_router = make_crud_router(
    prefix="/api/reading-list", tag="Reading List",
    model=models.ReadingItem, create_schema=schemas.ReadingCreate,
    update_schema=schemas.ReadingUpdate, out_schema=schemas.ReadingOut,
    search_fields=["title"], filter_fields=["type"],
)
