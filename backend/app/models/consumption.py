"""
Modelo de Consumo Energético
"""
from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.sql import func
from ..database import Base


class Consumption(Base):
    """Modelo de consumo energético"""
    
    __tablename__ = "consumptions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    kwh = Column(Float, nullable=False)  # Consumo en kWh
    area = Column(Float)  # Área en pies cuadrados
    temperatura = Column(Float)  # Temperatura del aire
    cobertura_nubes = Column(Float)  # Cobertura de nubes
    presion = Column(Float)  # Presión a nivel del mar
    velocidad_viento = Column(Float)  # Velocidad del viento
    mes = Column(Integer)
    dia_semana = Column(Integer)
    hora = Column(Integer)
    es_fin_de_semana = Column(Integer)
    medidor_electricidad = Column(Integer)
    medidor_agua_fria = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Consumption(id={self.id}, timestamp={self.timestamp}, kwh={self.kwh})>"
