"""
Esquemas Pydantic para validación de datos
"""
from .user import UserCreate, UserResponse, UserLogin
from .consumption import ConsumptionCreate, ConsumptionResponse
from .prediction import PredictionResponse, PredictionRequest
from .alert import AlertResponse, AlertConfig

__all__ = [
    "UserCreate", "UserResponse", "UserLogin",
    "ConsumptionCreate", "ConsumptionResponse",
    "PredictionResponse", "PredictionRequest",
    "AlertResponse", "AlertConfig"
]
