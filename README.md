# Heart Attack Prediction - Backend API

API REST para predicción de riesgo de ataque cardíaco usando Machine Learning.

## 🚀 Tecnologías

- **Framework**: FastAPI 0.104+
- **Base de Datos**: PostgreSQL 14
- **ORM**: SQLAlchemy 2.0
- **Validación**: Pydantic v2
- **ML**: scikit-learn, SHAP
- **Autenticación**: JWT (PyJWT)
- **Migraciones**: Alembic
- **Tests**: pytest, pytest-cov
- **PDF**: ReportLab
- **Python**: 3.11+

## 📋 Prerrequisitos

- Python 3.11 o superior
- Docker & Docker Compose
- PostgreSQL 14 (si no usas Docker)
- AWS CLI (para descargar modelos ML)
- Git

## 🛠️ Setup Desarrollo Local

### 1. Clonar Repositorio

```bash
git clone https://github.com/tu-org/heart-prediction-backend.git
cd heart-prediction-backend
```

### 2. Crear Entorno Virtual

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements/dev.txt
```

### 4. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Editar `.env` con tus valores:

```env
# Database
DATABASE_URL=postgresql://dev:dev123@localhost:5432/heart_prediction

# Security
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AWS (para descargar modelos)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
MODEL_BUCKET=heart-prediction-models

# App
DEBUG=True
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
```

### 5. Descargar Modelos ML

Los modelos entrenados están en S3. Para descargarlos:

```bash
# Opción 1: Usando AWS CLI
aws s3 cp s3://heart-prediction-models/production/latest/ models/ --recursive

# Opción 2: El backend los descarga automáticamente al iniciar
# (si tienes configuradas las credenciales AWS)
```

Ver más detalles en `models/README.md`

### 6. Iniciar Base de Datos (Docker)

```bash
docker-compose up -d postgres
```

### 7. Ejecutar Migraciones

```bash
alembic upgrade head
```

### 8. Iniciar Servidor de Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 9. Acceder a la API

- **API**: http://localhost:8000
- **Documentación Interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación Alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🐳 Usando Docker Compose (Recomendado)

Para iniciar todo el stack (PostgreSQL + Backend):

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL en puerto 5432
- Backend API en puerto 8000

Para ver logs:
```bash
docker-compose logs -f backend
```

Para detener:
```bash
docker-compose down
```

## 🧪 Tests

### Ejecutar Todos los Tests

```bash
pytest
```

### Tests con Cobertura

```bash
pytest --cov=app --cov-report=html --cov-report=term
```

Ver reporte de cobertura:
```bash
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### Solo Tests Unitarios

```bash
pytest tests/unit/
```

### Solo Tests de Integración

```bash
pytest tests/integration/
```

### Tests con Verbose

```bash
pytest -v
```

## 📁 Estructura del Proyecto

```
app/
├── api/              # Endpoints REST
│   └── routes/       # Rutas por módulo
├── core/             # Configuración core
├── models/           # Modelos SQLAlchemy y Pydantic
├── services/         # Lógica de negocio
├── utils/            # Utilidades
└── ml/               # Integración con ML

tests/
├── unit/             # Tests unitarios
└── integration/      # Tests de integración

alembic/              # Migraciones de BD
ml_training/          # Scripts de entrenamiento ML (opcional)
models/               # Modelos ML descargados (gitignored)
```

## 🔧 Comandos Útiles

### Migraciones de Base de Datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history
```

### Linting y Formato

```bash
# Formatear código
black app/ tests/

# Ordenar imports
isort app/ tests/

# Linting
flake8 app/ tests/

# Type checking
mypy app/
```

### Generar Documentación OpenAPI

```bash
# La documentación se genera automáticamente en /docs
# Para exportar el schema:
curl http://localhost:8000/openapi.json > openapi.json
```

## 🔐 Autenticación

La API usa JWT para autenticación. Para probar endpoints protegidos:

1. Registrar usuario:
```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "profile": {...},
    "medical_conditions": {...}
  }'
```

2. Login:
```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456"
  }'
```

3. Usar token en requests:
```bash
curl -X GET http://localhost:8000/v1/users/me \
  -H "Authorization: Bearer {tu_token_aqui}"
```

## 📊 Entrenar Nuevo Modelo ML

Si necesitas entrenar un nuevo modelo:

1. Ver instrucciones en `ml_training/README.md`
2. Entrenar modelo localmente
3. Subir a S3 usando script `ml_training/scripts/export_to_s3.py`
4. Actualizar variable `MODEL_VERSION` en `.env`
5. Reiniciar backend

## 🚀 Deploy

### Build Docker Image

```bash
docker build -t heart-prediction-backend:latest .
```

### Push a Registry

```bash
docker tag heart-prediction-backend:latest your-registry/heart-prediction-backend:latest
docker push your-registry/heart-prediction-backend:latest
```

### Deploy a AWS ECS

Ver instrucciones en el repositorio de infraestructura.

## 📝 Variables de Entorno

| Variable | Descripción | Requerida | Default |
|----------|-------------|-----------|---------|
| `DATABASE_URL` | URL de conexión PostgreSQL | Sí | - |
| `JWT_SECRET` | Secret para firmar JWT | Sí | - |
| `JWT_ALGORITHM` | Algoritmo JWT | No | HS256 |
| `JWT_EXPIRATION_HOURS` | Horas de expiración token | No | 24 |
| `AWS_ACCESS_KEY_ID` | AWS Access Key | Sí* | - |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key | Sí* | - |
| `MODEL_BUCKET` | Bucket S3 de modelos | Sí* | - |
| `DEBUG` | Modo debug | No | False |
| `CORS_ORIGINS` | Orígenes CORS permitidos | No | * |

*Requerido solo si usas modelos desde S3