"""
Cliente HTTP para comunicación con la API backend
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime
import os


class APIClient:
    """Cliente para interactuar con la API de backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.api_url = f"{self.base_url}/api/v1"
        self.token = None
    
    def set_token(self, token: str):
        """Establece el token de autenticación"""
        self.token = token
    
    def _get_headers(self) -> Dict:
        """Obtiene headers para las peticiones"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    # Autenticación
    def login(self, email: str, password: str) -> Optional[str]:
        """
        Inicia sesión y obtiene el token
        
        Returns:
            Token de acceso o None si falla
        """
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                data={"username": email, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                return self.token
            return None
        except Exception as e:
            print(f"Error en login: {e}")
            return None
    
    def register(self, email: str, password: str) -> bool:
        """Registra un nuevo usuario"""
        try:
            response = requests.post(
                f"{self.api_url}/auth/register",
                json={"email": email, "password": password}
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error en registro: {e}")
            return False
    
    # Consumo
    def get_consumption_data(
        self,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """Obtiene datos de consumo histórico"""
        try:
            params = {"skip": skip, "limit": limit}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            
            response = requests.get(
                f"{self.api_url}/consumption/",
                params=params,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo consumo: {e}")
            return []
    
    def get_realtime_consumption(self, hours: int = 24) -> List[Dict]:
        """Obtiene consumo en tiempo real"""
        try:
            response = requests.get(
                f"{self.api_url}/consumption/realtime",
                params={"hours": hours},
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo consumo tiempo real: {e}")
            return []
    
    def get_consumption_stats(self, days: int = 7) -> Dict:
        """Obtiene estadísticas de consumo"""
        try:
            response = requests.get(
                f"{self.api_url}/consumption/stats",
                params={"days": days},
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error obteniendo stats: {e}")
            return {}
    
    # Predicciones
    def predict_consumption(self, features: Dict) -> Optional[Dict]:
        """Solicita una predicción de consumo"""
        try:
            response = requests.post(
                f"{self.api_url}/predictions/predict",
                json=features,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error en predicción: {e}")
            return None
    
    def get_predictions(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Obtiene histórico de predicciones"""
        try:
            response = requests.get(
                f"{self.api_url}/predictions/",
                params={"skip": skip, "limit": limit},
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo predicciones: {e}")
            return []
    
    # Alertas
    def get_alerts(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Obtiene alertas del sistema"""
        try:
            params = {"skip": skip, "limit": limit}
            if status:
                params["status"] = status
            
            response = requests.get(
                f"{self.api_url}/alerts/",
                params=params,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo alertas: {e}")
            return []
    
    def get_active_alerts(self, limit: int = 10) -> List[Dict]:
        """Obtiene alertas activas"""
        try:
            response = requests.get(
                f"{self.api_url}/alerts/active",
                params={"limit": limit},
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo alertas activas: {e}")
            return []
    
    def get_alert_stats(self) -> Dict:
        """Obtiene estadísticas de alertas"""
        try:
            response = requests.get(
                f"{self.api_url}/alerts/stats",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error obteniendo stats de alertas: {e}")
            return {}
    
    # ML
    def get_models_info(self) -> Dict:
        """Obtiene información de los modelos"""
        try:
            response = requests.get(
                f"{self.api_url}/ml/models/info",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error obteniendo info de modelos: {e}")
            return {}
    
    def get_cluster_info(self) -> Dict:
        """Obtiene información de clusters"""
        try:
            response = requests.get(
                f"{self.api_url}/ml/clusters",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Error obteniendo info de clusters: {e}")
            return {}
