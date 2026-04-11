# Heart Attack Prediction - Backend API

API REST para predicción de riesgo de ataque cardíaco usando Machine Learning (MLP + SHAP).

## 🚀 Tecnologías

- **Framework**: FastAPI 0.109+
- **Base de Datos**: MySQL 8.0 (SQLAlchemy 2.0 + PyMySQL)
- **Validación**: Pydantic v2
- **ML**: scikit-learn 1.6.1, SHAP 0.43+
- **Autenticación**: JWT (PyJWT 2.8+) + bcrypt
- **PDF**: ReportLab 4.0+
- **Tests**: pytest 8.0+, pytest-cov, httpx
- **Python**: 3.11+

## 📋 Prerrequisitos

- Python 3.11 o superior
- Docker & Docker Compose
- MySQL 8.0 (si no usas Docker)

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
pip install -r requirements/test.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
APP_NAME=Heart Attack Prediction API
DEBUG=false
API_VERSION=1.0.0

# Base de datos MySQL
DATABASE_URL=mysql+pymysql://heart_user:heart_pass@localhost:3306/heart_attack_prediction

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=86400

# Modelos ML (ruta local a los artefactos .joblib)
ML_MODELS_DIR=app/ml/models
```

### 5. Iniciar Base de Datos y Backend (Docker)

```bash
docker-compose up -d
```

Esto levanta:
- MySQL 8.0 en puerto `3306`
- Backend API en puerto `8000`

Para ver logs:
```bash
docker-compose logs -f backend
```

Para detener:
```bash
docker-compose down
```

### 6. Iniciar Solo el Backend (sin Docker)

Asegúrate de tener MySQL corriendo y el `.env` configurado, luego:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Acceder a la API

| Recurso | URL |
|---------|-----|
| API base | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/v1/health |

## 📁 Estructura del Proyecto

```
app/
├── api/
│   └── routes/           # auth, users, predictions, catalogs, health
├── constants/            # Constantes tipadas por módulo
├── core/                 # Config, DB, excepciones, formato de tiempo
├── ml/
│   ├── artifacts.py      # Carga de artefactos .joblib
│   ├── feature_row.py    # Construcción del vector de features
│   ├── predictor.py      # Pipeline: OHE → Scaler → MLP → SHAP
│   └── models/           # Artefactos ML (best_mlp_model, encoders, scaler, shap_background)
├── models/               # Modelos SQLAlchemy (users, user_profiles, medical_conditions, predictions)
├── schemas/              # Schemas Pydantic (auth, user, prediction)
├── services/             # Lógica de negocio (auth, user, prediction, pdf, recommendations, catalog)
└── main.py               # Entry point FastAPI

tests/
├── unit/                 # Tests unitarios (BMI, risk level)
└── integration/          # Tests de integración (auth, users, predictions, catalogs, security)

