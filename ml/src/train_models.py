"""
Script para entrenar modelos de Machine Learning con el dataset real
datos_retail_para_modelos.csv
"""
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from datetime import datetime

# Importar módulos locales
from preprocessing import clean_data, create_features, scale_features, prepare_train_test_split
from forecasting import train_forecasting_model, predict_consumption, get_feature_importance
from clustering import train_clustering_model, predict_cluster, get_cluster_characteristics
from evaluation import calculate_metrics, generate_report


def entrenar_modelo_prediccion(df: pd.DataFrame, guardar_modelo: bool = True) -> dict:
    """
    Entrena el modelo de predicción de consumo energético
    
    Args:
        df: DataFrame con los datos limpios
        guardar_modelo: Si se debe guardar el modelo entrenado
        
    Returns:
        Diccionario con el modelo y métricas
    """
    print("\n" + "="*60)
    print("ENTRENANDO MODELO DE PREDICCIÓN DE CONSUMO")
    print("="*60)
    
    # Seleccionar características para el modelo
    feature_cols = [
        'pies_cuadrados',
        'ano_construccion',
        'temperatura_aire',
        'cobertura_nubes',
        'presion_nivel_mar',
        'velocidad_viento',
        'mes',
        'dia_del_ano',
        'dia_de_la_semana',
        'hora_del_dia',
        'es_fin_de_semana'
    ]
    
    # Convertir booleano a entero si es necesario
    if df['es_fin_de_semana'].dtype == bool:
        df['es_fin_de_semana'] = df['es_fin_de_semana'].astype(int)
    
    # Preparar datos para entrenamiento
    print("\n1. Preparando datos para entrenamiento...")
    X_train, X_test, y_train, y_test = prepare_train_test_split(
        df, 
        target_col='consumo_energia',
        feature_cols=feature_cols,
        test_size=0.2
    )
    
    print(f"   - Tamaño conjunto entrenamiento: {len(X_train)} muestras")
    print(f"   - Tamaño conjunto prueba: {len(X_test)} muestras")
    
    # Entrenar modelo con XGBoost (mejor rendimiento)
    print("\n2. Entrenando modelo XGBoost...")
    model = train_forecasting_model(
        X_train,
        y_train,
        model_type='xgboost',
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    print("   ✓ Modelo entrenado exitosamente")
    
    # Evaluar modelo
    print("\n3. Evaluando modelo en conjunto de prueba...")
    y_pred = predict_consumption(model, X_test)
    metrics = calculate_metrics(y_test.values, y_pred)
    
    # Mostrar reporte
    print(generate_report(metrics, "XGBoost - Predicción de Consumo"))
    
    # Mostrar importancia de características
    print("\n4. Importancia de características:")
    importance_df = get_feature_importance(model, feature_cols)
    print(importance_df.head(10).to_string(index=False))
    
    # Guardar modelo
    if guardar_modelo:
        models_dir = Path(__file__).parent.parent / "models"
        models_dir.mkdir(exist_ok=True)
        
        model_path = models_dir / "forecasting_model.pkl"
        joblib.dump(model, model_path)
        print(f"\n✓ Modelo guardado en: {model_path}")
        
        # Guardar también las columnas de características
        feature_cols_path = models_dir / "feature_columns.pkl"
        joblib.dump(feature_cols, feature_cols_path)
        print(f"✓ Columnas guardadas en: {feature_cols_path}")
    
    return {
        'model': model,
        'metrics': metrics,
        'feature_importance': importance_df,
        'feature_cols': feature_cols
    }


def entrenar_modelo_clustering(df: pd.DataFrame, guardar_modelo: bool = True) -> dict:
    """
    Entrena el modelo de clustering de patrones de consumo
    
    Args:
        df: DataFrame con los datos limpios
        guardar_modelo: Si se debe guardar el modelo entrenado
        
    Returns:
        Diccionario con el modelo y resultados
    """
    print("\n" + "="*60)
    print("ENTRENANDO MODELO DE CLUSTERING")
    print("="*60)
    
    # Seleccionar características para clustering
    feature_cols = [
        'pies_cuadrados',
        'temperatura_aire',
        'hora_del_dia',
        'dia_de_la_semana',
        'consumo_energia'
    ]
    
    print("\n1. Preparando datos para clustering...")
    X = df[feature_cols].copy()
    
    # Normalizar datos
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols, index=X.index)
    
    print(f"   - Total de muestras: {len(X_scaled_df)}")
    
    # Entrenar modelo con K-Means (3 clusters: bajo, medio, alto consumo)
    print("\n2. Entrenando modelo K-Means...")
    model = train_clustering_model(X_scaled_df, n_clusters=3, random_state=42)
    print("   ✓ Modelo entrenado exitosamente")
    
    # Obtener predicciones
    print("\n3. Asignando clusters...")
    labels = predict_cluster(model, X_scaled_df)
    
    # Analizar características de cada cluster
    print("\n4. Características de cada cluster:")
    cluster_stats = get_cluster_characteristics(df, labels, feature_cols)
    print(cluster_stats)
    
    # Contar muestras por cluster
    unique, counts = np.unique(labels, return_counts=True)
    print("\n5. Distribución de clusters:")
    for cluster_id, count in zip(unique, counts):
        pct = (count / len(labels)) * 100
        print(f"   - Cluster {cluster_id}: {count} muestras ({pct:.1f}%)")
    
    # Guardar modelo y scaler
    if guardar_modelo:
        models_dir = Path(__file__).parent.parent / "models"
        models_dir.mkdir(exist_ok=True)
        
        model_path = models_dir / "clustering_model.pkl"
        joblib.dump(model, model_path)
        print(f"\n✓ Modelo guardado en: {model_path}")
        
        scaler_path = models_dir / "clustering_scaler.pkl"
        joblib.dump(scaler, scaler_path)
        print(f"✓ Scaler guardado en: {scaler_path}")
        
        # Guardar columnas de clustering
        cluster_cols_path = models_dir / "clustering_columns.pkl"
        joblib.dump(feature_cols, cluster_cols_path)
        print(f"✓ Columnas guardadas en: {cluster_cols_path}")
    
    return {
        'model': model,
        'scaler': scaler,
        'labels': labels,
        'cluster_stats': cluster_stats,
        'feature_cols': feature_cols
    }


