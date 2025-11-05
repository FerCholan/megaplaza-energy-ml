"""
Esquemas Pydantic para Alertas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AlertBase(BaseModel):
    """Esquema base de alerta"""
    timestamp: datetime
    tipo: str
    mensaje: str
    area: Optional[str] = None
    threshold_exceeded: Optional[float] = None
    severity: str = "medium"
    status: str = "active"


class AlertResponse(AlertBase):
    """Esquema de respuesta de alerta"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertConfig(BaseModel):
    """Esquema para configuración de alertas"""
    tipo: str
    threshold: float
    enabled: bool = True
    notification_email: Optional[str] = None


class AlertStats(BaseModel):
    """Estadísticas de alertas"""
    total: int
    active: int
    resolved: int
    by_severity: dict
    by_type: dict
