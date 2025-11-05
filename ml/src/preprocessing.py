"""
Funciones de preprocesamiento de datos
"""
import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.preprocessing import StandardScaler


def load_data(path: str) -> pd.DataFrame:
    """
    Carga el dataset desde un archivo CSV
    
    Args:
        path: Ruta al archivo CSV
        
    Returns:
        DataFrame con los datos
    """
    df = pd.read_csv(path)
    
    # Convertir timestamp a datetime si existe
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset eliminando nulos y outliers
    
    Args:
        df: DataFrame a limpiar
        
    Returns:
        DataFrame limpio
    """
    # Crear copia para no modificar el original
    df_clean = df.copy()
    
    # Eliminar duplicados
    df_clean = df_clean.drop_duplicates()
    
    # Rellenar valores nulos con la mediana
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    # Eliminar outliers usando IQR (solo para consumo_energia)
    if 'consumo_energia' in df_clean.columns:
        Q1 = df_clean['consumo_energia'].quantile(0.25)
        Q3 = df_clean['consumo_energia'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        df_clean = df_clean[
            (df_clean['consumo_energia'] >= lower_bound) &
            (df_clean['consumo_energia'] <= upper_bound)
        ]
    
    return df_clean


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea nuevas características (feature engineering)
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        DataFrame con nuevas características
    """
    df_features = df.copy()
    
    # Si tenemos timestamp, crear features temporales
    if 'timestamp' in df_features.columns and pd.api.types.is_datetime64_any_dtype(df_features['timestamp']):
        df_features['hora'] = df_features['timestamp'].dt.hour
        df_features['dia_semana'] = df_features['timestamp'].dt.dayofweek
        df_features['mes'] = df_features['timestamp'].dt.month
        df_features['dia_mes'] = df_features['timestamp'].dt.day
        df_features['es_fin_de_semana'] = (df_features['dia_semana'] >= 5).astype(int)
    
    # Crear lags para consumo_energia (si existe)
    if 'consumo_energia' in df_features.columns:
        df_features['consumo_lag_1'] = df_features['consumo_energia'].shift(1)
        df_features['consumo_lag_24'] = df_features['consumo_energia'].shift(24)
        
        # Rolling means
        df_features['consumo_rolling_mean_24'] = df_features['consumo_energia'].rolling(
            window=24, min_periods=1
        ).mean()
        df_features['consumo_rolling_std_24'] = df_features['consumo_energia'].rolling(
            window=24, min_periods=1
        ).std()
    
    # Interacción temperatura-hora
    if 'temperatura_aire' in df_features.columns and 'hora' in df_features.columns:
        df_features['temp_hora_interaction'] = df_features['temperatura_aire'] * df_features['hora']
    
    return df_features


def scale_features(
    df: pd.DataFrame,
    features: List[str],
    scaler: StandardScaler = None
) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Normaliza las características especificadas
    
    Args:
        df: DataFrame con los datos
        features: Lista de columnas a escalar
        scaler: Scaler pre-entrenado (opcional)
        
    Returns:
        Tupla con (DataFrame escalado, scaler usado)
    """
    df_scaled = df.copy()
    
    # Crear scaler si no se proporciona
    if scaler is None:
        scaler = StandardScaler()
        df_scaled[features] = scaler.fit_transform(df[features])
    else:
        df_scaled[features] = scaler.transform(df[features])
    
    return df_scaled, scaler


def prepare_train_test_split(
    df: pd.DataFrame,
    target_col: str,
    feature_cols: List[str],
    test_size: float = 0.2
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Prepara los datos para entrenamiento con split temporal
    
    Args:
        df: DataFrame con los datos
        target_col: Nombre de la columna objetivo
        feature_cols: Lista de columnas de características
        test_size: Proporción del conjunto de prueba
        
    Returns:
        Tupla con (X_train, X_test, y_train, y_test)
    """
    # Ordenar por timestamp si existe
    if 'timestamp' in df.columns:
        df = df.sort_values('timestamp')
    
    # Calcular índice de corte
    split_idx = int(len(df) * (1 - test_size))
    
    # Dividir datos
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    # Separar features y target
    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]
    y_train = train_df[target_col]
    y_test = test_df[target_col]
    
    return X_train, X_test, y_train, y_test
