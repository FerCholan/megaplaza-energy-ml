"""
Rutas de consumo energético
Obtener histórico y datos en tiempo real
"""
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..schemas.consumption import ConsumptionCreate, ConsumptionResponse
from ..models.consumption import Consumption
from ..utils.dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/consumption", tags=["Consumo"])


@router.get("/", response_model=List[ConsumptionResponse])
async def get_consumption_history(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el histórico de consumo energético
    """
    query = db.query(Consumption)
    
    # Filtrar por fechas si se proporcionan
    if start_date:
        query = query.filter(Consumption.timestamp >= start_date)
    if end_date:
        query = query.filter(Consumption.timestamp <= end_date)
    
    # Ordenar por timestamp descendente
    query = query.order_by(desc(Consumption.timestamp))
    
    # Paginación
    consumptions = query.offset(skip).limit(limit).all()
    return consumptions


@router.get("/realtime", response_model=List[ConsumptionResponse])
async def get_realtime_consumption(
    hours: int = Query(24, description="Horas hacia atrás"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el consumo en tiempo real (últimas horas)
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    consumptions = db.query(Consumption).filter(
        Consumption.timestamp >= cutoff_time
    ).order_by(desc(Consumption.timestamp)).all()
    
    return consumptions


@router.post("/", response_model=ConsumptionResponse, status_code=201)
async def create_consumption(
    consumption: ConsumptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Registra un nuevo dato de consumo
    """
    db_consumption = Consumption(**consumption.dict())
    db.add(db_consumption)
    db.commit()
    db.refresh(db_consumption)
    return db_consumption


@router.get("/stats")
async def get_consumption_stats(
    days: int = Query(7, description="Días hacia atrás"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene estadísticas de consumo
    """
    from sqlalchemy import func
    
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
    
    stats = db.query(
        func.avg(Consumption.kwh).label("avg"),
        func.min(Consumption.kwh).label("min"),
        func.max(Consumption.kwh).label("max"),
        func.sum(Consumption.kwh).label("total")
    ).filter(
        Consumption.timestamp >= cutoff_time
    ).first()
    
    return {
        "period_days": days,
        "average_kwh": float(stats.avg) if stats.avg else 0,
        "min_kwh": float(stats.min) if stats.min else 0,
        "max_kwh": float(stats.max) if stats.max else 0,
        "total_kwh": float(stats.total) if stats.total else 0
    }
