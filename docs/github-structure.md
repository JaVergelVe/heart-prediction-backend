# Estructura de Repositorios GitHub - Heart Attack Prediction System

## Estrategia: 2 Repositorios + Archivos Locales

### ✅ Repositorio 1: `heart-prediction-backend`
**Propósito:** API REST + ML Integration  
**Responsable Principal:** Tu amigo (Backend)  
**Responsable Secundario:** Tú (ML Integration)  
**Tecnologías:** FastAPI + PostgreSQL + Python ML

### ✅ Repositorio 2: `heart-prediction-frontend`
**Propósito:** Aplicación web  
**Responsable:** Tu amigo (Frontend)  
**Tecnologías:** Angular + Angular Material

### 📁 Archivos Locales (NO en Git):
- **Modelos ML**: Entrenados localmente, subidos a S3
- **IaC**: Scripts de infraestructura en tu máquina local
- **Notebooks**: Análisis exploratorio en tu máquina

---

## Repositorio 1: heart-prediction-backend

### URL: `https://github.com/tu-org/heart-prediction-backend`

### Estructura de Carpetas

```
heart-prediction-backend/
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Tests y linting
│       └── deploy.yml              # Deploy a AWS ECS
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Entry point FastAPI
│   │
│   ├── api/                        # Endpoints REST
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── predictions.py
│   │       ├── health.py
│   │       └── catalogs.py
│   │
│   ├── core/                       # Configuración
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── database.py
│   │   └── logging.py
│   │
│   ├── models/                     # Modelos de datos
│   │   ├── __init__.py
│   │   ├── database.py             # SQLAlchemy
│   │   └── schemas.py              # Pydantic
│   │
│   ├── services/                   # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── prediction_service.py
│   │   ├── ml_service.py
│   │   ├── pdf_service.py
│   │   └── recommendation_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── preprocessing.py
│   │   └── constants.py
│   │
│   └── ml/                         # Integración ML
│       ├── __init__.py
│       ├── model_loader.py         # Descarga desde S3
│       ├── predictor.py
│       └── explainer.py            # SHAP
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── alembic/                        # Migraciones BD
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
├── ml_training/                    # Scripts ML (opcional en repo)
│   ├── notebooks/
│   │   ├── 01_eda.ipynb
│   │   ├── 02_feature_engineering.ipynb
│   │   └── 03_model_training.ipynb
│   ├── scripts/
│   │   ├── train_model.py
│   │   ├── evaluate_model.py
│   │   └── export_to_s3.py
│   └── README.md
│
├── models/                         # Modelos (gitignored)
│   ├── .gitignore                  # *.pkl, *.joblib
│   └── README.md                   # Cómo descargar desde S3
│
├── infrastructure/                 # IaC (opcional)
│   ├── cdk/
│   └── README.md
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

---

## Repositorio 2: heart-prediction-frontend

### URL: `https://github.com/tu-org/heart-prediction-frontend`

### Estructura de Carpetas

```
heart-prediction-frontend/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts
│   │   │   │   ├── auth.service.ts
│   │   │   │   └── storage.service.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   └── error.interceptor.ts
│   │   │   └── models/
│   │   │       ├── user.model.ts
│   │   │       ├── prediction.model.ts
│   │   │       └── api-response.model.ts
│   │   │
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── components/
│   │   │   │   ├── auth.module.ts
│   │   │   │   └── auth-routing.module.ts
│   │   │   ├── prediction/
│   │   │   ├── history/
│   │   │   └── profile/
│   │   │
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   ├── pipes/
│   │   │   └── shared.module.ts
│   │   │
│   │   ├── app.component.ts
│   │   ├── app.module.ts
│   │   └── app-routing.module.ts
│   │
│   ├── assets/
│   ├── environments/
│   ├── styles/
│   ├── index.html
│   └── main.ts
│
├── e2e/
├── Dockerfile
├── nginx.conf
├── angular.json
├── package.json
├── tsconfig.json
├── .gitignore
└── README.md
```

---

## Archivos Locales

### Estructura Local para ML

```
~/heart-prediction-local/
├── ml-workspace/
│   ├── data/
│   │   ├── raw/
│   │   │   └── heart_2022_no_nans.csv
│   │   └── processed/
│   │
│   ├── notebooks/
│   │   ├── 01_eda.ipynb
│   │   ├── 02_feature_engineering.ipynb
│   │   ├── 03_model_training.ipynb
│   │   └── 04_shap_analysis.ipynb
│   │
│   ├── models/
│   │   ├── experiments/
│   │   └── production/
│   │       └── v1.0.0/
│   │           ├── model.pkl
│   │           ├── preprocessor.pkl
│   │           └── metadata.json
│   │
│   └── scripts/
│       ├── train_model.py
│       ├── evaluate_model.py
│       └── upload_to_s3.py
│
└── infrastructure/
    ├── cdk/
    │   ├── bin/
    │   ├── lib/
    │   └── package.json
    ├── scripts/
    │   ├── deploy-dev.sh
    │   └── deploy-prod.sh
    └── README.md
```


