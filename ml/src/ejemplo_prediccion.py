#!/usr/bin/env python3
"""
Script de ejemplo para hacer predicciones con los modelos entrenados

Este script muestra cómo cargar y usar los modelos entrenados
para hacer predicciones de consumo energético.
"""
import joblib
import pandas as pd
from pathlib import Path
import sys


def main():
    """Ejemplo de predicción con los modelos entrenados"""
    
    print("="*60)
    print("EJEMPLO DE PREDICCIÓN DE CONSUMO ENERGÉTICO")
    print("="*60)
    
    # Ruta a los modelos
    models_dir = Path(__file__).parent.parent / "models"
    
    # Verificar que los modelos existen
    required_files = [
        'forecasting_model.pkl',
        'feature_columns.pkl',
        'clustering_model.pkl',
        'clustering_scaler.pkl',
        'clustering_columns.pkl'
    ]
    
    print("\n1. Verificando modelos...")
    missing_files = []
    for file in required_files:
        file_path = models_dir / file
        if file_path.exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} - NO ENCONTRADO")
            missing_files.append(file)
    
    if missing_files:
        print("\n❌ ERROR: Faltan archivos de modelos")
        print("Por favor, ejecuta primero el script de entrenamiento:")
        print("   python train_models.py")
        sys.exit(1)
    
    # Cargar modelos
    print("\n2. Cargando modelos...")
    forecasting_model = joblib.load(models_dir / 'forecasting_model.pkl')
    feature_cols = joblib.load(models_dir / 'feature_columns.pkl')
    clustering_model = joblib.load(models_dir / 'clustering_model.pkl')
    clustering_scaler = joblib.load(models_dir / 'clustering_scaler.pkl')
    clustering_cols = joblib.load(models_dir / 'clustering_columns.pkl')
    print("   ✓ Modelos cargados correctamente")
    
    # Datos de ejemplo (basados en tu dataset)
    print("\n3. Preparando datos de ejemplo...")
    ejemplo_datos = {
        'pies_cuadrados': 9045,
        'ano_construccion': 2016.0,
        'temperatura_aire': 25.0,
        'cobertura_nubes': 6.0,
        'presion_nivel_mar': 1019.7,
        'velocidad_viento': 0.0,
        'mes': 1,
        'dia_del_ano': 1,
        'dia_de_la_semana': 4,  # Viernes
        'hora_del_dia': 14,     # 2 PM
        'es_fin_de_semana': 0,
        'consumo_energia': 53.24  # Solo para clustering
    }
    
    print("\n   Datos de entrada:")
    for key, value in ejemplo_datos.items():
        if key != 'consumo_energia':  # No mostrar consumo ya que es lo que vamos a predecir
            print(f"     • {key}: {value}")
    
    # Hacer predicción de consumo
    print("\n4. Prediciendo consumo energético...")
    df_pred = pd.DataFrame([ejemplo_datos])
    X_pred = df_pred[feature_cols]
    
    consumo_predicho = forecasting_model.predict(X_pred)[0]
    print(f"\n   🔮 Consumo predicho: {consumo_predicho:.2f} kWh")
    
    # Hacer predicción de cluster
    print("\n5. Identificando patrón de consumo (cluster)...")
    df_cluster = pd.DataFrame([ejemplo_datos])
    X_cluster = df_cluster[clustering_cols]
    X_cluster_scaled = clustering_scaler.transform(X_cluster)
    
    cluster = clustering_model.predict(X_cluster_scaled)[0]
    
    # Interpretación del cluster
    cluster_interpretacion = {
        0: "Consumo Bajo - Típico de horarios nocturnos o baja ocupación",
        1: "Consumo Medio - Típico de horarios normales de operación",
        2: "Consumo Alto - Típico de horarios pico o alta demanda"
    }
    
    print(f"\n   📊 Cluster: {cluster}")
    print(f"   📝 Interpretación: {cluster_interpretacion.get(cluster, 'Desconocido')}")
    
    # Casos de uso práctico
    print("\n" + "="*60)
    print("EJEMPLOS DE USO PRÁCTICO")
    print("="*60)
    
    # Ejemplo 1: Predecir para diferentes horas del día
    print("\n📅 Ejemplo 1: Predicciones para un día completo")
    print("-" * 60)
    
    predicciones_diarias = []
    for hora in range(0, 24, 6):  # Cada 6 horas
        ejemplo_datos['hora_del_dia'] = hora
        df_temp = pd.DataFrame([ejemplo_datos])
        X_temp = df_temp[feature_cols]
        consumo = forecasting_model.predict(X_temp)[0]
        predicciones_diarias.append((hora, consumo))
    
    print("\n   Hora  | Consumo Predicho")
    print("   " + "-"*25)
    for hora, consumo in predicciones_diarias:
        print(f"   {hora:02d}:00 | {consumo:8.2f} kWh")
    
    consumo_total_dia = sum(c for _, c in predicciones_diarias) * 4  # Multiplicar por 4 porque es cada 6h
    print(f"\n   💡 Consumo total estimado del día: {consumo_total_dia:.2f} kWh")
    
    # Ejemplo 2: Comparar diferentes temperaturas
    print("\n🌡️  Ejemplo 2: Impacto de la temperatura")
    print("-" * 60)
    
    ejemplo_datos['hora_del_dia'] = 14  # Resetear a 2 PM
    temperaturas = [15, 20, 25, 30, 35]
    
    print("\n   Temperatura | Consumo Predicho | Diferencia")
    print("   " + "-"*45)
    consumo_base = None
    for temp in temperaturas:
        ejemplo_datos['temperatura_aire'] = temp
        df_temp = pd.DataFrame([ejemplo_datos])
        X_temp = df_temp[feature_cols]
        consumo = forecasting_model.predict(X_temp)[0]
        
        if consumo_base is None:
            consumo_base = consumo
            diff = 0
        else:
            diff = consumo - consumo_base
        
        print(f"   {temp}°C        | {consumo:8.2f} kWh  | {diff:+7.2f} kWh")
    
    # Resumen final
    print("\n" + "="*60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("="*60)
    print("\n✓ Los modelos están funcionando correctamente")
    print("✓ Puedes usar estos modelos para hacer predicciones")
    print("\n📚 Próximos pasos:")
    print("   1. Lee la documentación en docs/USO_POST_ENTRENAMIENTO.md")
    print("   2. Explora los notebooks en ml/notebooks/")
    print("   3. Integra los modelos en tu aplicación")
    print("   4. Configura la API REST para acceso remoto")
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Ejecución cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