def main():
    """Función principal para entrenar ambos modelos"""
    print("="*60)
    print("SISTEMA DE ENTRENAMIENTO DE MODELOS ML")
    print("Mega Plaza Chimbote - Optimización Energética")
    print("="*60)
    
    # Ruta al dataset
    data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "datos_retail_para_modelos.csv"
    
    # Verificar que existe el archivo
    if not data_path.exists():
        print(f"\n❌ ERROR: No se encontró el archivo de datos en:")
        print(f"   {data_path}")
        print("\nPor favor, coloca el archivo 'datos_retail_para_modelos.csv'")
        print("en el directorio 'data/raw/' antes de ejecutar este script.")
        sys.exit(1)
    
    # Cargar datos
    print(f"\n📂 Cargando datos desde: {data_path.name}")
    df = pd.read_csv(data_path)
    print(f"✓ Dataset cargado: {len(df)} registros, {len(df.columns)} columnas")
    
    # Mostrar primeras filas
    print("\nPrimeras 3 filas del dataset:")
    print(df.head(3).to_string())
    
    # Limpiar datos
    print("\n🧹 Limpiando datos...")
    df_clean = clean_data(df)
    print(f"✓ Datos limpios: {len(df_clean)} registros")
    print(f"  (Se eliminaron {len(df) - len(df_clean)} registros con outliers/nulos)")
    
    # Entrenar modelo de predicción
    try:
        prediccion_results = entrenar_modelo_prediccion(df_clean, guardar_modelo=True)
        print("\n✅ Modelo de predicción entrenado exitosamente")
    except Exception as e:
        print(f"\n❌ Error entrenando modelo de predicción: {e}")
        import traceback
        traceback.print_exc()
    
    # Entrenar modelo de clustering
    try:
        clustering_results = entrenar_modelo_clustering(df_clean, guardar_modelo=True)
        print("\n✅ Modelo de clustering entrenado exitosamente")
    except Exception as e:
        print(f"\n❌ Error entrenando modelo de clustering: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumen final
    print("\n" + "="*60)
    print("ENTRENAMIENTO COMPLETADO")
    print("="*60)
    print("\n✓ Todos los modelos han sido entrenados y guardados")
    print("✓ Los modelos están listos para ser usados en la API")
    print("\nArchivos generados:")
    print("  - ml/models/forecasting_model.pkl")
    print("  - ml/models/feature_columns.pkl")
    print("  - ml/models/clustering_model.pkl")
    print("  - ml/models/clustering_scaler.pkl")
    print("  - ml/models/clustering_columns.pkl")
    print("\n📚 Consulta la documentación en docs/ENTRENAMIENTO.md")
    print("   para más información sobre cómo usar los modelos.")
    print("="*60)


if __name__ == "__main__":
    main()
