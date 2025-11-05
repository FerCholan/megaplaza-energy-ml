# ⚡ Sistema de Optimización Energética - Mega Plaza Chimbote

Sistema completo de predicción y optimización de consumo energético usando Machine Learning para Mega Plaza Chimbote.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descripción

Este proyecto implementa un sistema integral para:
- **Predicción** de consumo energético usando modelos de Machine Learning
- **Clustering** de patrones de consumo para identificar comportamientos
- **Alertas** en tiempo real para consumos anómalos
- **Dashboard interactivo** para visualización y análisis
- **API REST** completa para integración con otros sistemas

## 🎯 Características

### Backend (FastAPI)
- ✅ API REST completa con autenticación JWT
- ✅ Gestión de usuarios y roles
- ✅ Endpoints para consumo, predicciones y alertas
- ✅ Integración con PostgreSQL y Redis
- ✅ Sistema de alertas automáticas
- ✅ Documentación automática con Swagger

### Machine Learning
- ✅ Análisis exploratorio de datos (EDA)
- ✅ Clustering con K-Means (3 clusters)
- ✅ Predicción con XGBoost (R² > 0.87)
- ✅ Feature engineering avanzado
- ✅ Evaluación y métricas de rendimiento

### Frontend (Streamlit)
- ✅ Dashboard interactivo en tiempo real
- ✅ Visualizaciones con Plotly
- ✅ Análisis estadísticos detallados
- ✅ Gestión de alertas y configuración
- ✅ Predicción interactiva

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendada)

```bash
# Clonar repositorio
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml

# Configurar variables de entorno
cp .env.example .env

# Iniciar con Docker Compose
docker-compose up -d
```

Acceder a:
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **Docs API**: http://localhost:8000/docs

### Opción 2: Instalación Manual

Ver guía completa en [docs/SETUP.md](docs/SETUP.md)

## 📊 Dataset

El sistema utiliza un dataset con ~113,000 registros que incluye:
- Consumo energético (kWh)
- Variables ambientales (temperatura, viento, nubes, presión)
- Variables temporales (hora, día, mes)
- Características del edificio (área, medidores)

## 🏗️ Arquitectura

```
megaplaza-energy-ml/
├── backend/               # API FastAPI
│   ├── app/
│   │   ├── models/       # Modelos de base de datos
│   │   ├── schemas/      # Esquemas Pydantic
│   │   ├── routes/       # Endpoints de la API
│   │   ├── services/     # Lógica de negocio
│   │   └── utils/        # Utilidades
│   └── Dockerfile
├── frontend/             # Dashboard Streamlit
│   ├── pages/           # Páginas del dashboard
│   ├── components/      # Componentes reutilizables
│   ├── utils/           # Utilidades
│   └── Dockerfile
├── ml/                   # Machine Learning
│   ├── notebooks/       # Jupyter notebooks
│   │   ├── 01_EDA.ipynb
│   │   ├── 02_Clustering.ipynb
│   │   └── 03_Forecasting.ipynb
│   ├── src/             # Scripts de ML
│   │   ├── preprocessing.py
│   │   ├── clustering.py
│   │   ├── forecasting.py
│   │   └── evaluation.py
│   └── models/          # Modelos entrenados
├── data/                 # Datos
│   └── raw/
│       └── energy_consumption.csv
├── tests/                # Tests
├── docs/                 # Documentación
└── docker-compose.yml
```

## 🔧 Tecnologías

**Backend:**
- FastAPI 0.104
- SQLAlchemy 2.0
- PostgreSQL 15
- Redis 7
- JWT Authentication

**Machine Learning:**
- Pandas & NumPy
- Scikit-learn 1.3
- XGBoost 2.0
- Matplotlib & Seaborn

**Frontend:**
- Streamlit 1.29
- Plotly 5.18
- Requests

**DevOps:**
- Docker & Docker Compose
- GitHub Actions
- pytest

## 📖 Documentación

- [Guía de Instalación](docs/SETUP.md)
- [Documentación de la API](docs/API.md)
- [API Interactiva](http://localhost:8000/docs) (después de iniciar)

## 🧪 Tests

```bash
# Instalar dependencias de test
pip install pytest

# Ejecutar tests
pytest tests/

# Con cobertura
pytest tests/ --cov=backend/app --cov=ml/src
```

## 📈 Resultados del Modelo

### Modelo de Predicción (XGBoost)
- **R² Score**: 0.8756
- **MAE**: 42.5 kWh
- **RMSE**: 58.3 kWh
- **MAPE**: 5.8%

### Clustering (K-Means)
- **Número de Clusters**: 3
- **Cluster 0**: Consumo bajo (horarios nocturnos)
- **Cluster 1**: Consumo medio (horarios normales)
- **Cluster 2**: Consumo alto (horarios pico)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

## 👥 Autores

- **Fernando Cholan** - [FerCholan](https://github.com/FerCholan)

## 🙏 Agradecimientos

- Mega Plaza Chimbote por proporcionar el contexto del proyecto
- Comunidad de FastAPI y Streamlit
- Contribuidores de Scikit-learn y XGBoost

## 📧 Contacto

Para preguntas o soporte, por favor abre un issue en GitHub.

---

⭐ Si este proyecto te fue útil, considera darle una estrella!
