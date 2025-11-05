# 🚀 Guía Rápida de Inicio - Mega Plaza Energy ML

## Para Empezar desde Cero (0)

### 📋 Prerequisitos

Necesitas tener instalado:
- **Docker** y **Docker Compose** (recomendado) - [Instalar Docker](https://docs.docker.com/get-docker/)
- O alternativamente: Python 3.11+, PostgreSQL 15+, Redis 7+

---

## 🎯 Opción 1: Docker (MÁS FÁCIL - Recomendado)

### Paso 1: Clonar el repositorio

```bash
# Clonar
git clone https://github.com/FerCholan/megaplaza-energy-ml.git

# Entrar al directorio
cd megaplaza-energy-ml
```

### Paso 2: Configurar variables de entorno (opcional)

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar si necesitas (opcional para desarrollo)
# nano .env
```

**Nota:** Para desarrollo local, puedes usar las configuraciones por defecto.

### Paso 3: Iniciar todos los servicios con Docker

```bash
# Construir e iniciar todos los servicios
docker-compose up -d

# Ver logs (opcional)
docker-compose logs -f
```

Espera 1-2 minutos mientras se descargan imágenes y se inician los servicios.

### Paso 4: Acceder a la aplicación

Una vez iniciado, abre tu navegador:

- **Frontend (Dashboard)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Documentación API Swagger**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (usuario: postgres, password: postgres)
- **Redis**: localhost:6379

### Comandos útiles de Docker

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose stop

# Reiniciar servicios
docker-compose restart

# Eliminar todo (limpieza completa)
docker-compose down -v
```

---

## 🛠️ Opción 2: Instalación Manual (Sin Docker)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/FerCholan/megaplaza-energy-ml.git
cd megaplaza-energy-ml
```

### Paso 2: Instalar PostgreSQL y Redis

**Ubuntu/Debian:**
```bash
# PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Redis
sudo apt-get install redis-server
sudo systemctl start redis-server

# Crear base de datos
sudo -u postgres createdb megaplaza_energy
```

**macOS:**
```bash
# PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Redis
brew install redis
brew services start redis

# Crear base de datos
createdb megaplaza_energy
```

**Windows:**
- Descargar PostgreSQL desde https://www.postgresql.org/download/windows/
- Descargar Redis desde https://github.com/microsoftarchive/redis/releases

### Paso 3: Configurar Backend

```bash
# Crear entorno virtual
cd backend
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/megaplaza_energy"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="tu-clave-secreta-cambia-esto"
export DEBUG=True

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend estará en: http://localhost:8000

### Paso 4: Configurar Frontend (en otra terminal)

```bash
# Crear entorno virtual
cd frontend
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variable de entorno
export BACKEND_URL="http://localhost:8000"

# Iniciar Streamlit
streamlit run app.py
```

Frontend estará en: http://localhost:8501

---

## 🧪 Verificar que todo funciona

### 1. Probar Backend API

```bash
# En tu navegador, abre:
http://localhost:8000/docs

# O con curl:
curl http://localhost:8000/health
# Debería responder: {"status":"healthy","service":"Mega Plaza Energy System","debug":true}
```

### 2. Probar Frontend

Abre http://localhost:8501 en tu navegador. Deberías ver el dashboard principal.

### 3. Ejecutar Tests (opcional)

```bash
# Instalar dependencias de test
pip install pytest

# Ejecutar tests ML
pytest tests/test_ml.py -v

# Ver cobertura
pytest tests/ --cov=backend/app --cov=ml/src
```

---

## 📊 Usar el Sistema

### Crear un usuario

```bash
# Usando la API directamente
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123",
    "role": "admin"
  }'
```

### Hacer login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=password123"
```

Guarda el `access_token` que te devuelve.

### Hacer una predicción

```bash
curl -X POST "http://localhost:8000/api/v1/predictions/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{
    "area": 250000,
    "temperatura": 22,
    "cobertura_nubes": 30,
    "presion": 1013,
    "velocidad_viento": 5,
    "mes": 6,
    "dia_semana": 2,
    "hora": 14,
    "es_fin_de_semana": 0
  }'
```

---

## 🔧 Solución de Problemas Comunes

### Puerto ya en uso

```bash
# Si el puerto 8000 o 8501 está ocupado, detén el servicio o cambia el puerto

# Ver qué está usando el puerto 8000
lsof -i :8000

# Matar proceso
kill -9 PID
```

### Error de conexión a PostgreSQL

```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Verificar que la base de datos existe
psql -U postgres -l
```

### Error de conexión a Redis

```bash
# Verificar que Redis está corriendo
redis-cli ping
# Debería responder: PONG

# Si no responde, iniciar Redis
sudo systemctl start redis-server  # Linux
brew services start redis  # macOS
```

### Docker no inicia servicios

```bash
# Ver logs de error
docker-compose logs

# Reconstruir imágenes
docker-compose build --no-cache
docker-compose up -d
```

---

## 📚 Documentación Adicional

- **Documentación API completa**: Ver `docs/API.md`
- **Guía de instalación detallada**: Ver `docs/SETUP.md`
- **README del proyecto**: Ver `README.md`
- **Implementación completa**: Ver `IMPLEMENTATION_SUMMARY.md`

---

## 🎓 Próximos Pasos

1. **Explorar la API**: http://localhost:8000/docs
2. **Ver el Dashboard**: http://localhost:8501
3. **Revisar notebooks ML**: Abrir `ml/notebooks/` con Jupyter
4. **Entrenar modelos**: Ejecutar notebooks de clustering y forecasting
5. **Agregar datos**: Cargar tu propio dataset en `data/raw/`

---

## 📞 ¿Necesitas Ayuda?

- Revisa la documentación en el directorio `docs/`
- Abre un issue en GitHub si encuentras problemas
- Revisa los logs con `docker-compose logs -f`

---

**¡Listo! Tu sistema está funcionando** 🎉

Para desarrollo, usa Docker. Es más fácil y no necesitas configurar nada.
