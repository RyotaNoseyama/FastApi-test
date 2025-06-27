from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from database.models import AIResponse as AIResponseModel, User as UserModel
from app.schemas import AIResponse, AIResponseCreate
from services.openai_service import OpenAIService

router = APIRouter()

@router.post("/generate", response_model=AIResponse, status_code=status.HTTP_201_CREATED)
async def generate_ai_response(
    request: AIResponseCreate, 
    user_id: int, 
    model: str = "gpt-3.5-turbo",
    db: Session = Depends(get_db)
):
    """OpenAI APIを使用してAI応答を生成し、データベースに保存"""
    # ユーザーが存在するかチェック
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # OpenAI APIを呼び出し
        openai_service = OpenAIService()
        ai_response, tokens_used = await openai_service.generate_response(
            prompt=request.prompt,
            model=model
        )
        
        # データベースに保存
        db_ai_response = AIResponseModel(
            user_id=user_id,
            prompt=request.prompt,
            response=ai_response,
            model=model,
            tokens_used=tokens_used
        )
        db.add(db_ai_response)
        db.commit()
        db.refresh(db_ai_response)
        
        return db_ai_response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI response: {str(e)}"
        )

@router.get("/", response_model=List[AIResponse])
async def read_ai_responses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """AI応答一覧を取得"""
    responses = db.query(AIResponseModel).offset(skip).limit(limit).all()
    return responses

@router.get("/{response_id}", response_model=AIResponse)
async def read_ai_response(response_id: int, db: Session = Depends(get_db)):
    """特定のAI応答を取得"""
    db_response = db.query(AIResponseModel).filter(AIResponseModel.id == response_id).first()
    if db_response is None:
        raise HTTPException(status_code=404, detail="AI response not found")
    return db_response

@router.get("/user/{user_id}", response_model=List[AIResponse])
async def read_user_ai_responses(user_id: int, db: Session = Depends(get_db)):
    """特定ユーザーのAI応答一覧を取得"""
    responses = db.query(AIResponseModel).filter(AIResponseModel.user_id == user_id).all()
    return responses

@router.delete("/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_response(response_id: int, db: Session = Depends(get_db)):
    """AI応答を削除"""
    db_response = db.query(AIResponseModel).filter(AIResponseModel.id == response_id).first()
    if db_response is None:
        raise HTTPException(status_code=404, detail="AI response not found")
    
    db.delete(db_response)
    db.commit()
    return None

