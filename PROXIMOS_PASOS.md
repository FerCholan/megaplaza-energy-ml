# 📋 Próximos Pasos - Qué Hacer Ahora

Este documento te guía en los pasos exactos a seguir después de que se completaron los cambios en el repositorio.

## ✅ Estado Actual

El repositorio ha sido actualizado con:
- ✅ Estructura de directorios para datos
- ✅ Scripts de entrenamiento completos
- ✅ Documentación exhaustiva en español
- ✅ Notebooks actualizados
- ✅ Guías de uso detalladas

## 🎯 Lo Que Debes Hacer Ahora

### Paso 1: Actualizar Tu Repositorio Local (2 minutos)

```bash
# Ir a tu directorio del proyecto
cd /ruta/a/megaplaza-energy-ml

# Actualizar desde GitHub
git fetch origin
git checkout copilot/usar-dataset-para-modelos
git pull origin copilot/usar-dataset-para-modelos

# Verificar que tienes todos los archivos nuevos
ls -la data/
ls -la docs/
ls -la ml/src/
```

**Verifica que veas**:
- `data/README.md`
- `docs/ENTRENAMIENTO.md`
- `docs/USO_POST_ENTRENAMIENTO.md`
- `docs/INICIO_RAPIDO.md`
- `ml/src/train_models.py`
- `ml/src/ejemplo_prediccion.py`

### Paso 2: Preparar Tu Dataset (5 minutos)

```bash
# Crear directorios si no existen
mkdir -p data/raw

# Copiar tu dataset
# IMPORTANTE: Ajusta la ruta a donde está tu archivo
cp /ruta/a/tu/datos_retail_para_modelos.csv data/raw/

# Verificar que el archivo existe
ls -lh data/raw/datos_retail_para_modelos.csv

# Ver las primeras líneas para confirmar
head -n 3 data/raw/datos_retail_para_modelos.csv
```

**Deberías ver algo como:**
```csv
consumo_energia,pies_cuadrados,ano_construccion,temperatura_aire,cobertura_nubes,presion_nivel_mar,velocidad_viento,mes,dia_del_ano,dia_de_la_semana,hora_del_dia,es_fin_de_semana,medidor_electricidad,medidor_agua_fria
0.0,59071,1980.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
53.2397,9045,2016.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
```

### Paso 3: Instalar Dependencias (5-10 minutos)

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias de ML
cd ml
pip install -r requirements.txt

# Volver a la raíz
cd ..
```

**Espera a que termine la instalación.** Verás la instalación de pandas, scikit-learn, xgboost, etc.

### Paso 4: Leer la Documentación (10-15 minutos)

**IMPORTANTE**: Antes de entrenar, lee al menos uno de estos documentos:

**Opción Rápida (10 min)**:
```bash
# Ver en tu editor o navegador
cat docs/INICIO_RAPIDO.md
# o abrirlo en VS Code, editor de texto, etc.
```

**Opción Completa (30 min)**:
```bash
# Leer en orden:
cat docs/INICIO_RAPIDO.md
cat docs/ENTRENAMIENTO.md
cat docs/USO_POST_ENTRENAMIENTO.md
```

**O simplemente abre estos archivos en tu navegador/editor favorito.**

### Paso 5: Entrenar los Modelos (10-20 minutos)

```bash
# Activar entorno virtual si no lo hiciste
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Ir al directorio de scripts
cd ml/src

# Entrenar modelos
python train_models.py
```

**Qué esperar:**
- El script tardará 10-20 minutos dependiendo del tamaño de tu dataset
- Verás progreso en la consola
- Al final, verás métricas como R², MAE, RMSE
- Se crearán 5 archivos en `ml/models/`

**Ejemplo de salida exitosa:**
```
========================================
ENTRENAMIENTO COMPLETADO
========================================

✓ Todos los modelos han sido entrenados y guardados
✓ Los modelos están listos para ser usados en la API

Archivos generados:
  - ml/models/forecasting_model.pkl
  - ml/models/feature_columns.pkl
  - ml/models/clustering_model.pkl
  - ml/models/clustering_scaler.pkl
  - ml/models/clustering_columns.pkl
