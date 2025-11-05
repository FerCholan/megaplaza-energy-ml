"""
Modelo de Alerta
"""
from sqlalchemy import Column, Integer, Float, DateTime, String, Text
from sqlalchemy.sql import func
from ..database import Base


class Alert(Base):
    """Modelo de alertas del sistema"""
    
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    tipo = Column(String, nullable=False)  # anomaly, high_consumption, prediction_error
    mensaje = Column(Text, nullable=False)
    area = Column(String, nullable=True)  # Área afectada
    threshold_exceeded = Column(Float, nullable=True)  # Umbral excedido
    severity = Column(String, default="medium")  # low, medium, high, critical
    status = Column(String, default="active")  # active, resolved, dismissed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Alert(id={self.id}, tipo={self.tipo}, severity={self.severity})>"
