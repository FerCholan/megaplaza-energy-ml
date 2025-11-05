# 🚀 Guía de Inicio Rápido

Esta guía te llevará desde cero hasta tener el sistema completamente funcional con tu dataset `datos_retail_para_modelos.csv`.

## ⏱️ Tiempo Estimado

- **Primera vez**: 30-45 minutos
- **Entrenamiento**: 5-15 minutos (depende del tamaño del dataset)
- **Con experiencia**: 10-15 minutos

---

## 📋 Requisitos Previos

### 1. Software Necesario

```bash
# Verificar instalaciones
python --version    # Debe ser Python 3.8+
docker --version    # Opcional pero recomendado
git --version
```

Si no tienes Docker, puedes instalar sin él (ver [Instalación Manual](#instalación-manual)).

### 2. Tu Dataset

Necesitas el archivo `datos_retail_para_modelos.csv` con esta estructura:

```csv
consumo_energia,pies_cuadrados,ano_construccion,temperatura_aire,cobertura_nubes,presion_nivel_mar,velocidad_viento,mes,dia_del_ano,dia_de_la_semana,hora_del_dia,es_fin_de_semana,medidor_electricidad,medidor_agua_fria
0.0,59071,1980.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
53.2397,9045,2016.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
```

---

## 🎯 Pasos del 1 al 5

### Paso 1: Clonar el Repositorio

```bash
# Clonar
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml

# Verificar estructura
ls -la
```

### Paso 2: Preparar el Dataset

```bash
# Crear directorio de datos
mkdir -p data/raw data/processed

# Copiar tu dataset (ajusta la ruta según donde esté tu archivo)
cp /ruta/a/tu/datos_retail_para_modelos.csv data/raw/

# Verificar
ls -lh data/raw/datos_retail_para_modelos.csv
head -n 3 data/raw/datos_retail_para_modelos.csv
```

**¿No tienes el archivo?** Revisa la sección "Formato del Dataset" en [data/README.md](../data/README.md).

### Paso 3: Instalar Dependencias

**Opción A: Solo para entrenamiento (más rápido)**

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de ML
cd ml
pip install -r requirements.txt
cd ..
```

**Opción B: Sistema completo con Docker**

```bash
# Configurar variables de entorno
cp .env.example .env

# Editar .env si es necesario
nano .env
```

### Paso 4: Entrenar los Modelos ⭐

```bash
# Activar entorno virtual (si no lo hiciste antes)
source venv/bin/activate

# Entrenar
cd ml/src
python train_models.py
```

**Salida esperada:**

```
========================================
SISTEMA DE ENTRENAMIENTO DE MODELOS ML
Mega Plaza Chimbote - Optimización Energética
========================================

📂 Cargando datos desde: datos_retail_para_modelos.csv
✓ Dataset cargado: 112483 registros, 14 columnas

🧹 Limpiando datos...
✓ Datos limpios: 110234 registros

============================================================
ENTRENANDO MODELO DE PREDICCIÓN DE CONSUMO
============================================================

1. Preparando datos para entrenamiento...
   - Tamaño conjunto entrenamiento: 88187 muestras
   - Tamaño conjunto prueba: 22047 muestras

2. Entrenando modelo XGBoost...
   ✓ Modelo entrenado exitosamente

3. Evaluando modelo en conjunto de prueba...

========================================
REPORTE DE EVALUACIÓN - XGBoost
========================================

Métricas de Error:
------------------
MAE (Error Absoluto Medio):       XX.XX kWh
RMSE (Raíz del ECM):              XX.XX kWh
MAPE (Error Porcentual Abs Med):  X.XX%

Métrica de Ajuste:
------------------
R² (Coeficiente de Determinación): 0.XXXX

✓ Excelente ajuste del modelo
========================================

✓ Modelo guardado en: ../models/forecasting_model.pkl

============================================================
ENTRENANDO MODELO DE CLUSTERING
============================================================
...

✅ ENTRENAMIENTO COMPLETADO
```

**⏱️ Tiempo de espera**: 5-15 minutos dependiendo de:
- Tamaño del dataset
- Velocidad de tu computadora
- Si tienes GPU (más rápido)

### Paso 5: Verificar Modelos Generados

```bash
# Desde ml/src
cd ..
ls -lh models/

# Deberías ver:
# forecasting_model.pkl
# feature_columns.pkl
# clustering_model.pkl
# clustering_scaler.pkl
# clustering_columns.pkl
```

---

## ✅ ¡Listo! ¿Qué Sigue?

Ahora tienes los modelos entrenados. Tienes 3 opciones:

### Opción 1: Usar en Notebooks (Más Fácil)

```bash
# Desde la raíz
cd ml/notebooks
jupyter notebook
```

Abre `03_Forecasting.ipynb` y ejecuta las celdas para hacer predicciones.

### Opción 2: Usar la API REST

```bash
# Desde la raíz
docker-compose up -d backend

# Probar
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
    "hora_del_dia": 14,
    "es_fin_de_semana": 0
  }'
```

Ver documentación completa en [USO_POST_ENTRENAMIENTO.md](USO_POST_ENTRENAMIENTO.md#opción-1-usar-la-api-rest).

### Opción 3: Usar el Dashboard

```bash
docker-compose up -d

# Abrir navegador en:
# http://localhost:8501 - Dashboard
# http://localhost:8000/docs - API docs
```

---

## 🔧 Instalación Manual (Sin Docker)

Si no tienes Docker, puedes instalar todo manualmente.

### Backend (API)

```bash
# Instalar PostgreSQL y Redis
# Ubuntu/Debian:
sudo apt-get install postgresql redis-server

# macOS:
brew install postgresql redis

# Crear base de datos
createdb megaplaza_energy

# Instalar dependencias Python
cd backend
pip install -r requirements.txt

# Configurar variables de entorno
cp ../.env.example ../.env
nano ../.env  # Ajustar DATABASE_URL, etc.

# Iniciar API
uvicorn app.main:app --reload
```

### Frontend (Dashboard)

```bash
cd frontend
pip install -r requirements.txt

# Iniciar dashboard
streamlit run app.py
```

---

## 🐛 Solución de Problemas Comunes

### Error: "No se encontró el archivo de datos"

```bash
# Verificar ruta
ls data/raw/datos_retail_para_modelos.csv

# Si no existe
mkdir -p data/raw
cp /tu/ruta/datos_retail_para_modelos.csv data/raw/
```

### Error: "ModuleNotFoundError"

```bash
# Reinstalar dependencias
pip install -r ml/requirements.txt

# Si persiste, actualizar pip
pip install --upgrade pip
```

### Error: "KeyError: columna_nombre"

Tu CSV no tiene todas las columnas requeridas. Verifica con:

```python
import pandas as pd
df = pd.read_csv('data/raw/datos_retail_para_modelos.csv')
print(df.columns.tolist())
```

Columnas requeridas: `consumo_energia`, `pies_cuadrados`, `ano_construccion`, `temperatura_aire`, `cobertura_nubes`, `presion_nivel_mar`, `velocidad_viento`, `mes`, `dia_del_ano`, `dia_de_la_semana`, `hora_del_dia`, `es_fin_de_semana`, `medidor_electricidad`, `medidor_agua_fria`

### Error: Modelo con bajo R² (<0.5)

Posibles causas:
1. **Dataset muy pequeño**: Necesitas al menos 1000 registros
2. **Muchos valores nulos**: Limpia tus datos primero
3. **Datos no representativos**: Verifica que los datos sean correctos

Soluciones:
```bash
# Ver estadísticas del dataset
cd ml/notebooks
jupyter notebook 01_EDA.ipynb
# Ejecuta el notebook para analizar tu dataset
```

### Error: Docker no inicia

```bash
# Verificar Docker
docker ps

# Ver logs
docker-compose logs backend
docker-compose logs frontend

# Reiniciar
docker-compose down
docker-compose up -d
```

---

## 📚 Siguientes Pasos Recomendados

1. **Explora tus datos** en `ml/notebooks/01_EDA.ipynb`
2. **Analiza los clusters** en `ml/notebooks/02_Clustering.ipynb`
3. **Haz predicciones** en `ml/notebooks/03_Forecasting.ipynb`
4. **Lee la documentación completa**: [USO_POST_ENTRENAMIENTO.md](USO_POST_ENTRENAMIENTO.md)
5. **Configura reentrenamiento periódico** (ver documentación)

---

## 📞 ¿Necesitas Ayuda?

- 📖 **Documentación completa**: Revisa `docs/`
- 🐛 **Issues**: Abre un issue en GitHub
- 💬 **Preguntas**: Consulta [FAQ.md](FAQ.md) (si existe)

---

## ✅ Checklist de Verificación

Antes de considerar que está todo listo:

- [ ] Dataset copiado a `data/raw/datos_retail_para_modelos.csv`
- [ ] Script de entrenamiento ejecutado sin errores
- [ ] 5 archivos de modelos generados en `ml/models/`
- [ ] R² del modelo > 0.7 (idealmente > 0.85)
- [ ] Probaste hacer una predicción simple
- [ ] Leíste [USO_POST_ENTRENAMIENTO.md](USO_POST_ENTRENAMIENTO.md)

---

## 🎓 Resumen de Comandos Clave

```bash
# Setup inicial
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml
mkdir -p data/raw
cp /ruta/datos_retail_para_modelos.csv data/raw/

# Entrenar modelos
python -m venv venv
source venv/bin/activate
cd ml && pip install -r requirements.txt
cd src && python train_models.py

# Usar con Docker (opcional)
docker-compose up -d

# Usar sin Docker
cd backend && uvicorn app.main:app --reload  # Terminal 1
cd frontend && streamlit run app.py          # Terminal 2
```

---

**¡Éxito con tu proyecto de optimización energética!** 🎉

---

**Última actualización**: 2024
**Versión**: 1.0
