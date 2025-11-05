"""
Rutas de alertas
Gestión y configuración de alertas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.alert import AlertResponse, AlertConfig, AlertStats
from ..models.alert import Alert
from ..services.alert_service import alert_service
from ..utils.dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/alerts", tags=["Alertas"])


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 50,
    status: str = None,
    severity: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene las alertas del sistema
    """
    query = db.query(Alert)
    
    # Filtrar por status si se proporciona
    if status:
        query = query.filter(Alert.status == status)
    
    # Filtrar por severity si se proporciona
    if severity:
        query = query.filter(Alert.severity == severity)
    
    # Ordenar por timestamp descendente
    alerts = query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
    
    return alerts


@router.get("/active", response_model=List[AlertResponse])
async def get_active_alerts(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene las alertas activas más recientes
    """
    return alert_service.get_active_alerts(db, limit=limit)


@router.get("/stats", response_model=AlertStats)
async def get_alert_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene estadísticas de alertas
    """
    stats = alert_service.get_alert_stats(db)
    
    # Agregar estadísticas por severidad y tipo
    from sqlalchemy import func
    
    by_severity = db.query(
        Alert.severity,
        func.count(Alert.id).label("count")
    ).group_by(Alert.severity).all()
    
    by_type = db.query(
        Alert.tipo,
        func.count(Alert.id).label("count")
    ).group_by(Alert.tipo).all()
    
    stats["by_severity"] = {item.severity: item.count for item in by_severity}
    stats["by_type"] = {item.tipo: item.count for item in by_type}
    
    return stats


@router.post("/config")
async def configure_alert(
    config: AlertConfig,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Configura los umbrales de alertas
    """
    # Actualizar umbral
    success = alert_service.update_threshold(config.tipo, config.threshold)
    
    if not success:
        raise HTTPException(status_code=400, detail="Tipo de alerta inválido")
    
    return {
        "message": "Configuración actualizada",
        "tipo": config.tipo,
        "threshold": config.threshold,
        "enabled": config.enabled
    }


@router.put("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marca una alerta como resuelta
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    
    alert.status = "resolved"
    db.commit()
    db.refresh(alert)
    
    return {"message": "Alerta resuelta", "alert": alert}
