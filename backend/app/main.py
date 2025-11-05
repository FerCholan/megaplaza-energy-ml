"""
Aplicación principal FastAPI
Sistema de Optimización Energética para Mega Plaza Chimbote
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from .config import settings
from .database import init_db
from .routes import auth, consumption, prediction, alerts, ml
from .services.ml_service import ml_service

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    Inicializa recursos al inicio y los libera al cierre
    """
    # Startup
    logger.info("Iniciando aplicación...")

    # Inicializar base de datos (crear tablas si no existen)
    try:
        init_db()
        logger.info("Base de datos inicializada")
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")

    # Cargar modelos de ML
    try:
        ml_service.load_forecasting_model()
        ml_service.load_clustering_model()
        logger.info("Modelos de ML cargados")
    except Exception as e:
        logger.warning(f"No se pudieron cargar los modelos ML: {e}")

    yield

    # Shutdown
    logger.info("Cerrando aplicación...")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para predicción y optimización de consumo energético",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Maneja errores no capturados
    """
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )


# Rutas principales
@app.get("/")
async def root():
    """
    Endpoint raíz
    """
    return {
        "message": "API de Optimización Energética - Mega Plaza Chimbote",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint de salud para verificar que el servicio está activo
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "debug": settings.DEBUG
    }


# Incluir routers de la API
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(consumption.router, prefix=settings.API_V1_STR)
app.include_router(prediction.router, prefix=settings.API_V1_STR)
app.include_router(alerts.router, prefix=settings.API_V1_STR)
app.include_router(ml.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
