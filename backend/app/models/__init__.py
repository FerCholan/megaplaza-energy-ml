"""
Modelos de base de datos SQLAlchemy
"""
from .user import User
from .consumption import Consumption
from .prediction import Prediction
from .alert import Alert

__all__ = ["User", "Consumption", "Prediction", "Alert"]
