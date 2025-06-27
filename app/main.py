from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, posts, ai_responses
from database.database import engine
from database.models import Base
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI PostgreSQL OpenAI Project",
    description="FastAPIとPostgreSQL、OpenAI APIを統合したプロジェクト",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(ai_responses.router, prefix="/api/v1/ai", tags=["ai"])

@app.get("/")
async def root():
    return {"message": "FastAPI PostgreSQL OpenAI Project"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

