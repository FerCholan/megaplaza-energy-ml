"""
Funciones de predicción de consumo energético
"""
import joblib
import numpy as np
import pandas as pd
from typing import Optional, Dict, Any
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor


def train_forecasting_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_type: str = 'xgboost',
    **kwargs
) -> Any:
    """
    Entrena un modelo de predicción
    
    Args:
        X_train: Características de entrenamiento
        y_train: Variable objetivo de entrenamiento
        model_type: Tipo de modelo ('xgboost', 'random_forest', 'gradient_boosting')
        **kwargs: Parámetros adicionales para el modelo
        
    Returns:
        Modelo entrenado
    """
    if model_type == 'xgboost':
        model = XGBRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', 6),
            learning_rate=kwargs.get('learning_rate', 0.1),
            random_state=kwargs.get('random_state', 42)
        )
    elif model_type == 'random_forest':
        model = RandomForestRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', 10),
            random_state=kwargs.get('random_state', 42)
        )
    elif model_type == 'gradient_boosting':
        model = GradientBoostingRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', 5),
            learning_rate=kwargs.get('learning_rate', 0.1),
            random_state=kwargs.get('random_state', 42)
        )
    else:
        raise ValueError(f"Tipo de modelo no soportado: {model_type}")
    
    # Entrenar modelo
    model.fit(X_train, y_train)
    
    return model


def predict_consumption(
    model: Any,
    X: pd.DataFrame
) -> np.ndarray:
    """
    Predice el consumo energético
    
    Args:
        model: Modelo entrenado
        X: Características para predicción
        
    Returns:
        Array con las predicciones
    """
    return model.predict(X)


def get_feature_importance(
    model: Any,
    feature_names: list
) -> pd.DataFrame:
    """
    Obtiene la importancia de las características
    
    Args:
        model: Modelo entrenado
        feature_names: Lista de nombres de características
        
    Returns:
        DataFrame con la importancia de cada característica
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return importance_df
    else:
        return pd.DataFrame()


def save_model(model: Any, path: str) -> bool:
    """
    Guarda el modelo en disco
    
    Args:
        model: Modelo entrenado
        path: Ruta donde guardar el modelo
        
    Returns:
        True si se guardó correctamente
    """
    try:
        joblib.dump(model, path)
        return True
    except Exception as e:
        print(f"Error guardando modelo: {e}")
        return False


def load_model(path: str) -> Optional[Any]:
    """
    Carga un modelo desde disco
    
    Args:
        path: Ruta del modelo
        
    Returns:
        Modelo cargado o None si hay error
    """
    try:
        model = joblib.load(path)
        return model
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return None


def tune_hyperparameters(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_type: str = 'xgboost',
    cv: int = 5
) -> Dict[str, Any]:
    """
    Optimiza hiperparámetros usando GridSearchCV
    
    Args:
        X_train: Características de entrenamiento
        y_train: Variable objetivo
        model_type: Tipo de modelo
        cv: Número de folds para cross-validation
        
    Returns:
        Diccionario con los mejores parámetros
    """
    from sklearn.model_selection import GridSearchCV
    
    param_grids = {
        'xgboost': {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3]
        },
        'random_forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10]
        }
    }
    
    if model_type not in param_grids:
        return {}
    
    # Crear modelo base
    if model_type == 'xgboost':
        base_model = XGBRegressor(random_state=42)
    elif model_type == 'random_forest':
        base_model = RandomForestRegressor(random_state=42)
    else:
        return {}
    
    # Grid search
    grid_search = GridSearchCV(
        base_model,
        param_grids[model_type],
        cv=cv,
        scoring='neg_mean_squared_error',
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    return grid_search.best_params_
