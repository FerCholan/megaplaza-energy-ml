"""
Funciones de clustering con K-Means
"""
import joblib
import numpy as np
import pandas as pd
from typing import Optional, Tuple
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def train_clustering_model(
    X: pd.DataFrame,
    n_clusters: int = 3,
    random_state: int = 42
) -> KMeans:
    """
    Entrena un modelo de K-Means
    
    Args:
        X: DataFrame con las características
        n_clusters: Número de clusters
        random_state: Semilla para reproducibilidad
        
    Returns:
        Modelo K-Means entrenado
    """
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    model.fit(X)
    return model


def predict_cluster(model: KMeans, X: pd.DataFrame) -> np.ndarray:
    """
    Predice el cluster para nuevos datos
    
    Args:
        model: Modelo K-Means entrenado
        X: DataFrame con las características
        
    Returns:
        Array con las predicciones de cluster
    """
    return model.predict(X)


def calculate_inertia(
    X: pd.DataFrame,
    max_k: int = 10
) -> Tuple[list, list]:
    """
    Calcula la inercia para diferentes valores de K (método del codo)
    
    Args:
        X: DataFrame con las características
        max_k: Máximo número de clusters a probar
        
    Returns:
        Tupla con (lista de K, lista de inercias)
    """
    inertias = []
    k_values = range(2, max_k + 1)
    
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X)
        inertias.append(model.inertia_)
    
    return list(k_values), inertias


def visualize_clusters_pca(
    X: pd.DataFrame,
    labels: np.ndarray,
    title: str = "Visualización de Clusters con PCA"
) -> plt.Figure:
    """
    Visualiza los clusters usando PCA para reducir dimensionalidad
    
    Args:
        X: DataFrame con las características
        labels: Array con las etiquetas de cluster
        title: Título del gráfico
        
    Returns:
        Figura de matplotlib
    """
    # Reducir a 2 dimensiones con PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Graficar cada cluster
    for cluster in np.unique(labels):
        mask = labels == cluster
        ax.scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            label=f'Cluster {cluster}',
            alpha=0.6
        )
    
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} varianza)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} varianza)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def get_cluster_characteristics(
    df: pd.DataFrame,
    labels: np.ndarray,
    features: list
) -> pd.DataFrame:
    """
    Obtiene las características de cada cluster
    
    Args:
        df: DataFrame con los datos originales
        labels: Array con las etiquetas de cluster
        features: Lista de columnas a analizar
        
    Returns:
        DataFrame con estadísticas por cluster
    """
    df_with_clusters = df.copy()
    df_with_clusters['cluster'] = labels
    
    # Calcular estadísticas por cluster
    stats = df_with_clusters.groupby('cluster')[features].agg(['mean', 'std', 'min', 'max'])
    
    return stats


def save_model(model: KMeans, path: str) -> bool:
    """
    Guarda el modelo en disco
    
    Args:
        model: Modelo K-Means
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


def load_model(path: str) -> Optional[KMeans]:
    """
    Carga un modelo desde disco
    
    Args:
        path: Ruta del modelo
        
    Returns:
        Modelo K-Means o None si hay error
    """
    try:
        model = joblib.load(path)
        return model
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return None
