from re import S
from turtle import st
from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional


# (Request) Article Schema
class ArticleBase(BaseModel):
    article_url: str
    article_title: str


# (Request) User Sign up Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    id_saved_post: Optional[List[int]]

# (Request) Vote Schema
class VoteBase(BaseModel):
    user_id: int
    post_id: int
    like: conint(ge = -1, le = 1)


# (Response) Token Schema
class TokenOut(BaseModel):
    access_token: str
    token_type: str


# (Response) Article Schema
class ArticleOut(ArticleBase):
    id: int
    user_id: int
    saved_count: int
    class Config:
        orm_mode = True


# (Response) User Schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    id_saved_post: Optional[List[int]]

    class Config:
        orm_mode = True




















