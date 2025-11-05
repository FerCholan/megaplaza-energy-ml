"""
Modelo de Predicción
"""
from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.sql import func
from ..database import Base


class Prediction(Base):
    """Modelo de predicciones de consumo energético"""
    
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    predicted_kwh = Column(Float, nullable=False)  # Consumo predicho
    real_kwh = Column(Float, nullable=True)  # Consumo real (si está disponible)
    model_version = Column(String, default="v1.0")  # Versión del modelo usado
    error = Column(Float, nullable=True)  # Error de predicción
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, timestamp={self.timestamp}, predicted_kwh={self.predicted_kwh})>"
