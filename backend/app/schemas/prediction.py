"""
Esquemas Pydantic para Predicciones
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """Esquema para solicitar predicciones"""
    timestamp: Optional[datetime] = None
    area: float
    temperatura: float
    cobertura_nubes: Optional[float] = None
    presion: Optional[float] = None
    velocidad_viento: Optional[float] = None
    mes: Optional[int] = None
    dia_semana: Optional[int] = None
    hora: Optional[int] = None
    es_fin_de_semana: Optional[int] = None


class PredictionResponse(BaseModel):
    """Esquema de respuesta de predicción"""
    id: int
    timestamp: datetime
    predicted_kwh: float
    real_kwh: Optional[float] = None
    model_version: str
    error: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BatchPredictionRequest(BaseModel):
    """Esquema para predicciones en lote"""
    predictions: List[PredictionRequest]
