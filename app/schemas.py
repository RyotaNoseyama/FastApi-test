from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Post schemas
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

class Post(PostBase):
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# AI Response schemas
class AIResponseBase(BaseModel):
    prompt: str

class AIResponseCreate(AIResponseBase):
    pass

class AIResponse(AIResponseBase):
    id: int
    user_id: int
    response: str
    model: str
    tokens_used: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response models
class UserWithPosts(User):
    posts: List[Post] = []

class PostWithAuthor(Post):
    author: User

