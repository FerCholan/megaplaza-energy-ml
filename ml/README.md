# 🤖 Módulo de Machine Learning

Este directorio contiene todo lo relacionado con el entrenamiento, evaluación y uso de modelos de Machine Learning para predicción y análisis de consumo energético.

## 📁 Estructura

```
ml/
├── src/                           # Código fuente de ML
│   ├── preprocessing.py           # Funciones de preprocesamiento
│   ├── forecasting.py            # Modelos de predicción
│   ├── clustering.py             # Modelos de clustering
│   ├── evaluation.py             # Métricas y evaluación
│   ├── train_models.py           # Script de entrenamiento ⭐
│   └── ejemplo_prediccion.py     # Script de ejemplo
├── notebooks/                     # Jupyter notebooks
│   ├── 01_EDA.ipynb              # Análisis exploratorio
│   ├── 02_Clustering.ipynb       # Análisis de clusters
│   └── 03_Forecasting.ipynb      # Predicciones
├── models/                        # Modelos entrenados (generados)
│   ├── forecasting_model.pkl
│   ├── feature_columns.pkl
│   ├── clustering_model.pkl
│   ├── clustering_scaler.pkl
│   └── clustering_columns.pkl
└── requirements.txt               # Dependencias Python
```

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
cd ml
pip install -r requirements.txt
```

### 2. Entrenar Modelos

```bash
# Asegúrate de tener el dataset en data/raw/datos_retail_para_modelos.csv
cd src
python train_models.py
```

### 3. Verificar Instalación

```bash
python ejemplo_prediccion.py
```

## 📊 Modelos Implementados

### Modelo de Predicción (Forecasting)

**Algoritmo**: XGBoost Regressor

**Características de entrada**:
- `pies_cuadrados`: Área del edificio
- `ano_construccion`: Año de construcción
- `temperatura_aire`: Temperatura en °C
- `cobertura_nubes`: Cobertura de nubes (0-10)
- `presion_nivel_mar`: Presión atmosférica (hPa)
- `velocidad_viento`: Velocidad del viento (m/s)
- `mes`: Mes del año (1-12)
- `dia_del_ano`: Día del año (1-365)
- `dia_de_la_semana`: Día de la semana (0-6)
- `hora_del_dia`: Hora (0-23)
- `es_fin_de_semana`: Booleano

**Salida**: Consumo energético en kWh

**Métricas típicas**:
- R² > 0.85 (excelente)
- MAE < 50 kWh
- MAPE < 10%

### Modelo de Clustering

**Algoritmo**: K-Means (3 clusters)

**Características de entrada**:
- `pies_cuadrados`: Área del edificio
- `temperatura_aire`: Temperatura
- `hora_del_dia`: Hora
- `dia_de_la_semana`: Día de la semana
- `consumo_energia`: Consumo real

**Salida**: Cluster (0, 1, o 2)

**Interpretación**:
- **Cluster 0**: Consumo bajo (horarios nocturnos/baja ocupación)
- **Cluster 1**: Consumo medio (operación normal)
- **Cluster 2**: Consumo alto (horarios pico)

## 📝 Uso de los Scripts

### train_models.py

Script principal para entrenar ambos modelos.

```bash
cd src
python train_models.py
```

**Salida**:
- Modelos entrenados en `ml/models/`
- Reporte de métricas en consola
- Importancia de características

**Tiempo estimado**: 5-15 minutos (depende del tamaño del dataset)

### ejemplo_prediccion.py

Script de demostración de cómo usar los modelos.

```bash
cd src
python ejemplo_prediccion.py
```

**Funcionalidades**:
- Verifica que los modelos existan
- Carga los modelos
- Hace predicciones de ejemplo
- Muestra casos de uso prácticos

## 📓 Notebooks Jupyter

### 01_EDA.ipynb - Análisis Exploratorio

**Propósito**: Entender tus datos antes de entrenar modelos

**Contenido**:
- Carga del dataset
- Estadísticas descriptivas
- Visualizaciones
- Detección de valores nulos y outliers
- Correlaciones

**Uso**:
```bash
cd notebooks
jupyter notebook 01_EDA.ipynb
```

### 02_Clustering.ipynb - Análisis de Clusters

**Propósito**: Identificar patrones de consumo

**Contenido**:
- Entrenamiento de K-Means
- Visualización con PCA
- Características de cada cluster
- Método del codo para seleccionar K

**Uso**:
```bash
cd notebooks
jupyter notebook 02_Clustering.ipynb
```

### 03_Forecasting.ipynb - Predicciones

**Propósito**: Entrenar y evaluar modelos de predicción

**Contenido**:
- Entrenamiento de modelos (XGBoost, Random Forest, etc.)
- Evaluación con métricas
- Visualización de predicciones
- Análisis de importancia de características
- Optimización de hiperparámetros

**Uso**:
```bash
cd notebooks
jupyter notebook 03_Forecasting.ipynb
```

## 🔧 Módulos de Código

### preprocessing.py

Funciones de preprocesamiento de datos.

**Funciones principales**:
- `load_data(path)`: Carga CSV
- `clean_data(df)`: Limpia datos (nulos, outliers)
- `create_features(df)`: Feature engineering
- `scale_features(df, features)`: Normalización
- `prepare_train_test_split(...)`: Split temporal

**Ejemplo**:
```python
from preprocessing import load_data, clean_data

