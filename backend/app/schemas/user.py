"""
Esquemas Pydantic para Usuario
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Esquema base de usuario"""
    email: EmailStr


class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    """Esquema para login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Esquema de respuesta de usuario"""
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Esquema de token JWT"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Datos del token"""
    email: Optional[str] = None