---

## Convenciones de Git

### Estructura de Ramas

Usamos **Git Flow simplificado** con las siguientes ramas:

#### Ramas Principales

- **`main`**: Código en producción
  - Siempre estable y desplegable
  - Solo se actualiza mediante merge desde `develop`
  - Cada merge a `main` = nueva versión (tag)
  - Protegida: requiere Pull Request aprobado

- **`develop`**: Rama de desarrollo
  - Integración de features
  - Base para crear nuevas ramas de feature
  - Se despliega a ambiente de staging/dev
  - Protegida: requiere Pull Request

#### Ramas Temporales

- **`feature/*`**: Nuevas funcionalidades
  - Formato: `feature/nombre-descriptivo`
  - Se crean desde `develop`
  - Se mergean a `develop`
  - Ejemplos:
    - `feature/user-authentication`
    - `feature/prediction-form`
    - `feature/pdf-export`

- **`bugfix/*`**: Corrección de bugs en develop
  - Formato: `bugfix/nombre-descriptivo`
  - Se crean desde `develop`
  - Se mergean a `develop`
  - Ejemplos:
    - `bugfix/login-validation`
    - `bugfix/prediction-calculation`

- **`hotfix/*`**: Correcciones urgentes en producción
  - Formato: `hotfix/nombre-descriptivo`
  - Se crean desde `main`
  - Se mergean a `main` Y `develop`
  - Ejemplos:
    - `hotfix/security-vulnerability`
    - `hotfix/critical-api-error`

### Flujo de Trabajo

#### Para Features Nuevas

```bash
# 1. Actualizar develop
git checkout develop
git pull origin develop

# 2. Crear rama de feature
git checkout -b feature/nombre-feature

# 3. Hacer cambios y commits
git add .
git commit -m "feat: descripción del cambio"

# 4. Push a remoto
git push origin feature/nombre-feature

# 5. Crear Pull Request en GitHub
# develop ← feature/nombre-feature

# 6. Después de aprobación y merge, eliminar rama
git checkout develop
git pull origin develop
git branch -d feature/nombre-feature
```

#### Para Hotfixes

```bash
# 1. Crear desde main
git checkout main
git pull origin main
git checkout -b hotfix/nombre-hotfix

# 2. Hacer fix y commit
git add .
git commit -m "fix: descripción del hotfix"

# 3. Push y crear PR a main
git push origin hotfix/nombre-hotfix

# 4. Después de merge a main, también mergear a develop
git checkout develop
git pull origin develop
git merge hotfix/nombre-hotfix
git push origin develop
```

---

### Formato de Commits

Usamos **Conventional Commits** para mensajes claros y consistentes.

#### Estructura

```
<tipo>(<scope>): <descripción corta>

[cuerpo opcional]

[footer opcional]
```

#### Tipos de Commit

- **`feat`**: Nueva funcionalidad
  ```
  feat(auth): agregar login con JWT
  feat(prediction): implementar formulario de predicción
  ```

- **`fix`**: Corrección de bug
  ```
  fix(api): corregir validación de email
  fix(ui): arreglar responsive en mobile
  ```

- **`docs`**: Cambios en documentación
  ```
  docs(readme): actualizar instrucciones de setup
  docs(api): agregar ejemplos de endpoints
  ```

- **`style`**: Cambios de formato (no afectan funcionalidad)
  ```
  style(frontend): formatear código con prettier
  style(backend): ordenar imports
  ```

- **`refactor`**: Refactorización de código
  ```
  refactor(services): simplificar lógica de predicción
  refactor(models): reorganizar estructura de datos
  ```

- **`test`**: Agregar o modificar tests
  ```
  test(auth): agregar tests unitarios de login
  test(prediction): agregar tests de integración
  ```

- **`chore`**: Tareas de mantenimiento
  ```
  chore(deps): actualizar dependencias
  chore(config): configurar CI/CD
  ```

- **`perf`**: Mejoras de performance
  ```
  perf(api): optimizar query de predicciones
  perf(frontend): implementar lazy loading
  ```

#### Scopes Comunes

