"""
Rutas de predicciones
Realizar predicciones y obtener histórico
"""
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..models.prediction import Prediction
from ..services.ml_service import ml_service
from ..utils.dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/predictions", tags=["Predicciones"])


@router.post("/predict", response_model=dict)
async def predict_consumption(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Predice el consumo energético basado en las características proporcionadas
    """
    # Preparar features
    features = {
        "area": request.area,
        "temperatura": request.temperatura,
        "cobertura_nubes": request.cobertura_nubes or 0,
        "presion": request.presion or 1013,
        "velocidad_viento": request.velocidad_viento or 0,
        "mes": request.mes or datetime.now().month,
        "dia_semana": request.dia_semana or datetime.now().weekday(),
        "hora": request.hora or datetime.now().hour,
        "es_fin_de_semana": request.es_fin_de_semana or (1 if datetime.now().weekday() >= 5 else 0)
    }
    
    # Realizar predicción
    predicted_kwh = ml_service.predict_consumption(features)
    
    if predicted_kwh is None:
        raise HTTPException(
            status_code=500,
            detail="Error al realizar la predicción. Modelo no disponible."
        )
    
    # Guardar predicción
    timestamp = request.timestamp or datetime.utcnow()
    db_prediction = Prediction(
        timestamp=timestamp,
        predicted_kwh=predicted_kwh,
        model_version=ml_service.model_version
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return {
        "predicted_kwh": predicted_kwh,
        "timestamp": timestamp,
        "model_version": ml_service.model_version
    }


@router.get("/", response_model=List[PredictionResponse])
async def get_predictions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el histórico de predicciones
    """
    predictions = db.query(Prediction).order_by(
        desc(Prediction.timestamp)
    ).offset(skip).limit(limit).all()
    
    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene una predicción específica
    """
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    
    return prediction
