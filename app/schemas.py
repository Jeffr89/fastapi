from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base



from .models import User


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass




class UserCreate(BaseModel):
    email: EmailStr
    password: str

        
        
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
class TokenData(BaseModel):
    id : Optional [int] = None
    
    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id: int
    dir: bool