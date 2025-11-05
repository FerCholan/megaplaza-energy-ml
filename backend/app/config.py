"""
Configuración de la aplicación
Gestiona variables de entorno y configuración general
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación usando variables de entorno"""
    
    # Base de datos
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/megaplaza_energy"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "megaplaza_energy"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Megaplaza Energy ML"
    DEBUG: bool = True
    
    # ML Models
    MODEL_PATH: str = "ml/models/"
    CLUSTERING_MODEL: str = "clustering_model.pkl"
    FORECASTING_MODEL: str = "forecasting_model.pkl"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    ALERT_EMAIL: str = "admin@megaplaza.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
