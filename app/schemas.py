from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =========================
# User Schemas
# =========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


# =========================
# Authentication Schemas
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# =========================
# Diary Schemas
# =========================

class DiaryCreate(BaseModel):
    title: str
    content: str
    mood: Optional[str] = None
    category: Optional[str] = None
    is_favorite: bool = False
    is_archived: bool = False


class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None
    category: Optional[str] = None
    is_favorite: bool = False
    is_archived: bool = False


class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    mood: Optional[str]
    category: Optional[str]
    is_favorite: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# Reflection Schema
# =========================

class ReflectionResponse(BaseModel):
    latest_title: str
    latest_mood: Optional[str]
    reflection: str