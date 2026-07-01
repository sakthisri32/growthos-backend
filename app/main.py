from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.config import settings
from app.routers import (
    auth_router,
    users_router,
    habits_router,
    achievements_router,
    analytics_router,
    crud_modules,
)

# Create tables. In production, prefer Alembic migrations over create_all.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GrowthOS API",
    description="Backend for GrowthOS — the all-in-one AI productivity platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(habits_router.router)
app.include_router(achievements_router.router)
app.include_router(analytics_router.router)
app.include_router(crud_modules.tasks_router)
app.include_router(crud_modules.timetable_router)
app.include_router(crud_modules.skills_router)
app.include_router(crud_modules.goals_router)
app.include_router(crud_modules.journal_router)
app.include_router(crud_modules.projects_router)
app.include_router(crud_modules.research_router)
app.include_router(crud_modules.startup_router)
app.include_router(crud_modules.reading_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "GrowthOS API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
