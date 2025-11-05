"""
Servicio de Machine Learning
Carga de modelos, predicciones y clustering
"""
import os
import joblib
import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..config import settings


class MLService:
    """Servicio para operaciones de Machine Learning"""
    
    def __init__(self):
        self.forecasting_model = None
        self.clustering_model = None
        self.model_version = "v1.0"
        
    def load_forecasting_model(self) -> bool:
        """
        Carga el modelo de predicción
        
        Returns:
            True si se cargó correctamente, False en caso contrario
        """
        try:
            model_path = os.path.join(
                settings.MODEL_PATH,
                settings.FORECASTING_MODEL
            )
            if os.path.exists(model_path):
                self.forecasting_model = joblib.load(model_path)
                return True
            return False
        except Exception as e:
            print(f"Error cargando modelo de predicción: {e}")
            return False
    
    def load_clustering_model(self) -> bool:
        """
        Carga el modelo de clustering
        
        Returns:
            True si se cargó correctamente, False en caso contrario
        """
        try:
            model_path = os.path.join(
                settings.MODEL_PATH,
                settings.CLUSTERING_MODEL
            )
            if os.path.exists(model_path):
                self.clustering_model = joblib.load(model_path)
                return True
            return False
        except Exception as e:
            print(f"Error cargando modelo de clustering: {e}")
            return False
    
    def predict_consumption(self, features: Dict[str, Any]) -> Optional[float]:
        """
        Predice el consumo energético
        
        Args:
            features: Diccionario con las características
            
        Returns:
            Consumo predicho en kWh o None si hay error
        """
        try:
            # Cargar modelo si no está cargado
            if self.forecasting_model is None:
                if not self.load_forecasting_model():
                    return None
            
            # Preparar features
            feature_names = [
                'area', 'temperatura', 'cobertura_nubes', 'presion',
                'velocidad_viento', 'mes', 'dia_semana', 'hora',
                'es_fin_de_semana'
            ]
            
            X = np.array([[features.get(f, 0) for f in feature_names]])
            
            # Predecir
            prediction = self.forecasting_model.predict(X)[0]
            return float(prediction)
            
        except Exception as e:
            print(f"Error en predicción: {e}")
            return None
    
    def predict_cluster(self, features: Dict[str, Any]) -> Optional[int]:
        """
        Predice el cluster de consumo
        
        Args:
            features: Diccionario con las características
            
        Returns:
            Número de cluster o None si hay error
        """
        try:
            # Cargar modelo si no está cargado
            if self.clustering_model is None:
                if not self.load_clustering_model():
                    return None
            
            # Preparar features
            feature_names = ['area', 'temperatura', 'hora', 'dia_semana']
            X = np.array([[features.get(f, 0) for f in feature_names]])
            
            # Predecir cluster
            cluster = self.clustering_model.predict(X)[0]
            return int(cluster)
            
        except Exception as e:
            print(f"Error en clustering: {e}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre los modelos
        
        Returns:
            Diccionario con información de los modelos
        """
        return {
            "forecasting_loaded": self.forecasting_model is not None,
            "clustering_loaded": self.clustering_model is not None,
            "version": self.model_version
        }


# Instancia global del servicio
ml_service = MLService()
