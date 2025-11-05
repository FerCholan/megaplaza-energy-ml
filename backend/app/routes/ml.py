"""
Rutas de Machine Learning
Clustering, información de modelos y re-entrenamiento
"""
from fastapi import APIRouter, Depends, HTTPException
from ..services.ml_service import ml_service
from ..utils.dependencies import get_current_user, get_current_admin_user
from ..models.user import User

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


@router.get("/models/info")
async def get_models_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene información sobre los modelos cargados
    """
    return ml_service.get_model_info()


@router.post("/models/load")
async def load_models(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Carga los modelos de ML (solo administradores)
    """
    forecasting_loaded = ml_service.load_forecasting_model()
    clustering_loaded = ml_service.load_clustering_model()
    
    return {
        "message": "Modelos cargados",
        "forecasting": forecasting_loaded,
        "clustering": clustering_loaded
    }


@router.get("/clusters")
async def get_cluster_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene información sobre los clusters
    """
    if not ml_service.clustering_model:
        ml_service.load_clustering_model()
    
    if not ml_service.clustering_model:
        raise HTTPException(
            status_code=404,
            detail="Modelo de clustering no disponible"
        )
    
    # Obtener número de clusters
    n_clusters = ml_service.clustering_model.n_clusters if hasattr(
        ml_service.clustering_model, 'n_clusters'
    ) else 3
    
    return {
        "n_clusters": n_clusters,
        "model_type": type(ml_service.clustering_model).__name__
    }


@router.post("/cluster/predict")
async def predict_cluster(
    area: float,
    temperatura: float,
    hora: int,
    dia_semana: int,
    current_user: User = Depends(get_current_user)
):
    """
    Predice el cluster para las características dadas
    """
    features = {
        "area": area,
        "temperatura": temperatura,
        "hora": hora,
        "dia_semana": dia_semana
    }
    
    cluster = ml_service.predict_cluster(features)
    
    if cluster is None:
        raise HTTPException(
            status_code=500,
            detail="Error al predecir cluster. Modelo no disponible."
        )
    
    return {
        "cluster": cluster,
        "features": features
    }


@router.post("/retrain")
async def retrain_models(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Solicita re-entrenamiento de modelos (solo administradores)
    """
    # En producción, esto dispararía un job asíncrono
    return {
        "message": "Re-entrenamiento solicitado",
        "status": "pending",
        "note": "El re-entrenamiento se procesará en segundo plano"
    }