infra/                    # Terraform + scripts de deploy AWS
docs/                     # Contratos API, mapeo de BD, requerimientos
requirements/
├── base.txt              # Dependencias de producción
└── test.txt              # base.txt + pytest, httpx
```

## 🔌 Endpoints

Todos los endpoints tienen el prefijo `/v1`.

### Autenticación

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `POST` | `/v1/auth/register` | No | Registro con perfil y condiciones médicas |
| `POST` | `/v1/auth/login` | No | Login, retorna JWT |

### Usuarios

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `GET` | `/v1/users/me` | Sí | Perfil completo del usuario autenticado |
| `PUT` | `/v1/users/me/profile` | Sí | Actualizar datos demográficos |
| `PUT` | `/v1/users/me/medical-conditions` | Sí | Actualizar condiciones médicas crónicas |

### Predicciones

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `POST` | `/v1/predictions` | Sí | Crear predicción (usuario registrado) |
| `POST` | `/v1/predictions/anonymous` | No | Crear predicción anónima (session_id) |
| `GET` | `/v1/predictions/history` | Sí | Historial paginado de predicciones |
| `GET` | `/v1/predictions/{id}` | Sí | Detalle con valores SHAP |
| `GET` | `/v1/predictions/{id}/export/pdf` | Sí | Exportar predicción como PDF |
| `POST` | `/v1/predictions/{id}/simulate` | Sí | Simulación what-if (sin persistir) |

### Catálogos y Salud

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `GET` | `/v1/catalogs/modifiable-variables` | No | Variables modificables en simulación |
| `GET` | `/v1/catalogs/{field}` | No | Valores permitidos para un campo categórico |
| `GET` | `/v1/health` | No | Estado del servicio (DB + modelo ML) |

## 🤖 Pipeline ML

El modelo es un **MLP (Multi-Layer Perceptron)** entrenado con el dataset BRFSS 2022.

**Artefactos requeridos en `app/ml/models/`:**

| Archivo | Descripción |
|---------|-------------|
| `best_mlp_model.joblib` | Clasificador MLP entrenado |
| `one_hot_encoder.joblib` | Encoder para variables categóricas |
| `standard_scaler.joblib` | Scaler para variables numéricas |
| `label_encoder.joblib` | Encoder del target (HadHeartAttack → 0/1) |
| `shap_background.joblib` | Datos de fondo para cálculo SHAP |

**Flujo de inferencia:**

1. Construir vector de 39 features desde perfil + condiciones médicas + encuesta
2. Aplicar `OneHotEncoder` a variables categóricas
3. Aplicar `StandardScaler` a variables numéricas
4. Inferencia con MLP → probabilidad (0–100%)
5. Calcular SHAP values → top 5 factores contribuyentes
6. Clasificar nivel de riesgo:
   - **Low**: probabilidad < 30%
   - **Medium**: 30% ≤ probabilidad ≤ 70%
   - **High**: probabilidad > 70%

## 🗄️ Base de Datos

El esquema usa 4 tablas principales:

| Tabla | Descripción |
|-------|-------------|
| `users` | Autenticación (email, password_hash, is_active) |
| `user_profiles` | Datos demográficos (sexo, fecha de nacimiento, altura, dientes removidos) |
| `medical_conditions` | 15 condiciones crónicas (angina, diabetes, COPD, artritis, etc.) |
| `predictions` | Snapshot de cada predicción + resultado ML (probabilidad, risk_level, model_version) |

> Ver mapeo detallado en [`docs/database-mapping.md`](docs/database-mapping.md)

## 🧪 Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html --cov-report=term

# Solo unitarios
pytest tests/unit/

# Solo integración
pytest tests/integration/

# Verbose
pytest -v
```

Ver reporte HTML de cobertura:
```bash
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

## 🔐 Autenticación

La API usa **JWT Bearer Token**. Expiración por defecto: 24 horas (`ACCESS_TOKEN_EXPIRE_SECONDS=86400`).

**1. Registrar usuario:**
```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "profile": {
      "sex": "Male",
      "birth_date": "1990-05-15",
      "height_meters": 1.75,
      "removed_teeth": "None of them"
    },
    "medical_conditions": {
      "had_diabetes": "No",
      "had_angina": false
    }
  }'
```

**2. Login:**
```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123456"}'
```

**3. Usar token:**
```bash
curl -X GET http://localhost:8000/v1/users/me \
  -H "Authorization: Bearer {tu_token_aqui}"
```

## 📝 Variables de Entorno

| Variable | Descripción | Requerida | Default |
|----------|-------------|-----------|---------|
| `DATABASE_URL` | URL de conexión MySQL (PyMySQL) | Sí | — |
| `JWT_SECRET_KEY` | Secret para firmar JWT | Sí | placeholder dev |
| `JWT_ALGORITHM` | Algoritmo JWT | No | `HS256` |
| `ACCESS_TOKEN_EXPIRE_SECONDS` | Segundos de expiración del token | No | `86400` (24h) |
| `ML_MODELS_DIR` | Ruta a los artefactos `.joblib` | No | `app/ml/models` |
| `APP_NAME` | Nombre de la aplicación | No | `Heart Attack Prediction API` |
| `API_VERSION` | Versión de la API | No | `1.0.0` |
| `DEBUG` | Modo debug de FastAPI | No | `false` |

## 🐳 Docker

**Build manual:**
```bash
docker build -t heart-prediction-backend:latest .
```

El contenedor corre con usuario no-root (`appuser:1001`) y expone el puerto `8000`.
Health check interno: `GET /v1/health` cada 30 segundos.

## 🚀 Deploy AWS

Ver instrucciones completas en [`infra/DEPLOY.md`](infra/DEPLOY.md).

Los scripts de Terraform en `infra/` gestionan el despliegue en AWS (EC2 + RDS MySQL).

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [`docs/api-contracts.md`](docs/api-contracts.md) | Contratos completos de la API (request/response, validaciones) |
| [`docs/database-mapping.md`](docs/database-mapping.md) | Mapeo dataset → tablas DB, pipeline del modelo |
| [`docs/requirements.md`](docs/requirements.md) | Requerimientos funcionales del sistema |
| [`docs/github-structure.md`](docs/github-structure.md) | Estructura del repositorio |
