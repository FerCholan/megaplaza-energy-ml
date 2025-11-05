"""
Servicio de alertas
Detección de anomalías y envío de alertas
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.alert import Alert
from ..models.consumption import Consumption


class AlertService:
    """Servicio para gestión de alertas"""
    
    def __init__(self):
        self.thresholds = {
            "high_consumption": 1000,  # kWh
            "anomaly_factor": 2.0,  # Factor sobre la media
            "prediction_error": 0.3  # 30% de error
        }
    
    def check_high_consumption(
        self,
        db: Session,
        kwh: float,
        area: Optional[str] = None
    ) -> Optional[Alert]:
        """
        Verifica si el consumo excede el umbral
        
        Args:
            db: Sesión de base de datos
            kwh: Consumo en kWh
            area: Área afectada
            
        Returns:
            Alerta si se detecta consumo alto, None en caso contrario
        """
        if kwh > self.thresholds["high_consumption"]:
            alert = Alert(
                timestamp=datetime.utcnow(),
                tipo="high_consumption",
                mensaje=f"Consumo alto detectado: {kwh:.2f} kWh (umbral: {self.thresholds['high_consumption']} kWh)",
                area=area,
                threshold_exceeded=kwh - self.thresholds["high_consumption"],
                severity="high"
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            return alert
        return None
    
    def check_anomaly(
        self,
        db: Session,
        kwh: float,
        hours_back: int = 24
    ) -> Optional[Alert]:
        """
        Detecta anomalías en el consumo comparando con la media histórica
        
        Args:
            db: Sesión de base de datos
            kwh: Consumo actual
            hours_back: Horas hacia atrás para calcular la media
            
        Returns:
            Alerta si se detecta anomalía, None en caso contrario
        """
        # Calcular media de las últimas horas
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        avg_consumption = db.query(func.avg(Consumption.kwh)).filter(
            Consumption.timestamp >= cutoff_time
        ).scalar()
        
        if avg_consumption and kwh > avg_consumption * self.thresholds["anomaly_factor"]:
            alert = Alert(
                timestamp=datetime.utcnow(),
                tipo="anomaly",
                mensaje=f"Anomalía detectada: consumo {kwh:.2f} kWh es {kwh/avg_consumption:.1f}x mayor que la media ({avg_consumption:.2f} kWh)",
                threshold_exceeded=kwh - avg_consumption,
                severity="critical"
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            return alert
        return None
    
    def get_active_alerts(
        self,
        db: Session,
        limit: int = 10
    ) -> List[Alert]:
        """
        Obtiene las alertas activas más recientes
        
        Args:
            db: Sesión de base de datos
            limit: Número máximo de alertas
            
        Returns:
            Lista de alertas activas
        """
        return db.query(Alert).filter(
            Alert.status == "active"
        ).order_by(Alert.timestamp.desc()).limit(limit).all()
    
    def get_alert_stats(self, db: Session) -> dict:
        """
        Obtiene estadísticas de alertas
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            Diccionario con estadísticas
        """
        total = db.query(Alert).count()
        active = db.query(Alert).filter(Alert.status == "active").count()
        resolved = db.query(Alert).filter(Alert.status == "resolved").count()
        
        return {
            "total": total,
            "active": active,
            "resolved": resolved
        }
    
    def update_threshold(self, tipo: str, value: float) -> bool:
        """
        Actualiza un umbral de alerta
        
        Args:
            tipo: Tipo de umbral
            value: Nuevo valor
            
        Returns:
            True si se actualizó correctamente
        """
        if tipo in self.thresholds:
            self.thresholds[tipo] = value
            return True
        return False


# Instancia global del servicio
alert_service = AlertService()
