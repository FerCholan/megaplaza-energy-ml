# Documentación de la API

## Sistema de Optimización Energética - API REST

Base URL: `http://localhost:8000/api/v1`

Documentación interactiva: `http://localhost:8000/docs`

## Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación.

### Registro de Usuario

```http
POST /api/v1/auth/register
```

**Body:**
```json
{
  "email": "usuario@example.com",
  "password": "password123",
  "role": "user"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00"
}
```

### Login

```http
POST /api/v1/auth/login
```

**Body (form-data):**
```
username: usuario@example.com
password: password123
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Obtener Usuario Actual

```http
GET /api/v1/auth/me
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00"
}
```

## Consumo Energético

### Obtener Histórico de Consumo

```http
GET /api/v1/consumption/?skip=0&limit=100
Authorization: Bearer {token}
```

**Parámetros:**
- `skip` (opcional): Número de registros a saltar (paginación)
- `limit` (opcional): Número máximo de registros a retornar
- `start_date` (opcional): Fecha inicial (ISO 8601)
- `end_date` (opcional): Fecha final (ISO 8601)

**Respuesta:**
```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T12:00:00",
    "kwh": 750.5,
    "area": 250000.0,
    "temperatura": 22.5,
    "cobertura_nubes": 45.0,
    "presion": 1013.0,
    "velocidad_viento": 5.2,
    "mes": 1,
    "dia_semana": 0,
    "hora": 12,
    "es_fin_de_semana": 0,
    "medidor_electricidad": 1,
    "medidor_agua_fria": 1,
    "created_at": "2024-01-15T12:05:00"
  }
]
```

### Obtener Consumo en Tiempo Real

```http
GET /api/v1/consumption/realtime?hours=24
Authorization: Bearer {token}
```

**Parámetros:**
- `hours` (opcional): Horas hacia atrás (default: 24)

**Respuesta:** Array de consumos de las últimas horas

### Registrar Nuevo Consumo

```http
POST /api/v1/consumption/
Authorization: Bearer {token}
```

**Body:**
```json
{
  "timestamp": "2024-01-15T12:00:00",
  "kwh": 750.5,
  "area": 250000.0,
  "temperatura": 22.5,
  "hora": 12,
  "dia_semana": 0,
  "es_fin_de_semana": 0
}
```

### Obtener Estadísticas de Consumo

```http
GET /api/v1/consumption/stats?days=7
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "period_days": 7,
  "average_kwh": 750.5,
  "min_kwh": 450.2,
  "max_kwh": 1200.8,
  "total_kwh": 126090.0
}
```

## Predicciones

### Realizar Predicción

```http
POST /api/v1/predictions/predict
Authorization: Bearer {token}
```

**Body:**
```json
{
  "area": 250000.0,
  "temperatura": 22.5,
  "cobertura_nubes": 45.0,
  "presion": 1013.0,
  "velocidad_viento": 5.2,
  "mes": 1,
  "dia_semana": 0,
  "hora": 12,
  "es_fin_de_semana": 0
}
```

**Respuesta:**
```json
{
  "predicted_kwh": 755.3,
  "timestamp": "2024-01-15T12:00:00",
  "model_version": "v1.0"
}
```

### Obtener Histórico de Predicciones

```http
GET /api/v1/predictions/?skip=0&limit=100
Authorization: Bearer {token}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T12:00:00",
    "predicted_kwh": 755.3,
    "real_kwh": 750.5,
    "model_version": "v1.0",
    "error": 4.8,
    "created_at": "2024-01-15T12:05:00"
  }
]
```

## Alertas

### Obtener Alertas

```http
GET /api/v1/alerts/?skip=0&limit=50
Authorization: Bearer {token}
```

**Parámetros:**
- `skip` (opcional): Paginación
- `limit` (opcional): Límite de resultados
- `status` (opcional): Filtrar por estado (active, resolved, dismissed)
- `severity` (opcional): Filtrar por severidad (critical, high, medium, low)

**Respuesta:**
```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T12:00:00",
    "tipo": "high_consumption",
    "mensaje": "Consumo alto detectado: 1050.5 kWh",
    "area": "Piso 2",
    "threshold_exceeded": 50.5,
    "severity": "high",
    "status": "active",
    "created_at": "2024-01-15T12:05:00"
  }
]
```

### Obtener Alertas Activas

```http
GET /api/v1/alerts/active?limit=10
Authorization: Bearer {token}
```

### Obtener Estadísticas de Alertas

```http
GET /api/v1/alerts/stats
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "total": 45,
  "active": 5,
  "resolved": 40,
  "by_severity": {
    "critical": 2,
    "high": 8,
    "medium": 15,
    "low": 20
  },
  "by_type": {
    "high_consumption": 20,
    "anomaly": 15,
    "prediction_error": 10
  }
}
```

### Configurar Alertas

```http
POST /api/v1/alerts/config
Authorization: Bearer {token}
```

**Body:**
```json
{
  "tipo": "high_consumption",
  "threshold": 1000.0,
  "enabled": true,
  "notification_email": "admin@example.com"
}
```

### Resolver Alerta

```http
PUT /api/v1/alerts/{alert_id}/resolve
Authorization: Bearer {token}
```

## Machine Learning

### Información de Modelos

```http
GET /api/v1/ml/models/info
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "forecasting_loaded": true,
  "clustering_loaded": true,
  "version": "v1.0"
}
```

### Cargar Modelos

```http
POST /api/v1/ml/models/load
Authorization: Bearer {token}
```

**Nota:** Requiere permisos de administrador

### Información de Clusters

```http
GET /api/v1/ml/clusters
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "n_clusters": 3,
  "model_type": "KMeans"
}
```

### Predecir Cluster

```http
POST /api/v1/ml/cluster/predict
Authorization: Bearer {token}
```

**Body:**
```json
{
  "area": 250000.0,
  "temperatura": 22.5,
  "hora": 12,
  "dia_semana": 0
}
```

**Respuesta:**
```json
{
  "cluster": 1,
  "features": {
    "area": 250000.0,
    "temperatura": 22.5,
    "hora": 12,
    "dia_semana": 0
  }
}
```

### Re-entrenar Modelos

```http
POST /api/v1/ml/retrain
Authorization: Bearer {token}
```

**Nota:** Requiere permisos de administrador

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en los datos enviados
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: No tiene permisos
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Error de validación
- `500 Internal Server Error`: Error del servidor

## Límites de Rate

- Máximo 100 solicitudes por minuto por usuario
- Máximo 1000 solicitudes por hora por usuario

## Ejemplos de Uso

### Python (requests)

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "user@example.com", "password": "password123"}
)
token = response.json()["access_token"]

# Headers con autenticación
headers = {"Authorization": f"Bearer {token}"}

# Obtener consumo
response = requests.get(
    "http://localhost:8000/api/v1/consumption/realtime",
    params={"hours": 24},
    headers=headers
)
data = response.json()
```

### JavaScript (fetch)

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'username=user@example.com&password=password123'
});
const {access_token} = await loginResponse.json();

// Realizar predicción
const predictionResponse = await fetch('http://localhost:8000/api/v1/predictions/predict', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    area: 250000,
    temperatura: 22.5,
    hora: 12,
    dia_semana: 0
  })
});
const prediction = await predictionResponse.json();
```

## Soporte

Para más información, consulta la documentación interactiva en:
`http://localhost:8000/docs`
