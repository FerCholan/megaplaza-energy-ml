# 📓 Notebooks de Análisis y Modelado

Esta carpeta contiene notebooks Jupyter para análisis exploratorio, entrenamiento y evaluación de modelos de Machine Learning.

## 📚 Notebooks Disponibles

### 1. 01_EDA.ipynb - Análisis Exploratorio de Datos

**Propósito**: Entender y explorar el dataset `datos_retail_para_modelos.csv`

**Contenido**:
- ✅ Carga y visualización del dataset
- ✅ Estadísticas descriptivas
- ✅ Análisis de valores nulos
- ✅ Detección de outliers
- ✅ Distribuciones de variables
- ✅ Correlaciones entre características
- ✅ Visualizaciones temporales del consumo
- ✅ Análisis por hora, día, mes

**Cuándo usar**: 
- Antes de entrenar cualquier modelo
- Para entender patrones en tus datos
- Para identificar problemas de calidad de datos
- Para decidir qué características incluir en los modelos

**Prerequisitos**:
- Dataset en `../../data/raw/datos_retail_para_modelos.csv`

**Tiempo estimado**: 15-30 minutos

---

### 2. 02_Clustering.ipynb - Análisis de Patrones con K-Means

**Propósito**: Identificar patrones de consumo usando clustering

**Contenido**:
- ✅ Preprocesamiento de datos para clustering
- ✅ Método del codo para seleccionar K óptimo
- ✅ Entrenamiento de modelo K-Means
- ✅ Visualización de clusters con PCA
- ✅ Análisis de características de cada cluster
- ✅ Interpretación de patrones encontrados

**Cuándo usar**:
- Para segmentar diferentes tipos de consumo
- Para identificar anomalías
- Para entender comportamientos de consumo
- Para crear estrategias diferenciadas por patrón

**Prerequisitos**:
- Dataset en `../../data/raw/datos_retail_para_modelos.csv`
- Haber ejecutado 01_EDA.ipynb (recomendado)

**Tiempo estimado**: 20-30 minutos

**Resultados esperados**:
- 3 clusters principales (bajo, medio, alto consumo)
- Gráficos de visualización
- Estadísticas por cluster

---

### 3. 03_Forecasting.ipynb - Predicción de Consumo Energético

**Propósito**: Entrenar y evaluar modelos de predicción

**Contenido**:
- ✅ Feature engineering (creación de características)
- ✅ Preparación de datos de entrenamiento/prueba
- ✅ Entrenamiento de múltiples modelos:
  - Random Forest
  - Gradient Boosting
  - XGBoost
- ✅ Evaluación con métricas (MAE, RMSE, R², MAPE)
- ✅ Comparación de modelos
- ✅ Visualización de predicciones
- ✅ Análisis de importancia de características
- ✅ Optimización de hiperparámetros (opcional)

**Cuándo usar**:
- Para entrenar modelos de predicción
- Para comparar diferentes algoritmos
- Para optimizar hiperparámetros
- Para evaluar el rendimiento del modelo

**Prerequisitos**:
- Dataset en `../../data/raw/datos_retail_para_modelos.csv`
- Haber ejecutado 01_EDA.ipynb y 02_Clustering.ipynb (recomendado)

**Tiempo estimado**: 30-60 minutos

**Resultados esperados**:
- Modelo con R² > 0.85
- MAE < 50 kWh
- MAPE < 10%
- Gráficos de predicciones vs valores reales

---

## 🚀 Cómo Usar los Notebooks

### Opción 1: Jupyter Notebook (Clásico)

```bash
# Instalar dependencias
cd ml
pip install -r requirements.txt

# Iniciar Jupyter
cd notebooks
jupyter notebook

# Abrir el notebook deseado en el navegador
```

### Opción 2: JupyterLab (Recomendado)

```bash
# Instalar JupyterLab
pip install jupyterlab

# Iniciar JupyterLab
cd ml/notebooks
jupyter lab
```

### Opción 3: VS Code

```bash
# Instalar extensión de Jupyter en VS Code
# Abrir el archivo .ipynb directamente en VS Code
```

## 📋 Orden Recomendado de Ejecución

Para un análisis completo, sigue este orden:

1. **01_EDA.ipynb** → Entender los datos
2. **02_Clustering.ipynb** → Identificar patrones
3. **03_Forecasting.ipynb** → Entrenar modelos de predicción

## 🔧 Prerequisitos

### 1. Dataset

Asegúrate de tener el dataset en la ubicación correcta:

```bash
# Verificar
ls -lh ../../data/raw/datos_retail_para_modelos.csv

# Si no existe, copia tu archivo
cp /ruta/a/tu/datos_retail_para_modelos.csv ../../data/raw/
```

### 2. Dependencias Python

```bash
cd ../
pip install -r requirements.txt
```

Dependencias principales:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- xgboost
- jupyter

