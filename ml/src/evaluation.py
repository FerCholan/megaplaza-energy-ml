"""
Funciones de evaluación de modelos
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Tuple
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calcula métricas de evaluación
    
    Args:
        y_true: Valores reales
        y_pred: Valores predichos
        
    Returns:
        Diccionario con las métricas
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'MAPE': mape
    }


def plot_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Predicciones vs Valores Reales",
    n_samples: int = None
) -> plt.Figure:
    """
    Grafica las predicciones comparadas con los valores reales
    
    Args:
        y_true: Valores reales
        y_pred: Valores predichos
        title: Título del gráfico
        n_samples: Número de muestras a mostrar (None para todas)
        
    Returns:
        Figura de matplotlib
    """
    # Limitar número de muestras si se especifica
    if n_samples:
        y_true = y_true[:n_samples]
        y_pred = y_pred[:n_samples]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Gráfico de línea temporal
    ax1.plot(y_true, label='Real', alpha=0.7)
    ax1.plot(y_pred, label='Predicho', alpha=0.7)
    ax1.set_xlabel('Muestra')
    ax1.set_ylabel('Consumo (kWh)')
    ax1.set_title(title)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfico de dispersión
    ax2.scatter(y_true, y_pred, alpha=0.5)
    
    # Línea de referencia perfecta
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    ax2.plot([min_val, max_val], [min_val, max_val], 'r--', label='Predicción perfecta')
    
    ax2.set_xlabel('Consumo Real (kWh)')
    ax2.set_ylabel('Consumo Predicho (kWh)')
    ax2.set_title('Scatter Plot: Real vs Predicho')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> plt.Figure:
    """
    Grafica los residuos de las predicciones
    
    Args:
        y_true: Valores reales
        y_pred: Valores predichos
        
    Returns:
        Figura de matplotlib
    """
    residuals = y_true - y_pred
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histograma de residuos
    ax1.hist(residuals, bins=50, edgecolor='black', alpha=0.7)
    ax1.axvline(x=0, color='r', linestyle='--', label='Error = 0')
    ax1.set_xlabel('Residuo (kWh)')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Distribución de Residuos')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Residuos vs predicciones
    ax2.scatter(y_pred, residuals, alpha=0.5)
    ax2.axhline(y=0, color='r', linestyle='--')
    ax2.set_xlabel('Consumo Predicho (kWh)')
    ax2.set_ylabel('Residuo (kWh)')
    ax2.set_title('Residuos vs Predicciones')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def generate_report(
    metrics: Dict[str, float],
    model_name: str = "Modelo"
) -> str:
    """
    Genera un reporte en texto de las métricas
    
    Args:
        metrics: Diccionario con las métricas
        model_name: Nombre del modelo
        
    Returns:
        Reporte en formato de texto
    """
    report = f"""
    ========================================
    REPORTE DE EVALUACIÓN - {model_name}
    ========================================
    
    Métricas de Error:
    ------------------
    MAE (Error Absoluto Medio):       {metrics['MAE']:.2f} kWh
    MSE (Error Cuadrático Medio):     {metrics['MSE']:.2f} kWh²
    RMSE (Raíz del ECM):              {metrics['RMSE']:.2f} kWh
    MAPE (Error Porcentual Abs Med):  {metrics['MAPE']:.2f}%
    
    Métrica de Ajuste:
    ------------------
    R² (Coeficiente de Determinación): {metrics['R2']:.4f}
    
    Interpretación:
    ---------------
    - El modelo predice con un error promedio de {metrics['MAE']:.2f} kWh
    - El R² de {metrics['R2']:.4f} indica que el modelo explica el 
      {metrics['R2']*100:.1f}% de la varianza en los datos
    """
    
    # Evaluación cualitativa del R²
    if metrics['R2'] > 0.9:
        report += "\n    ✓ Excelente ajuste del modelo"
    elif metrics['R2'] > 0.7:
        report += "\n    ✓ Buen ajuste del modelo"
    elif metrics['R2'] > 0.5:
        report += "\n    ⚠ Ajuste moderado del modelo"
    else:
        report += "\n    ✗ Ajuste pobre del modelo - considerar mejoras"
    
    report += "\n    ========================================"
    
    return report


def compare_models(
    results: Dict[str, Dict[str, float]]
) -> pd.DataFrame:
    """
    Compara múltiples modelos basándose en sus métricas
    
    Args:
        results: Diccionario con {nombre_modelo: métricas}
        
    Returns:
        DataFrame con la comparación
    """
    comparison_df = pd.DataFrame(results).T
    comparison_df = comparison_df.sort_values('R2', ascending=False)
    
    return comparison_df
