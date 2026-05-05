from fastapi import FastAPI

from app.routers import auth, categories, stats, study_logs, users

app = FastAPI(
    title="SkillLog API",
    description="学習時間・学習内容・振り返りを記録する認証付きAPI",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(study_logs.router)
app.include_router(stats.router)