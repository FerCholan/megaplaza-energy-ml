"""
Servicio de autenticación
Manejo de registro, login y gestión de usuarios
"""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from ..utils.security import verify_password, get_password_hash, create_access_token


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Busca un usuario por email
    
    Args:
        db: Sesión de base de datos
        email: Email del usuario
        
    Returns:
        Usuario o None si no existe
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Crea un nuevo usuario
    
    Args:
        db: Sesión de base de datos
        user: Datos del usuario
        
    Returns:
        Usuario creado
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Autentica un usuario
    
    Args:
        db: Sesión de base de datos
        email: Email del usuario
        password: Contraseña
        
    Returns:
        Usuario autenticado o None si las credenciales son inválidas
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_token(user: User) -> str:
    """
    Crea un token JWT para un usuario
    
    Args:
        user: Usuario
        
    Returns:
        Token JWT
    """
    access_token = create_access_token(data={"sub": user.email})
    return access_token
