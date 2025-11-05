# Guía de Instalación y Configuración

## Sistema de Optimización Energética - Mega Plaza Chimbote

Esta guía te ayudará a configurar e instalar el sistema completo de predicción y optimización de consumo energético.

## Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15 o superior
- Redis 7 o superior
- Docker y Docker Compose (opcional, recomendado)
- Git

## Opción 1: Instalación con Docker (Recomendada)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones específicas.

### 3. Construir y Ejecutar con Docker Compose

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL en el puerto 5432
- Redis en el puerto 6379
- Backend FastAPI en el puerto 8000
- Frontend Streamlit en el puerto 8501

### 4. Acceder a la Aplicación

- **Frontend (Dashboard)**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Opción 2: Instalación Manual

### 1. Clonar el Repositorio

```bash
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml
```

### 2. Configurar Base de Datos PostgreSQL

```bash
# Crear base de datos
createdb megaplaza_energy

# O usando psql
psql -U postgres
CREATE DATABASE megaplaza_energy;
```

### 3. Instalar Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# macOS
brew install redis
brew services start redis
```

### 4. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp ../.env.example ../.env
# Editar .env con tus configuraciones

# Ejecutar migraciones (si se implementaron)
# alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

El backend estará disponible en http://localhost:8000

### 5. Configurar Frontend

```bash
cd frontend

# Crear entorno virtual (o usar el mismo)
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar aplicación
streamlit run app.py
```

El frontend estará disponible en http://localhost:8501

### 6. Entrenar Modelos de ML

```bash
cd ml

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar notebooks de entrenamiento
jupyter notebook

# O ejecutar scripts directamente
# (Los modelos se guardarán en ml/models/)
```

## Generar Dataset de Ejemplo

Si necesitas generar datos de prueba:

```bash
cd data
python generate_dataset.py
```

Esto creará el archivo `data/raw/energy_consumption.csv` con aproximadamente 113,000 registros.

## Verificar Instalación

### Backend

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "Megaplaza Energy ML",
  "debug": true
}
```

### Probar API

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=test@example.com&password=testpass123"
```

## Solución de Problemas

### Error de Conexión a PostgreSQL

Verifica que PostgreSQL esté ejecutándose:
```bash
sudo systemctl status postgresql
```

Verifica la configuración en `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/megaplaza_energy
```

### Error de Conexión a Redis

Verifica que Redis esté ejecutándose:
```bash
redis-cli ping
# Debería responder: PONG
```

### Modelos ML no Disponibles

Los modelos deben ser entrenados primero:
```bash
cd ml/notebooks
jupyter notebook
# Ejecutar los notebooks en orden: 01_EDA, 02_Clustering, 03_Forecasting
```

### Puerto ya en Uso

Si los puertos 8000 o 8501 están ocupados:
```bash
# Cambiar puerto del backend
uvicorn app.main:app --reload --port 8001

# Cambiar puerto del frontend
streamlit run app.py --server.port 8502
```

## Configuración de Producción

### 1. Seguridad

- Cambiar `SECRET_KEY` en `.env`
- Usar contraseñas fuertes para la base de datos
- Configurar CORS apropiadamente
- Habilitar HTTPS

### 2. Base de Datos

- Configurar respaldos automáticos
- Optimizar índices
- Configurar pooling de conexiones

### 3. Monitoreo

- Implementar logging estructurado
- Configurar alertas de sistema
- Monitorear métricas de rendimiento

### 4. Escalabilidad

- Usar un servidor WSGI como Gunicorn
- Implementar balanceo de carga
- Configurar caché con Redis
- Considerar réplicas de base de datos

## Actualización del Sistema

```bash
# Detener servicios
docker-compose down

# Actualizar código
git pull origin main

# Reconstruir imágenes
docker-compose build

# Iniciar servicios
docker-compose up -d
```

## Soporte

Para problemas o preguntas:
- Crear un issue en GitHub
- Revisar la documentación de la API en `/docs`
- Consultar logs del sistema

## Próximos Pasos

1. Revisar la documentación de la API en `docs/API.md`
2. Explorar los notebooks de ML en `ml/notebooks/`
3. Configurar alertas personalizadas
4. Entrenar modelos con datos propios
5. Personalizar el dashboard según necesidades
