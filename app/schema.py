from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr
from typing import Optional
from pydantic.types import conint



class PostBase(BaseModel):
    title: str
    contents: str
    published: bool = False

class User(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id: int
    title: str
    contents: str
    published: bool
    created_at: datetime 
    owner: UserResponse
    #owner_id: int
    class Config:
        orm_mode = True

        
class PostOut(BaseModel):
    post: Post
    vote: int



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dire: conint(le=1)