**Backend:**
- `auth`, `users`, `predictions`, `api`, `db`, `ml`, `services`

**Frontend:**
- `auth`, `prediction`, `history`, `profile`, `ui`, `routing`

#### Ejemplos Completos

```bash
# Feature simple
git commit -m "feat(prediction): agregar cálculo de BMI automático"

# Fix con descripción
git commit -m "fix(auth): corregir expiración de token

El token expiraba antes de tiempo debido a timezone incorrecto.
Ahora usa UTC para todos los cálculos de tiempo."

# Breaking change
git commit -m "feat(api)!: cambiar formato de response de predicción

BREAKING CHANGE: El campo 'risk_score' ahora se llama 'prediction_probability'
y retorna un valor entre 0-100 en lugar de 0-1."
```

---

### Formato de Pull Requests / Merge Requests

#### Título del PR

Usar el mismo formato que commits:

```
feat(prediction): implementar exportación a PDF
fix(auth): corregir validación de contraseña
```

#### Template del PR

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Nueva funcionalidad (feat)
- [ ] Corrección de bug (fix)
- [ ] Refactorización (refactor)
- [ ] Documentación (docs)
- [ ] Otro: _____

## ¿Cómo se probó?
Describe las pruebas realizadas:
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Pruebas manuales

## Checklist
- [ ] El código sigue las convenciones del proyecto
- [ ] He realizado self-review del código
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Los tests pasan exitosamente
- [ ] No hay warnings de linting

## Screenshots (si aplica)
Agregar capturas de pantalla para cambios de UI.

## Issues Relacionados
Closes #123
Related to #456
```

#### Proceso de Review

1. **Crear PR**: Desde rama feature/bugfix hacia develop
2. **Asignar Reviewer**: Asignar al compañero de equipo
3. **CI/CD**: Esperar que pasen los checks automáticos
4. **Code Review**: Revisor deja comentarios
5. **Hacer Cambios**: Autor responde a comentarios y hace ajustes
6. **Aprobar**: Revisor aprueba el PR
7. **Merge**: Usar "Squash and Merge" para mantener historial limpio
8. **Eliminar Rama**: Eliminar rama feature después del merge

#### Reglas de Merge

- **Squash and Merge**: Para features (un solo commit en develop)
- **Merge Commit**: Para hotfixes (mantener historial completo)
- **Rebase**: NO usar (puede causar conflictos en equipo)

---

### Versionado

Usamos **Semantic Versioning** (SemVer): `MAJOR.MINOR.PATCH`

#### Formato

```
v1.2.3
│ │ │
│ │ └─ PATCH: Bug fixes
│ └─── MINOR: Nuevas features (backward compatible)
└───── MAJOR: Breaking changes
```

#### Ejemplos

- `v1.0.0`: Release inicial
- `v1.1.0`: Agregar exportación a PDF
- `v1.1.1`: Fix en cálculo de BMI
- `v2.0.0`: Cambio en formato de API (breaking change)

#### Crear Tags

```bash
# Después de merge a main
git checkout main
git pull origin main

# Crear tag
git tag -a v1.2.0 -m "Release v1.2.0: Agregar historial de predicciones"

# Push tag
git push origin v1.2.0
```

---

### Reglas Generales

#### DO ✅

- Hacer commits pequeños y frecuentes
- Escribir mensajes descriptivos
- Hacer pull antes de push
- Crear PR para todo cambio a develop/main
- Mantener ramas actualizadas con develop
- Eliminar ramas después de merge
- Usar branches para cada feature/fix

#### DON'T ❌

- NO hacer commit directo a main o develop
- NO hacer commits gigantes con muchos cambios
- NO usar mensajes vagos ("fix", "update", "changes")
- NO dejar ramas sin mergear por mucho tiempo
- NO hacer force push a ramas compartidas
- NO mergear sin code review
- NO subir archivos grandes (modelos ML, datasets)

---

### Archivos a Ignorar (.gitignore)

#### Backend

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# ML Models
models/*.pkl
models/*.joblib
*.h5

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Database
*.db
*.sqlite3

# Logs
*.log
```

#### Frontend

```gitignore
# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build
dist/
.angular/

# Environment
.env
.env.local
environment.ts
!environment.example.ts

# IDE
.vscode/
.idea/
*.swp

# Tests
coverage/
.nyc_output/
```

---

### Recursos Adicionales

- **Conventional Commits**: https://www.conventionalcommits.org/
- **Git Flow**: https://nvie.com/posts/a-successful-git-branching-model/
- **Semantic Versioning**: https://semver.org/
- **GitHub Flow**: https://guides.github.com/introduction/flow/
