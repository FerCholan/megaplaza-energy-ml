# 📚 Guía de Entrenamiento de Modelos

Esta guía explica cómo entrenar los modelos de Machine Learning usando tu dataset personalizado `datos_retail_para_modelos.csv`.

## 📋 Requisitos Previos

### 1. Dataset Preparado

Asegúrate de tener el archivo `datos_retail_para_modelos.csv` con la siguiente estructura:

```csv
consumo_energia,pies_cuadrados,ano_construccion,temperatura_aire,cobertura_nubes,presion_nivel_mar,velocidad_viento,mes,dia_del_ano,dia_de_la_semana,hora_del_dia,es_fin_de_semana,medidor_electricidad,medidor_agua_fria
0.0,59071,1980.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
53.2397,9045,2016.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
```

**Columnas requeridas:**
- `consumo_energia`: Consumo de energía en kWh (target variable)
- `pies_cuadrados`: Área del edificio en pies cuadrados
- `ano_construccion`: Año de construcción
- `temperatura_aire`: Temperatura del aire en °C
- `cobertura_nubes`: Cobertura de nubes (0-10)
- `presion_nivel_mar`: Presión atmosférica en hPa
- `velocidad_viento`: Velocidad del viento en m/s
- `mes`: Mes del año (1-12)
- `dia_del_ano`: Día del año (1-365)
- `dia_de_la_semana`: Día de la semana (0-6)
- `hora_del_dia`: Hora del día (0-23)
- `es_fin_de_semana`: Booleano indicando fin de semana
- `medidor_electricidad`: Tipo de medidor eléctrico
- `medidor_agua_fria`: Tipo de medidor de agua fría

### 2. Dependencias Instaladas

```bash
# Instalar dependencias de ML
cd ml
pip install -r requirements.txt
```

## 🚀 Paso a Paso: Entrenar los Modelos

### Paso 1: Colocar el Dataset

Copia tu archivo `datos_retail_para_modelos.csv` en el directorio correcto:

```bash
# Desde la raíz del proyecto
cp /ruta/a/tu/datos_retail_para_modelos.csv data/raw/
```

Verifica que el archivo esté en el lugar correcto:

```bash
ls -lh data/raw/datos_retail_para_modelos.csv
```

### Paso 2: Ejecutar el Script de Entrenamiento

```bash
# Desde la raíz del proyecto
cd ml/src
python train_models.py
```

Este script hará lo siguiente:

1. **Carga de datos**: Lee el archivo CSV
2. **Limpieza de datos**: Elimina duplicados, outliers y valores nulos
3. **Entrenamiento del modelo de predicción**:
   - Usa XGBoost con 200 estimadores
   - Split 80/20 para entrenamiento/prueba
   - Evalúa con métricas MAE, RMSE, R², MAPE
   - Guarda el modelo entrenado
4. **Entrenamiento del modelo de clustering**:
   - Usa K-Means con 3 clusters
   - Normaliza los datos con StandardScaler
   - Identifica patrones de consumo (bajo, medio, alto)
   - Guarda el modelo y el scaler

### Paso 3: Verificar los Modelos Generados

Después del entrenamiento, verifica que se hayan creado los siguientes archivos:

```bash
ls -lh ml/models/
```

Deberías ver:
- `forecasting_model.pkl` - Modelo de predicción de consumo
- `feature_columns.pkl` - Columnas usadas en el modelo de predicción
- `clustering_model.pkl` - Modelo de clustering
- `clustering_scaler.pkl` - Scaler para normalización
- `clustering_columns.pkl` - Columnas usadas en clustering

## 📊 Interpretación de Resultados

### Métricas del Modelo de Predicción

Al finalizar el entrenamiento, verás un reporte como este:

```
========================================
REPORTE DE EVALUACIÓN - XGBoost - Predicción de Consumo
========================================

Métricas de Error:
------------------
MAE (Error Absoluto Medio):       XX.XX kWh
MSE (Error Cuadrático Medio):     XXXX.XX kWh²
RMSE (Raíz del ECM):              XX.XX kWh
MAPE (Error Porcentual Abs Med):  X.XX%

Métrica de Ajuste:
------------------
R² (Coeficiente de Determinación): 0.XXXX

✓ Excelente ajuste del modelo
========================================
```

**¿Qué significan estas métricas?**

- **MAE**: Error promedio en kWh. Menor es mejor.
- **RMSE**: Similar a MAE pero penaliza más los errores grandes.
- **MAPE**: Error porcentual. <10% es excelente.
- **R²**: Qué tan bien el modelo explica la varianza (0-1). >0.85 es muy bueno.

### Importancia de Características

El script también muestra qué variables son más importantes:

```
Importancia de características:
              feature  importance
    pies_cuadrados      0.350
  temperatura_aire      0.220
      hora_del_dia      0.180
...
```

### Resultados del Clustering

Verás la distribución de los clusters:

```
Distribución de clusters:
   - Cluster 0: 35000 muestras (31.2%)  <- Consumo bajo
   - Cluster 1: 45000 muestras (40.1%)  <- Consumo medio
   - Cluster 2: 32000 muestras (28.7%)  <- Consumo alto
```

## 🔧 Personalización del Entrenamiento

### Ajustar Hiperparámetros del Modelo de Predicción

Edita `ml/src/train_models.py` en la función `entrenar_modelo_prediccion()`:

```python
model = train_forecasting_model(
    X_train,
    y_train,
    model_type='xgboost',
    n_estimators=200,      # Número de árboles (aumentar para más precisión)
    max_depth=6,           # Profundidad máxima (3-10 recomendado)
    learning_rate=0.1,     # Tasa de aprendizaje (0.01-0.3)
    random_state=42
)
```

### Cambiar el Número de Clusters

En la función `entrenar_modelo_clustering()`:

```python
model = train_clustering_model(
    X_scaled_df, 
    n_clusters=3,  # Cambiar a 4, 5, etc. según necesites
    random_state=42
)
```

### Modificar el Split de Entrenamiento/Prueba

En `entrenar_modelo_prediccion()`:

```python
X_train, X_test, y_train, y_test = prepare_train_test_split(
    df, 
    target_col='consumo_energia',
    feature_cols=feature_cols,
    test_size=0.2  # Cambiar a 0.1, 0.3, etc. (10%, 30%)
)
```

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo de datos"

**Problema**: El script no encuentra `datos_retail_para_modelos.csv`

**Solución**:
```bash
# Verifica que el archivo esté en el lugar correcto
ls data/raw/datos_retail_para_modelos.csv

# Si no existe, crea el directorio y copia el archivo
mkdir -p data/raw
cp /ruta/a/tu/archivo.csv data/raw/datos_retail_para_modelos.csv
```

### Error: "KeyError: 'columna_nombre'"

**Problema**: El dataset no tiene todas las columnas requeridas

**Solución**: Verifica que tu CSV tenga todas las columnas listadas en "Requisitos Previos". Puedes verificar con:

```python
import pandas as pd
df = pd.read_csv('data/raw/datos_retail_para_modelos.csv')
print(df.columns.tolist())
```

### El Modelo Tiene Bajo R² (<0.5)

**Posibles causas**:
1. Dataset muy pequeño (se recomienda >1000 registros)
2. Muchos valores nulos o inconsistentes
3. Las características no son predictivas del consumo

**Soluciones**:
- Recolectar más datos
- Limpiar mejor los datos antes de entrenar
- Añadir más características relevantes
- Probar diferentes modelos (`random_forest`, `gradient_boosting`)

### Error de Memoria

**Problema**: El dataset es muy grande

**Solución**:
```python
# Entrenar con una muestra del dataset
df_sample = df.sample(n=50000, random_state=42)
```

## 🔄 Reentrenar los Modelos

Para reentrenar con datos actualizados:

1. Actualiza el archivo `datos_retail_para_modelos.csv` con nuevos datos
2. Ejecuta nuevamente el script:
   ```bash
   cd ml/src
   python train_models.py
   ```
3. Los modelos antiguos serán sobrescritos automáticamente

## 📈 Validación Avanzada

### Validación Cruzada

Para una evaluación más robusta, puedes usar validación cruzada:

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    model, 
    X_train, 
    y_train, 
    cv=5,  # 5 folds
    scoring='r2'
)
print(f"R² promedio: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### Optimización de Hiperparámetros

Para encontrar los mejores hiperparámetros automáticamente:

```python
from forecasting import tune_hyperparameters

best_params = tune_hyperparameters(
    X_train, 
    y_train, 
    model_type='xgboost',
    cv=5
)
print("Mejores parámetros:", best_params)
```

## 📝 Logs y Seguimiento

El script muestra progreso detallado en consola. Para guardar los logs:

```bash
cd ml/src
python train_models.py 2>&1 | tee training_log_$(date +%Y%m%d_%H%M%S).txt
```

## ✅ Checklist Final

Después del entrenamiento, verifica:

- [ ] El script se ejecutó sin errores
- [ ] Los 5 archivos de modelos se crearon en `ml/models/`
- [ ] El R² del modelo de predicción es >0.7
- [ ] Los 3 clusters se distribuyeron razonablemente
- [ ] Las métricas son aceptables para tu caso de uso

## 🎯 Próximos Pasos

Una vez entrenados los modelos, puedes:

1. **Usar los modelos en la API**: Ver [USO_POST_ENTRENAMIENTO.md](USO_POST_ENTRENAMIENTO.md)
2. **Explorar en notebooks**: Ver notebooks en `ml/notebooks/`
3. **Integrar con el dashboard**: Los modelos se cargarán automáticamente
4. **Hacer predicciones**: Usar los endpoints de la API

## 📞 Soporte

Si encuentras problemas:
1. Revisa esta documentación
2. Verifica los logs de error
3. Consulta los notebooks de ejemplo en `ml/notebooks/`
4. Abre un issue en el repositorio

---

**Última actualización**: 2024
**Versión**: 1.0
