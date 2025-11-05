# 🚀 Guía Rápida de Uso

> **¿Primera vez?** Lee primero [docs/INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)

## ⚡ Comandos Esenciales

### Configuración Inicial (Una sola vez)

```bash
# 1. Clonar repositorio
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml

# 2. Colocar dataset
mkdir -p data/raw
cp /ruta/a/tu/datos_retail_para_modelos.csv data/raw/

# 3. Instalar dependencias
cd ml
pip install -r requirements.txt
```

### Entrenar Modelos

```bash
# Desde ml/
cd src
python train_models.py

# Verificar
python ejemplo_prediccion.py
```

### Usar los Modelos

#### Opción 1: Dashboard (Visual)
```bash
# Desde raíz
docker-compose up -d
# Abrir: http://localhost:8501
```

#### Opción 2: API REST
```bash
# Desde raíz
docker-compose up -d backend
# API: http://localhost:8000/docs
```

#### Opción 3: Notebooks
```bash
# Desde ml/notebooks
jupyter notebook
# Abrir 01_EDA.ipynb, 02_Clustering.ipynb, 03_Forecasting.ipynb
```

#### Opción 4: Python
```python
import joblib
model = joblib.load('ml/models/forecasting_model.pkl')
consumo = model.predict(datos)
```

## 📚 Documentación por Caso de Uso

| Si quieres... | Lee esto |
|---------------|----------|
| 🆕 **Empezar desde cero** | [docs/INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md) |
| 🎓 **Entrenar modelos** | [docs/ENTRENAMIENTO.md](docs/ENTRENAMIENTO.md) |
| 🚀 **Usar modelos entrenados** | [docs/USO_POST_ENTRENAMIENTO.md](docs/USO_POST_ENTRENAMIENTO.md) |
| 📊 **Explorar datos** | [ml/notebooks/README.md](ml/notebooks/README.md) |
| 🔧 **Entender código ML** | [ml/README.md](ml/README.md) |
| 📝 **Ver resumen de cambios** | [docs/RESUMEN_CAMBIOS.md](docs/RESUMEN_CAMBIOS.md) |

## 🔍 Estructura del Dataset

```csv
consumo_energia,pies_cuadrados,ano_construccion,temperatura_aire,cobertura_nubes,presion_nivel_mar,velocidad_viento,mes,dia_del_ano,dia_de_la_semana,hora_del_dia,es_fin_de_semana,medidor_electricidad,medidor_agua_fria
0.0,59071,1980.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
53.2397,9045,2016.0,25.0,6.0,1019.7,0.0,1,1,4,0,0,True,False
```

**Ubicación**: `data/raw/datos_retail_para_modelos.csv`  
**Detalles**: Ver [data/README.md](data/README.md)

## 📁 Archivos Importantes

```
📂 megaplaza-energy-ml/
├── 📄 GUIA_RAPIDA.md (este archivo)
├── 📂 data/
│   ├── 📄 README.md (estructura del dataset)
│   └── 📂 raw/
│       └── 📄 datos_retail_para_modelos.csv (TU DATASET AQUÍ)
├── 📂 docs/
│   ├── 📄 INICIO_RAPIDO.md ⭐
│   ├── 📄 ENTRENAMIENTO.md ⭐
│   └── 📄 USO_POST_ENTRENAMIENTO.md ⭐
├── 📂 ml/
│   ├── 📄 README.md
│   ├── 📂 src/
│   │   ├── 📄 train_models.py ⭐ (entrenar)
│   │   └── 📄 ejemplo_prediccion.py ⭐ (verificar)
│   ├── 📂 notebooks/ (análisis interactivo)
│   └── 📂 models/ (modelos entrenados - se generan)
└── 📂 backend/ (API REST)
```

## 🎯 Checklist Rápido

**Antes de entrenar:**
- [ ] Dataset en `data/raw/datos_retail_para_modelos.csv`
- [ ] Dependencias instaladas (`pip install -r ml/requirements.txt`)
- [ ] Has leído [docs/INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)

**Después de entrenar:**
- [ ] 5 archivos en `ml/models/` (forecasting_model.pkl, etc.)
- [ ] R² > 0.70 en el reporte de entrenamiento
- [ ] Script de ejemplo funciona (`python ejemplo_prediccion.py`)

**Para usar:**
- [ ] Elegiste método (API, Dashboard, Notebooks, o Código)
- [ ] Leíste [docs/USO_POST_ENTRENAMIENTO.md](docs/USO_POST_ENTRENAMIENTO.md)

## 🆘 Ayuda Rápida

| Problema | Solución |
|----------|----------|
| ❌ "File not found" | Verifica que el dataset esté en `data/raw/` |
| ❌ "Module not found" | Ejecuta `pip install -r ml/requirements.txt` |
| ❌ Bajo R² (<0.5) | Revisa calidad de datos en notebook 01_EDA.ipynb |
| ❌ Docker no funciona | Usa instalación manual (ver docs/INICIO_RAPIDO.md) |
| ❌ Modelo no carga | Re-entrena con `python train_models.py` |

## 💡 Tips Rápidos

- 📊 **Explora primero**: Usa notebooks antes de entrenar en producción
- 🔄 **Reentrena periódicamente**: Mensual o cuando tengas datos nuevos
- 📈 **Monitorea R²**: Si baja de 0.70, considera reentrenar
- 💾 **Guarda versiones**: Haz backup de modelos antes de reentrenar
- 📚 **Lee la docs**: Está toda en español y muy detallada

## 🔗 Enlaces Útiles

- **GitHub**: https://github.com/FerCholan/megaplaza-energy-ml
- **Documentación completa**: [docs/](docs/)
- **Issues**: https://github.com/FerCholan/megaplaza-energy-ml/issues

## 📞 Soporte

1. Revisa la documentación en `docs/`
2. Busca en los README de cada directorio
3. Abre un issue en GitHub
4. Consulta los notebooks de ejemplo

---

**Versión**: 1.0  
**Última actualización**: 2024

🎉 **¡Éxito con tu proyecto de optimización energética!**
