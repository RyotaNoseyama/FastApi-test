from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from database.models import Post as PostModel, User as UserModel
from app.schemas import Post, PostCreate, PostUpdate, PostWithAuthor

router = APIRouter()

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, author_id: int, db: Session = Depends(get_db)):
    """新しい投稿を作成"""
    # 作成者が存在するかチェック
    db_user = db.query(UserModel).filter(UserModel.id == author_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_post = PostModel(**post.dict(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostWithAuthor])
async def read_posts(skip: int = 0, limit: int = 100, published_only: bool = False, db: Session = Depends(get_db)):
    """投稿一覧を取得"""
    query = db.query(PostModel)
    if published_only:
        query = query.filter(PostModel.is_published == True)
    
    posts = query.offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostWithAuthor)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    """特定の投稿を取得"""
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    """投稿を更新"""
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """投稿を削除"""
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return None

@router.get("/user/{user_id}", response_model=List[Post])
async def read_user_posts(user_id: int, db: Session = Depends(get_db)):
    """特定ユーザーの投稿一覧を取得"""
    posts = db.query(PostModel).filter(PostModel.author_id == user_id).all()
    return posts