```

### Paso 6: Verificar la Instalación (2 minutos)

```bash
# Desde ml/src
python ejemplo_prediccion.py
```

**Deberías ver:**
- ✓ Todos los modelos cargados
- 🔮 Predicciones de ejemplo
- 📊 Análisis de clusters
- 📅 Predicciones para diferentes horas

**Si ves esto, ¡todo funciona correctamente!** 🎉

### Paso 7: Elegir Cómo Usar los Modelos (variable)

Ahora tienes 4 opciones. Elige según tu caso:

#### Opción A: Solo Quiero Explorar (Notebooks)

```bash
cd ml/notebooks
jupyter notebook
# Abre: 01_EDA.ipynb
```

**Mejor para**: Análisis exploratorio, experimentación

#### Opción B: Quiero una Interfaz Visual (Dashboard)

```bash
# Desde la raíz
docker-compose up -d
# Abre: http://localhost:8501
```

**Mejor para**: Visualización, demostraciones, usuarios no técnicos

#### Opción C: Quiero una API (Backend)

```bash
# Desde la raíz
docker-compose up -d backend
# API: http://localhost:8000/docs
```

**Mejor para**: Integración con otras aplicaciones, automatización

#### Opción D: Quiero Integrar en Mi Código

Lee: `docs/USO_POST_ENTRENAMIENTO.md` - Opción 4

**Mejor para**: Aplicaciones personalizadas, scripts

## 📊 Resumen Visual del Flujo

```
┌─────────────────────────────────────────────────┐
│  1. Actualizar Repositorio (git pull)          │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  2. Colocar Dataset en data/raw/               │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  3. Instalar Dependencias (pip install)        │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  4. Leer Documentación (docs/)                 │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  5. Entrenar Modelos (train_models.py)         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  6. Verificar (ejemplo_prediccion.py)          │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  7. Elegir Método de Uso:                      │
│     • Notebooks (exploración)                   │
│     • Dashboard (visual)                        │
│     • API (integración)                         │
│     • Código (personalizado)                    │
└─────────────────────────────────────────────────┘
```

## 📚 Documentos de Referencia Rápida

| Documento | Cuándo Leerlo | Tiempo |
|-----------|---------------|--------|
| `GUIA_RAPIDA.md` | Ahora (referencia rápida) | 2 min |
| `docs/INICIO_RAPIDO.md` | Antes de empezar | 10 min |
| `docs/ENTRENAMIENTO.md` | Antes de entrenar | 15 min |
| `docs/USO_POST_ENTRENAMIENTO.md` | Después de entrenar | 20 min |
| `ml/README.md` | Para entender el código | 10 min |
| `data/README.md` | Si tienes dudas del dataset | 5 min |

## ✅ Checklist de Progreso

Marca cada paso conforme lo completes:

**Setup Inicial:**
- [ ] Repositorio actualizado (`git pull`)
- [ ] Dataset copiado a `data/raw/`
- [ ] Dependencias instaladas
- [ ] Documentación leída (al menos INICIO_RAPIDO.md)

**Entrenamiento:**
- [ ] Script `train_models.py` ejecutado
- [ ] 5 archivos generados en `ml/models/`
- [ ] R² > 0.70 en el reporte
- [ ] Script `ejemplo_prediccion.py` funciona

**Uso:**
- [ ] Elegiste método de uso (Notebooks/Dashboard/API/Código)
- [ ] Probaste hacer una predicción
- [ ] Entiendes cómo usar los modelos

**Producción (opcional):**
- [ ] Configuraste reentrenamiento periódico
- [ ] Implementaste monitoreo
- [ ] Documentaste tu implementación

## 🆘 Si Algo Sale Mal

### Problema: Git pull falla

```bash
# Opción 1: Stash tus cambios
git stash
git pull origin copilot/usar-dataset-para-modelos

# Opción 2: Clone fresco
cd ..
git clone https://github.com/FerCholan/megaplaza-energy-ml.git megaplaza-energy-ml-new
cd megaplaza-energy-ml-new
```

### Problema: No encuentras el dataset

El sistema espera: `data/raw/datos_retail_para_modelos.csv`

Verifica:
1. Nombre exacto del archivo
2. Ubicación correcta
3. Formato CSV válido

### Problema: Entrenamiento falla

1. Verifica que el dataset tenga todas las columnas
2. Lee los mensajes de error
3. Consulta `docs/ENTRENAMIENTO.md` - Sección "Solución de Problemas"

### Problema: Modelos dan bajo R²

1. Verifica calidad de datos (notebook 01_EDA.ipynb)
2. Asegúrate de tener suficientes datos (>1000 registros)
3. Consulta documentación sobre optimización

## 💡 Tips Finales

1. **No te saltes la documentación**: Está en español y muy detallada
2. **Empieza con notebooks**: Es la forma más fácil de familiarizarte
3. **Reentrena periódicamente**: Los datos cambian con el tiempo
4. **Guarda versiones**: Haz backup de modelos que funcionen bien
5. **Monitorea rendimiento**: El R² puede bajar con el tiempo

## 🎯 Meta Final

Al completar todos estos pasos, deberías tener:
- ✅ Sistema completamente funcional
- ✅ Modelos entrenados con tu dataset
- ✅ Capacidad de hacer predicciones
- ✅ Entendimiento de cómo mantener el sistema

## 📞 Contacto y Soporte

- **Issues de GitHub**: https://github.com/FerCholan/megaplaza-energy-ml/issues
- **Documentación**: Directorio `docs/`
- **Ejemplos**: Directorio `ml/notebooks/`

---

## 🎓 ¿Qué Sigue Después de Todo Esto?

Una vez que tengas todo funcionando:

1. **Integra en producción** (ver `docs/USO_POST_ENTRENAMIENTO.md`)
2. **Configura monitoreo** de rendimiento del modelo
3. **Establece calendario de reentrenamiento**
4. **Documenta tu implementación** específica
5. **Capacita a tu equipo** en el uso del sistema

---

**¡Mucho éxito con tu proyecto de optimización energética!** 🎉

Si tienes preguntas, consulta la documentación o abre un issue.

---

**Fecha**: 2024  
**Versión**: 1.0
