# 🚀 Guía de Uso Después del Entrenamiento

Esta guía te explica qué hacer después de haber entrenado los modelos con tu dataset `datos_retail_para_modelos.csv`.

## 📋 Tabla de Contenidos

1. [Verificación Inicial](#verificación-inicial)
2. [Opciones de Uso](#opciones-de-uso)
3. [Opción 1: Usar la API REST](#opción-1-usar-la-api-rest)
4. [Opción 2: Usar el Dashboard Streamlit](#opción-2-usar-el-dashboard-streamlit)
5. [Opción 3: Usar los Notebooks](#opción-3-usar-los-notebooks)
6. [Opción 4: Integración Personalizada](#opción-4-integración-personalizada)
7. [Mantenimiento y Actualización](#mantenimiento-y-actualización)

---

## ✅ Verificación Inicial

Antes de empezar, verifica que el entrenamiento fue exitoso:

```bash
# Desde la raíz del proyecto
ls -lh ml/models/
```

Debes ver estos archivos:
- ✅ `forecasting_model.pkl` (~5-50 MB)
- ✅ `feature_columns.pkl` (~1 KB)
- ✅ `clustering_model.pkl` (~1-5 MB)
- ✅ `clustering_scaler.pkl` (~1-5 KB)
- ✅ `clustering_columns.pkl` (~1 KB)

Si faltan archivos, regresa a [ENTRENAMIENTO.md](ENTRENAMIENTO.md).

---

## 🎯 Opciones de Uso

Tienes **4 formas principales** de usar los modelos entrenados:

| Opción | Mejor Para | Complejidad | Requiere Docker |
|--------|-----------|-------------|-----------------|
| **API REST** | Integración con otras aplicaciones | Media | Sí (recomendado) |
| **Dashboard Streamlit** | Análisis visual e interactivo | Baja | Sí (recomendado) |
| **Notebooks Jupyter** | Exploración y experimentación | Baja | No |
| **Código Python** | Integración personalizada | Alta | No |

---

## 🔧 Opción 1: Usar la API REST

La API REST permite hacer predicciones y obtener insights desde cualquier aplicación.

### 1.1 Iniciar la API con Docker (Recomendado)

```bash
# Desde la raíz del proyecto
docker-compose up -d backend
```

La API estará disponible en: `http://localhost:8000`

### 1.2 Verificar que la API está funcionando

```bash
curl http://localhost:8000/health
```

Deberías ver: `{"status":"healthy"}`

### 1.3 Ver la Documentación Interactiva

Abre en tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 1.4 Hacer una Predicción de Consumo

**Ejemplo con cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "pies_cuadrados": 9045,
    "ano_construccion": 2016,
    "temperatura_aire": 25.0,
    "cobertura_nubes": 6.0,
    "presion_nivel_mar": 1019.7,
    "velocidad_viento": 0.0,
    "mes": 1,
    "dia_del_ano": 1,
    "dia_de_la_semana": 4,
    "hora_del_dia": 0,
    "es_fin_de_semana": 0
  }'
```

**Ejemplo con Python:**

```python
import requests

url = "http://localhost:8000/api/v1/ml/predict"
data = {
    "pies_cuadrados": 9045,
    "ano_construccion": 2016,
    "temperatura_aire": 25.0,
    "cobertura_nubes": 6.0,
    "presion_nivel_mar": 1019.7,
    "velocidad_viento": 0.0,
    "mes": 1,
    "dia_del_ano": 1,
    "dia_de_la_semana": 4,
    "hora_del_dia": 0,
    "es_fin_de_semana": 0
}

response = requests.post(url, json=data)
print(f"Consumo predicho: {response.json()['consumo_predicho']} kWh")
```

**Respuesta esperada:**

```json
{
  "consumo_predicho": 53.24,
  "cluster": 1,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 1.5 Obtener Información del Cluster

```bash
curl -X POST "http://localhost:8000/api/v1/ml/cluster" \
  -H "Content-Type: application/json" \
  -d '{
    "pies_cuadrados": 9045,
    "temperatura_aire": 25.0,
    "hora_del_dia": 14,
    "dia_de_la_semana": 2
  }'
```

### 1.6 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/ml/predict` | POST | Predice consumo energético |
| `/api/v1/ml/cluster` | POST | Identifica cluster de consumo |
| `/api/v1/ml/batch-predict` | POST | Predicciones en lote |
| `/health` | GET | Estado de salud de la API |

---

## 📊 Opción 2: Usar el Dashboard Streamlit

El dashboard ofrece una interfaz visual para explorar predicciones y análisis.

### 2.1 Iniciar el Dashboard

**Con Docker:**

```bash
docker-compose up -d frontend
```

**Sin Docker:**

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 2.2 Acceder al Dashboard

Abre en tu navegador: `http://localhost:8501`

### 2.3 Funcionalidades del Dashboard

1. **📈 Panel Principal**
   - Vista general del consumo
   - Gráficos de tendencias
   - Estadísticas en tiempo real

2. **🔮 Predicciones**
   - Formulario interactivo para predecir consumo
   - Visualización de resultados
   - Comparación con histórico

3. **🎯 Análisis de Clusters**
   - Visualización de patrones de consumo
   - Características de cada cluster
   - Distribución de datos

4. **⚠️ Alertas**
   - Configuración de umbrales
   - Historial de alertas
   - Notificaciones

### 2.4 Hacer una Predicción en el Dashboard

1. Ve a la página **"Predicciones"** en el menú lateral
2. Completa el formulario con los valores:
   - Pies cuadrados: `9045`
   - Temperatura: `25.0`
   - Hora del día: `14`
   - etc.
3. Haz clic en **"Predecir Consumo"**
4. Verás el resultado y gráficos explicativos

---

## 📓 Opción 3: Usar los Notebooks

Los notebooks permiten experimentación y análisis detallado.

### 3.1 Iniciar Jupyter

```bash
cd ml/notebooks
jupyter notebook
```

### 3.2 Notebooks Disponibles

1. **01_EDA.ipynb** - Análisis Exploratorio de Datos
   - Cargar tu dataset `datos_retail_para_modelos.csv`
   - Visualizar estadísticas
   - Identificar patrones

2. **02_Clustering.ipynb** - Análisis de Clusters
   - Cargar modelo entrenado
   - Visualizar clusters
   - Analizar características

3. **03_Forecasting.ipynb** - Predicciones
   - Cargar modelo de predicción
   - Hacer predicciones
   - Evaluar rendimiento

### 3.3 Ejemplo: Cargar y Usar el Modelo en Notebook

```python
import joblib
import pandas as pd
import numpy as np

# Cargar modelo
model = joblib.load('../models/forecasting_model.pkl')
feature_cols = joblib.load('../models/feature_columns.pkl')

# Preparar datos de ejemplo
data = pd.DataFrame({
    'pies_cuadrados': [9045],
    'ano_construccion': [2016],
    'temperatura_aire': [25.0],
    'cobertura_nubes': [6.0],
    'presion_nivel_mar': [1019.7],
    'velocidad_viento': [0.0],
    'mes': [1],
    'dia_del_ano': [1],
    'dia_de_la_semana': [4],
    'hora_del_dia': [14],
    'es_fin_de_semana': [0]
})

# Predecir
prediction = model.predict(data[feature_cols])
print(f"Consumo predicho: {prediction[0]:.2f} kWh")
```

---

## 💻 Opción 4: Integración Personalizada

Si necesitas integrar los modelos en tu propia aplicación Python.

### 4.1 Crear un Script de Predicción

Crea un archivo `predecir.py`:

```python
#!/usr/bin/env python3
"""
Script para hacer predicciones con los modelos entrenados
"""
import joblib
import pandas as pd
from pathlib import Path


class PredictorEnergia:
    """Clase para hacer predicciones de consumo energético"""
    
    def __init__(self, models_dir='ml/models'):
        """
        Inicializa el predictor cargando los modelos
        
        Args:
            models_dir: Directorio donde están los modelos
        """
        self.models_dir = Path(models_dir)
        
        # Cargar modelo de predicción
        self.forecasting_model = joblib.load(
            self.models_dir / 'forecasting_model.pkl'
        )
        self.feature_cols = joblib.load(
            self.models_dir / 'feature_columns.pkl'
        )
        
        # Cargar modelo de clustering
        self.clustering_model = joblib.load(
            self.models_dir / 'clustering_model.pkl'
        )
        self.clustering_scaler = joblib.load(
            self.models_dir / 'clustering_scaler.pkl'
        )
        self.clustering_cols = joblib.load(
            self.models_dir / 'clustering_columns.pkl'
        )
    
    def predecir_consumo(self, datos: dict) -> float:
        """
        Predice el consumo de energía
        
        Args:
            datos: Diccionario con las características
            
        Returns:
            Consumo predicho en kWh
        """
        # Crear DataFrame
        df = pd.DataFrame([datos])
        
        # Seleccionar columnas requeridas
        X = df[self.feature_cols]
        
        # Predecir
        prediccion = self.forecasting_model.predict(X)[0]
        return float(prediccion)
    
    def predecir_cluster(self, datos: dict) -> int:
        """
        Predice el cluster de consumo
        
        Args:
            datos: Diccionario con las características
            
        Returns:
            Número de cluster (0, 1, o 2)
        """
        # Crear DataFrame
        df = pd.DataFrame([datos])
        
        # Seleccionar columnas y escalar
        X = df[self.clustering_cols]
        X_scaled = self.clustering_scaler.transform(X)
        
        # Predecir
        cluster = self.clustering_model.predict(X_scaled)[0]
        return int(cluster)


def main():
    """Ejemplo de uso"""
    # Crear predictor
    predictor = PredictorEnergia()
    
    # Datos de ejemplo
    datos = {
        'pies_cuadrados': 9045,
        'ano_construccion': 2016,
        'temperatura_aire': 25.0,
        'cobertura_nubes': 6.0,
        'presion_nivel_mar': 1019.7,
        'velocidad_viento': 0.0,
        'mes': 1,
        'dia_del_ano': 1,
        'dia_de_la_semana': 4,
        'hora_del_dia': 14,
        'es_fin_de_semana': 0,
        'consumo_energia': 53.24  # Solo para clustering
    }
    
    # Predecir consumo
    consumo = predictor.predecir_consumo(datos)
    print(f"Consumo predicho: {consumo:.2f} kWh")
    
    # Predecir cluster
    cluster = predictor.predecir_cluster(datos)
    print(f"Cluster: {cluster}")
    
    # Interpretación del cluster
    cluster_nombres = {
        0: "Consumo Bajo",
        1: "Consumo Medio",
        2: "Consumo Alto"
    }
    print(f"Tipo de consumo: {cluster_nombres[cluster]}")


if __name__ == "__main__":
    main()
```

### 4.2 Usar el Script

```bash
python predecir.py
```

### 4.3 Integrar en tu Aplicación

```python
from predecir import PredictorEnergia

# Inicializar una vez
predictor = PredictorEnergia()

# Usar en tu aplicación
def procesar_nuevo_dato(datos):
    consumo = predictor.predecir_consumo(datos)
    cluster = predictor.predecir_cluster(datos)
    
    return {
        'consumo_predicho': consumo,
        'cluster': cluster,
        'alerta': consumo > 100  # Ejemplo de lógica de negocio
    }
```

---

## 🔄 Mantenimiento y Actualización

### Reentrenar Periódicamente

Se recomienda reentrenar los modelos cuando:
- Tengas nuevos datos (mensual/trimestral)
- El rendimiento del modelo disminuya
- Cambien patrones de consumo

```bash
# 1. Actualizar el dataset
cp /nueva/ubicacion/datos_retail_para_modelos.csv data/raw/

# 2. Reentrenar
cd ml/src
python train_models.py

# 3. Reiniciar servicios (si usas Docker)
docker-compose restart backend frontend
```

### Monitorear Rendimiento

Crea un script de monitoreo `ml/src/monitor_modelo.py`:

```python
import joblib
import pandas as pd
from evaluation import calculate_metrics

# Cargar modelo
model = joblib.load('../models/forecasting_model.pkl')

# Cargar datos nuevos
df_new = pd.read_csv('../../data/raw/datos_nuevos.csv')

# Evaluar
X_test = df_new[feature_cols]
y_test = df_new['consumo_energia']
y_pred = model.predict(X_test)

metrics = calculate_metrics(y_test.values, y_pred)
print(f"R² actual: {metrics['R2']:.4f}")

# Alerta si el rendimiento baja
if metrics['R2'] < 0.70:
    print("⚠️ ALERTA: El modelo necesita reentrenamiento")
```

### Versionado de Modelos

Mantén un historial de versiones:

```bash
# Backup antes de reentrenar
cp ml/models/forecasting_model.pkl ml/models/forecasting_model_v1.pkl

# Después del reentrenamiento
mv ml/models/forecasting_model.pkl ml/models/forecasting_model_v2.pkl
```

---

## 📈 Casos de Uso Reales

### 1. Predecir Consumo para el Día Siguiente

```python
import pandas as pd
from datetime import datetime, timedelta

predictor = PredictorEnergia()

# Generar predicciones para mañana (cada hora)
tomorrow = datetime.now() + timedelta(days=1)
predicciones = []

for hora in range(24):
    datos = {
        'pies_cuadrados': 9045,
        'ano_construccion': 2016,
        'temperatura_aire': 25.0,  # Usar pronóstico del clima
        'cobertura_nubes': 6.0,
        'presion_nivel_mar': 1019.7,
        'velocidad_viento': 0.0,
        'mes': tomorrow.month,
        'dia_del_ano': tomorrow.timetuple().tm_yday,
        'dia_de_la_semana': tomorrow.weekday(),
        'hora_del_dia': hora,
        'es_fin_de_semana': int(tomorrow.weekday() >= 5)
    }
    
    consumo = predictor.predecir_consumo(datos)
    predicciones.append({
        'hora': hora,
        'consumo_predicho': consumo
    })

df_pred = pd.DataFrame(predicciones)
print(df_pred)
print(f"\nConsumo total predicho: {df_pred['consumo_predicho'].sum():.2f} kWh")
```

### 2. Detectar Anomalías

```python
# Predecir consumo esperado
consumo_esperado = predictor.predecir_consumo(datos)

# Comparar con consumo real
consumo_real = 150.0  # Obtener de sensores

# Detectar anomalía
diferencia = abs(consumo_real - consumo_esperado)
porcentaje_diferencia = (diferencia / consumo_esperado) * 100

if porcentaje_diferencia > 20:
    print(f"⚠️ ANOMALÍA DETECTADA:")
    print(f"   Esperado: {consumo_esperado:.2f} kWh")
    print(f"   Real: {consumo_real:.2f} kWh")
    print(f"   Diferencia: {porcentaje_diferencia:.1f}%")
```

### 3. Optimizar Horarios de Operación

```python
# Encontrar las horas de menor consumo predicho
horarios = []
for hora in range(24):
    datos['hora_del_dia'] = hora
    consumo = predictor.predecir_consumo(datos)
    horarios.append({'hora': hora, 'consumo': consumo})

df_horarios = pd.DataFrame(horarios)
df_horarios = df_horarios.sort_values('consumo')

print("Mejores horarios (menor consumo):")
print(df_horarios.head(5))
```

---

## ✅ Checklist de Uso

- [ ] Modelos entrenados y verificados
- [ ] API REST funcionando (si la usas)
- [ ] Dashboard accesible (si lo usas)
- [ ] Scripts de predicción probados
- [ ] Documentación revisada
- [ ] Plan de reentrenamiento definido
- [ ] Sistema de monitoreo configurado

---

## 🆘 Troubleshooting

### Problema: "Model file not found"

```bash
# Verificar que los modelos existen
ls -lh ml/models/*.pkl

# Si no existen, reentrenar
cd ml/src && python train_models.py
```

### Problema: "Prediction returns NaN"

- Verifica que los datos de entrada sean válidos
- Asegúrate de pasar todas las características requeridas
- Revisa que no haya valores nulos

### Problema: La API no se conecta

```bash
# Verificar que el contenedor está corriendo
docker ps | grep backend

# Ver logs
docker logs megaplaza-backend

# Reiniciar
docker-compose restart backend
```

---

## 📚 Recursos Adicionales

- [ENTRENAMIENTO.md](ENTRENAMIENTO.md) - Cómo entrenar los modelos
- [API.md](API.md) - Documentación completa de la API
- [README.md](../README.md) - Información general del proyecto
- Notebooks en `ml/notebooks/` - Ejemplos interactivos

---

## 🎓 Conclusión

¡Felicitaciones! Ahora sabes cómo usar los modelos entrenados con tu dataset personalizado. 

**Recuerda**:
- Los modelos son tan buenos como los datos con los que se entrenan
- Reentrenar periódicamente mejora la precisión
- Monitorear el rendimiento ayuda a detectar cuándo reentrenar
- La experimentación en notebooks ayuda a entender mejor los resultados

**¿Preguntas?** Consulta la documentación o abre un issue en el repositorio.

---

**Última actualización**: 2024
**Versión**: 1.0