### 3. Kernels de Jupyter

```bash
# Crear un kernel con el entorno virtual (opcional)
python -m ipykernel install --user --name=megaplaza-ml
```

## 💡 Tips y Mejores Prácticas

### 1. Ejecutar Celdas Secuencialmente

- Siempre ejecuta las celdas en orden (de arriba a abajo)
- No saltes celdas importantes de configuración
- Si algo falla, reinicia el kernel: `Kernel → Restart & Clear Output`

### 2. Modificar y Experimentar

- Los notebooks están diseñados para ser modificados
- Haz copias antes de experimentar mucho
- Documenta tus cambios en las celdas de markdown

### 3. Guardar Resultados

```python
# Ejemplo: Guardar gráfico
fig.savefig('../../data/processed/mi_grafico.png', dpi=300, bbox_inches='tight')

# Ejemplo: Guardar modelo
import joblib
joblib.dump(model, '../models/mi_modelo_experimental.pkl')
```

### 4. Trabajar con Datos Grandes

Si tu dataset es muy grande (>100k registros):

```python
# Trabajar con una muestra primero
df_sample = df.sample(n=10000, random_state=42)

# Cuando estés seguro, usar el dataset completo
# df_full = df.copy()
```

### 5. Debugging

```python
# Ver información del DataFrame
df.info()
df.describe()
df.head()

# Ver tipos de datos
print(df.dtypes)

# Ver valores únicos
print(df['columna'].unique())

# Ver valores nulos
print(df.isnull().sum())
```

## 📊 Personalización

### Agregar Nuevas Visualizaciones

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Personalizar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Crear gráfico
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['fecha'], df['consumo_energia'])
ax.set_title('Mi Gráfico Personalizado')
plt.show()
```

### Probar Nuevos Modelos

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge

# Modelo alternativo
model_gb = GradientBoostingRegressor(n_estimators=200)
model_gb.fit(X_train, y_train)

# Evaluar
from evaluation import calculate_metrics
metrics = calculate_metrics(y_test, model_gb.predict(X_test))
print(metrics)
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
# Instalar módulo faltante
pip install nombre_del_modulo

# O reinstalar todas las dependencias
cd .. && pip install -r requirements.txt
```

### Error: "FileNotFoundError" al cargar datos

```bash
# Verificar que el dataset existe
ls ../../data/raw/datos_retail_para_modelos.csv

# Verificar la ruta relativa
pwd  # Debes estar en ml/notebooks/
```

### Kernel se Desconecta

- Dataset muy grande → usar una muestra
- Poco RAM → cerrar otros programas
- Cálculos muy pesados → reducir parámetros del modelo

### Gráficos no se Muestran

```python
# Agregar al inicio del notebook
%matplotlib inline

# O usar
import matplotlib.pyplot as plt
plt.show()
```

## 📁 Estructura de Archivos Generados

Después de ejecutar los notebooks, podrías tener:

```
notebooks/
├── 01_EDA.ipynb
├── 02_Clustering.ipynb
├── 03_Forecasting.ipynb
├── README.md (este archivo)
└── .ipynb_checkpoints/     # Backups automáticos (git-ignored)
```

Los resultados principales (modelos, gráficos) se guardan en:
- `../models/` - Modelos entrenados
- `../../data/processed/` - Datos procesados

## 🔗 Recursos Adicionales

- **Documentación de entrenamiento**: [../../docs/ENTRENAMIENTO.md](../../docs/ENTRENAMIENTO.md)
- **Guía de uso post-entrenamiento**: [../../docs/USO_POST_ENTRENAMIENTO.md](../../docs/USO_POST_ENTRENAMIENTO.md)
- **README del módulo ML**: [../README.md](../README.md)
- **Script de entrenamiento**: [../src/train_models.py](../src/train_models.py)

## ✅ Checklist Antes de Empezar

- [ ] Dataset colocado en `../../data/raw/datos_retail_para_modelos.csv`
- [ ] Dependencias instaladas (`pip install -r ../requirements.txt`)
- [ ] Jupyter funcionando (`jupyter notebook` o `jupyter lab`)
- [ ] Has leído [../../docs/INICIO_RAPIDO.md](../../docs/INICIO_RAPIDO.md)

---

## 🎓 Próximos Pasos

Después de trabajar con los notebooks:

1. **Entrenar modelos finales**: Usa `../src/train_models.py`
2. **Implementar en producción**: Ver [../../docs/USO_POST_ENTRENAMIENTO.md](../../docs/USO_POST_ENTRENAMIENTO.md)
3. **Integrar con la API**: Los modelos se cargan automáticamente
4. **Configurar reentrenamiento**: Periódico para mantener precisión

---

**¿Preguntas?** Consulta la documentación o abre un issue en GitHub.

---

**Última actualización**: 2024
**Versión**: 1.0