df = load_data('../data/raw/datos_retail_para_modelos.csv')
df_clean = clean_data(df)
```

### forecasting.py

Funciones para modelos de predicción.

**Funciones principales**:
- `train_forecasting_model(X, y, model_type)`: Entrena modelo
- `predict_consumption(model, X)`: Hace predicciones
- `get_feature_importance(model, features)`: Importancia
- `save_model(model, path)`: Guarda modelo
- `load_model(path)`: Carga modelo
- `tune_hyperparameters(X, y)`: Optimización

**Ejemplo**:
```python
from forecasting import train_forecasting_model, predict_consumption

model = train_forecasting_model(X_train, y_train, model_type='xgboost')
predictions = predict_consumption(model, X_test)
```

### clustering.py

Funciones para clustering.

**Funciones principales**:
- `train_clustering_model(X, n_clusters)`: Entrena K-Means
- `predict_cluster(model, X)`: Predice cluster
- `calculate_inertia(X, max_k)`: Método del codo
- `visualize_clusters_pca(X, labels)`: Visualización
- `get_cluster_characteristics(df, labels)`: Estadísticas

**Ejemplo**:
```python
from clustering import train_clustering_model, predict_cluster

model = train_clustering_model(X, n_clusters=3)
clusters = predict_cluster(model, X_new)
```

### evaluation.py

Funciones de evaluación de modelos.

**Funciones principales**:
- `calculate_metrics(y_true, y_pred)`: MAE, RMSE, R², MAPE
- `plot_predictions(y_true, y_pred)`: Gráficos
- `plot_residuals(y_true, y_pred)`: Análisis de residuos
- `generate_report(metrics)`: Reporte en texto
- `compare_models(results)`: Comparación

**Ejemplo**:
```python
from evaluation import calculate_metrics, generate_report

metrics = calculate_metrics(y_test, y_pred)
print(generate_report(metrics, "Mi Modelo"))
```

## 🎯 Workflows Comunes

### Workflow 1: Entrenar por Primera Vez

```bash
# 1. Verificar dataset
ls ../data/raw/datos_retail_para_modelos.csv

# 2. Entrenar modelos
cd src
python train_models.py

# 3. Verificar resultados
python ejemplo_prediccion.py

