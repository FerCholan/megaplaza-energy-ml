"""
Esquemas Pydantic para Consumo Energético
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ConsumptionBase(BaseModel):
    """Esquema base de consumo"""
    timestamp: datetime
    kwh: float
    area: Optional[float] = None
    temperatura: Optional[float] = None
    cobertura_nubes: Optional[float] = None
    presion: Optional[float] = None
    velocidad_viento: Optional[float] = None
    mes: Optional[int] = None
    dia_semana: Optional[int] = None
    hora: Optional[int] = None
    es_fin_de_semana: Optional[int] = None
    medidor_electricidad: Optional[int] = None
    medidor_agua_fria: Optional[int] = None


class ConsumptionCreate(ConsumptionBase):
    """Esquema para crear consumo"""
    pass


class ConsumptionResponse(ConsumptionBase):
    """Esquema de respuesta de consumo"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
