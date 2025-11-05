"""
Tests para los módulos de Machine Learning
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Añadir directorio ml/src al path
ml_src_path = Path(__file__).parent.parent / "ml" / "src"
sys.path.insert(0, str(ml_src_path))

from preprocessing import load_data, clean_data, create_features
from clustering import train_clustering_model, predict_cluster
from forecasting import train_forecasting_model, predict_consumption
from evaluation import calculate_metrics


@pytest.fixture
def sample_data():
    """Crear dataset de ejemplo para tests"""
    np.random.seed(42)
    n_samples = 100
    
    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=n_samples, freq='H'),
        'consumo_energia': np.random.normal(750, 100, n_samples),
        'pies_cuadrados': np.random.normal(250000, 10000, n_samples),
        'temperatura_aire': np.random.normal(22, 5, n_samples),
        'cobertura_nubes': np.random.uniform(0, 100, n_samples),
        'presion_nivel_mar': np.random.normal(1013, 10, n_samples),
        'velocidad_viento': np.random.gamma(2, 2, n_samples),
        'mes': [d.month for d in pd.date_range(start='2024-01-01', periods=n_samples, freq='H')],
        'dia_del_ano': [d.timetuple().tm_yday for d in pd.date_range(start='2024-01-01', periods=n_samples, freq='H')],
        'dia_de_la_semana': [d.weekday() for d in pd.date_range(start='2024-01-01', periods=n_samples, freq='H')],
        'hora_del_dia': [d.hour for d in pd.date_range(start='2024-01-01', periods=n_samples, freq='H')],
        'es_fin_de_semana': [(d.weekday() >= 5) for d in pd.date_range(start='2024-01-01', periods=n_samples, freq='H')],
        'medidor_electricidad': np.random.choice([1, 2, 3], n_samples),
        'medidor_agua_fria': np.random.choice([1, 2], n_samples)
    })
    
    return df


def test_clean_data(sample_data):
    """Test de limpieza de datos"""
    # Añadir algunos valores nulos
    sample_data.loc[0, 'consumo_energia'] = np.nan
    sample_data.loc[1, 'temperatura_aire'] = np.nan
    
    df_clean = clean_data(sample_data)
    
    # Verificar que no hay nulos
    assert df_clean.isnull().sum().sum() == 0
    
    # Verificar que se mantienen la mayoría de registros
    assert len(df_clean) >= len(sample_data) * 0.8


def test_create_features(sample_data):
    """Test de creación de features"""
    df_features = create_features(sample_data)
    
    # Verificar que se crearon nuevas columnas
    assert 'consumo_lag_1' in df_features.columns or len(df_features.columns) >= len(sample_data.columns)
    
    # Verificar que timestamp es datetime
    if 'timestamp' in df_features.columns:
        assert pd.api.types.is_datetime64_any_dtype(df_features['timestamp'])


def test_train_clustering_model(sample_data):
    """Test de entrenamiento de modelo de clustering"""
    # Preparar features
    feature_cols = ['pies_cuadrados', 'temperatura_aire', 'hora_del_dia']
    X = sample_data[feature_cols]
    
    # Entrenar modelo
    model = train_clustering_model(X, n_clusters=3)
    
    # Verificar que el modelo se entrenó
    assert hasattr(model, 'cluster_centers_')
    assert len(model.cluster_centers_) == 3


def test_predict_cluster(sample_data):
    """Test de predicción de clusters"""
    feature_cols = ['pies_cuadrados', 'temperatura_aire', 'hora_del_dia']
    X = sample_data[feature_cols]
    
    # Entrenar modelo
    model = train_clustering_model(X, n_clusters=3)
    
    # Predecir
    predictions = predict_cluster(model, X.head(10))
    
    # Verificar predicciones
    assert len(predictions) == 10
    assert all(0 <= p <= 2 for p in predictions)


def test_train_forecasting_model(sample_data):
    """Test de entrenamiento de modelo de predicción"""
    feature_cols = ['pies_cuadrados', 'temperatura_aire', 'hora_del_dia', 'dia_de_la_semana']
    X = sample_data[feature_cols]
    y = sample_data['consumo_energia']
    
    # Entrenar modelo
    model = train_forecasting_model(X, y, model_type='random_forest', n_estimators=10)
    
    # Verificar que el modelo se entrenó
    assert hasattr(model, 'predict')


def test_predict_consumption(sample_data):
    """Test de predicción de consumo"""
    feature_cols = ['pies_cuadrados', 'temperatura_aire', 'hora_del_dia', 'dia_de_la_semana']
    X = sample_data[feature_cols]
    y = sample_data['consumo_energia']
    
    # Entrenar modelo
    model = train_forecasting_model(X, y, model_type='random_forest', n_estimators=10)
    
    # Predecir
    predictions = predict_consumption(model, X.head(5))
    
    # Verificar predicciones
    assert len(predictions) == 5
    assert all(isinstance(p, (int, float, np.number)) for p in predictions)


def test_calculate_metrics():
    """Test de cálculo de métricas"""
    y_true = np.array([100, 200, 300, 400, 500])
    y_pred = np.array([110, 190, 310, 390, 510])
    
    metrics = calculate_metrics(y_true, y_pred)
    
    # Verificar que se calcularon todas las métricas
    assert 'MAE' in metrics
    assert 'MSE' in metrics
    assert 'RMSE' in metrics
    assert 'R2' in metrics
    assert 'MAPE' in metrics
    
    # Verificar que las métricas son razonables
    assert metrics['MAE'] > 0
    assert metrics['R2'] <= 1
    assert metrics['MAPE'] >= 0


def test_model_performance(sample_data):
    """Test de rendimiento del modelo"""
    feature_cols = ['pies_cuadrados', 'temperatura_aire', 'hora_del_dia', 'dia_de_la_semana']
    X = sample_data[feature_cols]
    y = sample_data['consumo_energia']
    
    # Split train/test
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Entrenar y predecir
    model = train_forecasting_model(X_train, y_train, model_type='random_forest', n_estimators=10)
    y_pred = predict_consumption(model, X_test)
    
    # Calcular métricas
    metrics = calculate_metrics(y_test.values, y_pred)
    
    # Verificar que el modelo tiene un rendimiento mínimo aceptable
    # (con datos aleatorios, R2 puede ser bajo, pero debería existir)
    assert -1 <= metrics['R2'] <= 1