# 4. Explorar en notebooks
cd ../notebooks
jupyter notebook
```

### Workflow 2: Reentrenar con Datos Actualizados

```bash
# 1. Backup de modelos actuales
cp models/*.pkl models/backup/

# 2. Actualizar dataset
cp /nueva/ubicacion/datos.csv ../data/raw/datos_retail_para_modelos.csv

# 3. Reentrenar
cd src
python train_models.py

# 4. Comparar métricas
# (ver consola o notebooks)
```

### Workflow 3: Experimentar con Hiperparámetros

```bash
# Usar notebooks para experimentación
cd notebooks
jupyter notebook 03_Forecasting.ipynb

# Modificar parámetros en el notebook
# Comparar resultados
# Actualizar train_models.py con mejores parámetros
```

### Workflow 4: Hacer Predicciones en Producción

```python
# Script personalizado
import joblib
import pandas as pd

# Cargar modelo
model = joblib.load('models/forecasting_model.pkl')
feature_cols = joblib.load('models/feature_columns.pkl')

# Preparar datos
datos = {...}  # Tus datos
df = pd.DataFrame([datos])

# Predecir
consumo = model.predict(df[feature_cols])[0]
print(f"Consumo predicho: {consumo:.2f} kWh")
```

## 📈 Optimización de Modelos

### Mejorar el Rendimiento

1. **Más datos**: Recolectar más datos históricos
2. **Feature engineering**: Crear nuevas características
3. **Hiperparámetros**: Usar `tune_hyperparameters()`
4. **Ensemble**: Combinar múltiples modelos
5. **Limpieza**: Mejorar calidad de datos

### Ejemplo de Optimización

```python
from forecasting import tune_hyperparameters

# Encontrar mejores hiperparámetros
best_params = tune_hyperparameters(X_train, y_train, model_type='xgboost', cv=5)
print("Mejores parámetros:", best_params)

# Entrenar con mejores parámetros
model = train_forecasting_model(X_train, y_train, model_type='xgboost', **best_params)
```

## 🐛 Solución de Problemas

### Error: "Model not found"

```bash
# Verifica que entrenaste los modelos
ls models/

# Si no existen, entrena
cd src && python train_models.py
```

### Error: "Feature mismatch"

Las características deben coincidir exactamente con las usadas en el entrenamiento.

```python
# Ver características requeridas
feature_cols = joblib.load('models/feature_columns.pkl')
print(feature_cols)

# Asegúrate de tener todas
```

### Bajo Rendimiento del Modelo (R² < 0.5)

1. Verifica la calidad de tus datos (notebook 01_EDA.ipynb)
2. Asegúrate de tener suficientes datos (>1000 registros)
3. Revisa correlaciones entre variables
4. Prueba diferentes modelos
5. Considera agregar más características

### Error de Memoria

```python
# Entrenar con una muestra
df_sample = df.sample(n=50000, random_state=42)
```

## 📚 Recursos Adicionales

- **Documentación completa**: [docs/ENTRENAMIENTO.md](../docs/ENTRENAMIENTO.md)
- **Guía de uso**: [docs/USO_POST_ENTRENAMIENTO.md](../docs/USO_POST_ENTRENAMIENTO.md)
- **Inicio rápido**: [docs/INICIO_RAPIDO.md](../docs/INICIO_RAPIDO.md)

## 🔗 Integración con Otros Componentes

### Con la API (Backend)

Los modelos se cargan automáticamente en el backend:

```python
# backend/app/services/ml_service.py
model = joblib.load('ml/models/forecasting_model.pkl')
```

### Con el Dashboard (Frontend)

El frontend consulta la API para obtener predicciones.

### Con Notebooks

Los notebooks cargan los modelos directamente para análisis.

## ✅ Checklist de Verificación

Antes de considerar el módulo ML listo:

- [ ] Dataset en `../data/raw/datos_retail_para_modelos.csv`
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Script de entrenamiento ejecutado sin errores
- [ ] 5 archivos de modelos en `models/`
- [ ] Script de ejemplo funciona correctamente
- [ ] R² del modelo > 0.70
- [ ] Documentación revisada

---

**Última actualización**: 2024
**Versión**: 1.0
