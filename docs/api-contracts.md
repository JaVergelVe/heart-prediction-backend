# API Contracts - Heart Attack Prediction System

## Información General

- **Base URL**: `https://api.heart-prediction.com/v1`
- **Protocolo**: HTTPS
- **Formato**: JSON
- **Autenticación**: JWT Bearer Token (excepto endpoints públicos)
- **Encoding**: UTF-8

## Convenciones

### Categorización de Riesgo

El sistema categoriza el riesgo de ataque cardíaco en tres niveles basados en la probabilidad calculada por el modelo ML:

- **Low (Bajo)**: `prediction_probability < 30%`
  - Indicador visual: Verde
  - Interpretación: Riesgo bajo de ataque cardíaco
  
- **Medium (Medio)**: `30% ≤ prediction_probability ≤ 70%`
  - Indicador visual: Amarillo
  - Interpretación: Riesgo moderado de ataque cardíaco
  
- **High (Alto)**: `prediction_probability > 70%`
  - Indicador visual: Rojo
  - Interpretación: Riesgo alto de ataque cardíaco

**Nota:** Estos umbrales están definidos en Requirement 3 del documento de requerimientos y deben ser consistentes en toda la aplicación.

### Explicabilidad del Modelo (XAI)

El sistema utiliza **SHAP (SHapley Additive exPlanations)** para proporcionar explicabilidad del modelo ML:

- **SHAP Values**: Cada predicción incluye valores SHAP que cuantifican la contribución de cada característica al resultado
- **Contribution Score**: Valores positivos aumentan el riesgo, valores negativos lo disminuyen
- **Top 5 Factors**: Se presentan los 5 factores con mayor impacto absoluto en el resultado
- **Interpretación**: Cada factor incluye una descripción en lenguaje natural comprensible para usuarios no técnicos

**Ejemplo de interpretación:**
```json
{
  "feature_name": "SmokerStatus",
  "feature_value": "Current smoker - now smokes every day",
  "contribution_score": 0.234,
  "interpretation": "Fumar diariamente aumenta tu riesgo en 23.4%"
}
```

### Headers Comunes

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer {jwt_token}  // Solo para endpoints protegidos
```

**Response Headers:**
```
Content-Type: application/json
X-Request-ID: {uuid}
```

### Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en validación de datos
- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: Sin permisos para el recurso
- `404 Not Found`: Recurso no encontrado
- `409 Conflict`: Conflicto (ej: email duplicado)
- `422 Unprocessable Entity`: Error de validación de negocio
- `500 Internal Server Error`: Error del servidor

### Formato de Errores

Todos los errores siguen este formato:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensaje descriptivo del error",
    "details": {
      "field": "nombre_campo",
      "reason": "razón específica"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "uuid"
  }
}
```

---

## 1. Autenticación y Usuarios

### 1.1. Registro de Usuario

**Endpoint:** `POST /auth/register`

**Descripción:** Crea una nueva cuenta de usuario con perfil médico completo.

**Autenticación:** No requerida

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "SecurePass123",
  "profile": {
    "state": "California",
    "sex": "Male",
    "birth_date": "1980-05-15",
    "height_meters": 1.75,
    "race_ethnicity_category": "White only, Non-Hispanic",
    "removed_teeth": "None of them"
  },
  "medical_conditions": {
    "had_angina": false,
    "had_stroke": false,
    "had_asthma": false,
    "had_copd": false,
    "had_skin_cancer": false,
    "had_depressive_disorder": false,
    "had_kidney_disease": false,
    "had_arthritis": false,
    "had_diabetes": "No",
    "deaf_or_hard_of_hearing": false,
    "blind_or_vision_difficulty": false,
    "difficulty_concentrating": false,
    "difficulty_walking": false,
    "difficulty_dressing_bathing": false,
    "difficulty_errands": false
  }
}
```

**Validaciones:**
- `email`: Formato válido, único en el sistema
- `password`: Mínimo 8 caracteres, al menos 1 letra y 1 número
- `sex`: Solo "Male" o "Female"
- `birth_date`: Formato ISO 8601, edad entre 18-120 años
- `height_meters`: Entre 0.5 y 2.5
- `removed_teeth`: Valores permitidos: "None of them", "1 to 5", "6 or more, but not all", "All"
- `had_diabetes`: Valores permitidos: "No", "Yes", "No, pre-diabetes or borderline diabetes", "Yes, but only during pregnancy (female)"

**Response 201 Created:**
```json
{
  "data": {
    "user_id": "uuid",
    "email": "usuario@example.com",
    "access_token": "jwt_token_string",
    "token_type": "Bearer",
    "expires_in": 86400,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Response 400 Bad Request:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Error en validación de datos",
    "details": {
      "field": "email",
      "reason": "Email ya está registrado"
    }
  }
}
```

---

### 1.2. Login de Usuario

**Endpoint:** `POST /auth/login`

**Descripción:** Autentica un usuario y retorna JWT token.

**Autenticación:** No requerida

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "SecurePass123"
}
```

**Response 200 OK:**
```json
{
  "data": {
    "user_id": "uuid",
    "email": "usuario@example.com",
    "access_token": "jwt_token_string",
    "token_type": "Bearer",
    "expires_in": 86400,
    "last_login": "2024-01-15T10:30:00Z"
  }
}
```

**Response 401 Unauthorized:**
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Email o contraseña incorrectos"
  }
}
```

---

### 1.3. Obtener Perfil de Usuario

**Endpoint:** `GET /users/me`

**Descripción:** Obtiene el perfil completo del usuario autenticado.

**Autenticación:** Requerida (JWT)

**Request:** Sin body

**Response 200 OK:**
```json
{
  "data": {
    "user_id": "uuid",
    "email": "usuario@example.com",
    "profile": {
      "state": "California",
      "sex": "Male",
      "birth_date": "1980-05-15",
      "age_category": "Age 40 to 44",
      "height_meters": 1.75,
      "race_ethnicity_category": "White only, Non-Hispanic",
      "removed_teeth": "None of them",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    "medical_conditions": {
      "had_angina": false,
      "had_stroke": false,
      "had_asthma": false,
      "had_copd": false,
      "had_skin_cancer": false,
      "had_depressive_disorder": false,
      "had_kidney_disease": false,
      "had_arthritis": false,
      "had_diabetes": "No",
      "deaf_or_hard_of_hearing": false,
      "blind_or_vision_difficulty": false,
      "difficulty_concentrating": false,
      "difficulty_walking": false,
      "difficulty_dressing_bathing": false,
      "difficulty_errands": false,
      "updated_at": "2024-01-15T10:30:00Z"
    }
  }
}
```

---

### 1.4. Actualizar Perfil de Usuario

**Endpoint:** `PUT /users/me/profile`

**Descripción:** Actualiza datos demográficos del usuario.

**Autenticación:** Requerida (JWT)

**Request Body:**
```json
{
  "state": "New York",
  "height_meters": 1.76,
  "removed_teeth": "1 to 5"
}
```

**Nota:** Solo se envían los campos que se desean actualizar. `sex`, `birth_date` y `race_ethnicity_category` no son modificables después del registro.

**Response 200 OK:**
```json
{
  "data": {
    "profile": {
      "state": "New York",
      "sex": "Male",
      "birth_date": "1980-05-15",
      "age_category": "Age 40 to 44",
      "height_meters": 1.76,
      "race_ethnicity_category": "White only, Non-Hispanic",
      "removed_teeth": "1 to 5",
      "updated_at": "2024-01-16T14:20:00Z"
    }
  }
}
```

---

### 1.5. Actualizar Condiciones Médicas

**Endpoint:** `PUT /users/me/medical-conditions`

**Descripción:** Actualiza condiciones médicas crónicas del usuario.

**Autenticación:** Requerida (JWT)

**Request Body:**
```json
{
  "had_diabetes": "Yes",
  "had_arthritis": true
}
```

**Nota:** Solo se envían los campos que se desean actualizar.

**Response 200 OK:**
```json
{
  "data": {
    "medical_conditions": {
      "had_angina": false,
      "had_stroke": false,
      "had_asthma": false,
      "had_copd": false,
      "had_skin_cancer": false,
      "had_depressive_disorder": false,
      "had_kidney_disease": false,
      "had_arthritis": true,
      "had_diabetes": "Yes",
      "deaf_or_hard_of_hearing": false,
      "blind_or_vision_difficulty": false,
      "difficulty_concentrating": false,
      "difficulty_walking": false,
      "difficulty_dressing_bathing": false,
      "difficulty_errands": false,
      "updated_at": "2024-01-16T14:25:00Z"
    }
  }
}
```

---

## 2. Predicciones

### 2.1. Crear Predicción (Usuario Registrado)

**Endpoint:** `POST /predictions`

**Descripción:** Crea una nueva predicción para usuario autenticado. Solo requiere datos variables.

**Autenticación:** Requerida (JWT)

**Request Body:**
```json
{
  "weight_kilograms": 85.5,
  "general_health": "Good",
  "physical_health_days": 2,
  "mental_health_days": 0,
  "last_checkup_time": "Within past year (anytime less than 12 months ago)",
  "physical_activities": true,
  "sleep_hours": 7.5,
  "smoker_status": "Never smoked",
  "ecigarette_usage": "Never used e-cigarettes in my entire life",
  "alcohol_drinkers": false,
  "chest_scan": false,
  "hiv_testing": true,
  "flu_vax_last_12": true,
  "pneumo_vax_ever": false,
  "tetanus_last_10_tdap": "Yes, received Tdap",
  "high_risk_last_year": false,
  "covid_pos": "No"
}
```

**Validaciones:**
- `weight_kilograms`: Entre 20 y 300
- `general_health`: "Excellent", "Very good", "Good", "Fair", "Poor"
- `physical_health_days`: Entre 0 y 30
- `mental_health_days`: Entre 0 y 30
- `sleep_hours`: Entre 0 y 24
- `smoker_status`: "Never smoked", "Former smoker", "Current smoker - now smokes some days", "Current smoker - now smokes every day"
- `ecigarette_usage`: "Never used e-cigarettes in my entire life", "Not at all (right now)", "Use them some days", "Use them every day"
- `last_checkup_time`: "Within past year...", "Within past 2 years...", "Within past 5 years...", "5 or more years ago", "Never"
- `tetanus_last_10_tdap`: "Yes, received Tdap", "Yes, received tetanus shot but not sure what type", "Yes, received tetanus shot, but not Tdap", "No, did not receive any tetanus shot in the past 10 years"
- `covid_pos`: "Yes", "No", "Tested positive using home test without health professional"

**Response 201 Created:**
```json
{
  "data": {
    "prediction_id": "uuid",
    "user_id": "uuid",
    "prediction_probability": 15.8,
    "risk_level": "Low",
    "bmi": 27.92,
    "prediction_timestamp": "2024-01-15T10:30:00Z",
    "model_version": "v1.0.0",
    "explanations": [
      {
        "feature_name": "GeneralHealth",
        "feature_value": "Good",
        "contribution_score": 0.234,
        "rank": 1,
        "interpretation": "Su estado de salud general 'Good' reduce su riesgo"
      },
      {
        "feature_name": "Age",
        "feature_value": "Age 40 to 44",
        "contribution_score": 0.189,
        "rank": 2,
        "interpretation": "Su grupo de edad tiene riesgo moderado"
      },
      {
        "feature_name": "BMI",
        "feature_value": "27.92",
        "contribution_score": 0.156,
        "rank": 3,
        "interpretation": "Su IMC está ligeramente elevado"
      },
      {
        "feature_name": "SmokerStatus",
        "feature_value": "Never smoked",
        "contribution_score": -0.142,
        "rank": 4,
        "interpretation": "No fumar reduce significativamente su riesgo"
      },
      {
        "feature_name": "PhysicalActivities",
        "feature_value": "Yes",
        "contribution_score": -0.098,
        "rank": 5,
        "interpretation": "La actividad física regular reduce su riesgo"
      }
    ],
    "recommendations": [
      {
        "text": "Mantenga su peso en un rango saludable. Su IMC actual es 27.92, considere reducirlo a menos de 25.",
        "category": "Nutrition",
        "priority": 1
      },
      {
        "text": "Continue con su rutina de actividad física regular, es excelente para su salud cardiovascular.",
        "category": "Physical Activity",
        "priority": 2
      },
      {
        "text": "Mantenga sus chequeos médicos anuales para monitorear su salud cardiovascular.",
        "category": "Preventive Care",
        "priority": 3
      }
    ]
  }
}
```

**Response 400 Bad Request:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Error en validación de datos",
    "details": {
      "field": "weight_kilograms",
      "reason": "El peso debe estar entre 20 y 300 kg"
    }
  }
}
```

---

### 2.2. Crear Predicción (Usuario No Registrado)

**Endpoint:** `POST /predictions/anonymous`

**Descripción:** Crea una predicción para usuario no registrado. Requiere TODOS los datos.

**Autenticación:** No requerida

**Request Body:**
```json
{
  "session_id": "temp_session_uuid",
  "demographic_data": {
    "state": "California",
    "sex": "Male",
    "age_category": "Age 40 to 44",
    "height_meters": 1.75,
    "race_ethnicity_category": "White only, Non-Hispanic",
    "removed_teeth": "None of them"
  },
  "medical_conditions": {
    "had_angina": false,
    "had_stroke": false,
    "had_asthma": false,
    "had_copd": false,
    "had_skin_cancer": false,
    "had_depressive_disorder": false,
    "had_kidney_disease": false,
    "had_arthritis": false,
    "had_diabetes": "No",
    "deaf_or_hard_of_hearing": false,
    "blind_or_vision_difficulty": false,
    "difficulty_concentrating": false,
    "difficulty_walking": false,
    "difficulty_dressing_bathing": false,
    "difficulty_errands": false
  },
  "current_health_data": {
    "weight_kilograms": 85.5,
    "general_health": "Good",
    "physical_health_days": 2,
    "mental_health_days": 0,
    "last_checkup_time": "Within past year (anytime less than 12 months ago)",
    "physical_activities": true,
    "sleep_hours": 7.5,
    "smoker_status": "Never smoked",
    "ecigarette_usage": "Never used e-cigarettes in my entire life",
    "alcohol_drinkers": false,
    "chest_scan": false,
    "hiv_testing": true,
    "flu_vax_last_12": true,
    "pneumo_vax_ever": false,
    "tetanus_last_10_tdap": "Yes, received Tdap",
    "high_risk_last_year": false,
    "covid_pos": "No"
  }
}
```

**Response 201 Created:**
```json
{
  "data": {
    "prediction_id": "uuid",
    "session_id": "temp_session_uuid",
    "prediction_probability": 15.8,
    "risk_level": "Low",
    "bmi": 27.92,
    "prediction_timestamp": "2024-01-15T10:30:00Z",
    "model_version": "v1.0.0",
    "explanations": [
      // Mismo formato que predicción de usuario registrado
    ],
    "recommendations": [
      // Mismo formato que predicción de usuario registrado
    ],
    "message": "Crea una cuenta para guardar tu historial de predicciones"
  }
}
```

---

### 2.3. Obtener Historial de Predicciones

**Endpoint:** `GET /predictions/history`

**Descripción:** Obtiene el historial de predicciones del usuario autenticado.

**Autenticación:** Requerida (JWT)

**Query Parameters:**
- `limit` (opcional): Número de resultados (default: 10, max: 50)
- `offset` (opcional): Offset para paginación (default: 0)
- `sort` (opcional): Campo de ordenamiento (default: "prediction_timestamp")
- `order` (opcional): Orden ascendente/descendente (default: "desc")

**Request:** `GET /predictions/history?limit=10&offset=0`

**Response 200 OK:**
```json
{
  "data": {
    "predictions": [
      {
        "prediction_id": "uuid",
        "prediction_probability": 15.8,
        "risk_level": "Low",
        "bmi": 27.92,
        "weight_kilograms": 85.5,
        "general_health": "Good",
        "prediction_timestamp": "2024-01-15T10:30:00Z"
      },
      {
        "prediction_id": "uuid",
        "prediction_probability": 18.2,
        "risk_level": "Low",
        "bmi": 28.15,
        "weight_kilograms": 86.0,
        "general_health": "Good",
        "prediction_timestamp": "2024-01-10T14:20:00Z"
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 10,
      "offset": 0,
      "has_more": true
    }
  }
}
```

---

### 2.4. Obtener Detalle de Predicción

**Endpoint:** `GET /predictions/{prediction_id}`

**Descripción:** Obtiene el detalle completo de una predicción específica.

**Autenticación:** Requerida (JWT) - Solo puede ver sus propias predicciones

**Request:** `GET /predictions/uuid-de-prediccion`

**Response 200 OK:**
```json
{
  "data": {
    "prediction_id": "uuid",
    "user_id": "uuid",
    "prediction_probability": 15.8,
    "risk_level": "Low",
    "bmi": 27.92,
    "prediction_timestamp": "2024-01-15T10:30:00Z",
    "model_version": "v1.0.0",
    "input_data": {
      "weight_kilograms": 85.5,
      "general_health": "Good",
      "physical_health_days": 2,
      "mental_health_days": 0,
      "last_checkup_time": "Within past year (anytime less than 12 months ago)",
      "physical_activities": true,
      "sleep_hours": 7.5,
      "smoker_status": "Never smoked",
      "ecigarette_usage": "Never used e-cigarettes in my entire life",
      "alcohol_drinkers": false,
      "chest_scan": false,
      "hiv_testing": true,
      "flu_vax_last_12": true,
      "pneumo_vax_ever": false,
      "tetanus_last_10_tdap": "Yes, received Tdap",
      "high_risk_last_year": false,
      "covid_pos": "No"
    },
    "explanations": [
      // Array completo de explicaciones
    ],
    "recommendations": [
      // Array completo de recomendaciones
    ]
  }
}
```

**Response 404 Not Found:**
```json
{
  "error": {
    "code": "PREDICTION_NOT_FOUND",
    "message": "Predicción no encontrada"
  }
}
```

---

### 2.5. Exportar Predicción a PDF

**Endpoint:** `GET /predictions/{prediction_id}/export/pdf`

**Descripción:** Genera y descarga un reporte PDF de la predicción.

**Autenticación:** Requerida (JWT) - Solo puede exportar sus propias predicciones

**Request:** `GET /predictions/uuid-de-prediccion/export/pdf`

**Response 200 OK:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="heart-risk-report-2024-01-15.pdf"

[Binary PDF content]
```

**Response 404 Not Found:**
```json
{
  "error": {
    "code": "PREDICTION_NOT_FOUND",
    "message": "Predicción no encontrada"
  }
}
```

---

## 3. Health Check y Metadata

### 3.1. Health Check

**Endpoint:** `GET /health`

**Descripción:** Verifica el estado del servicio.

**Autenticación:** No requerida

**Request:** Sin body

**Response 200 OK:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "ml_model": "healthy"
  }
}
```

**Response 503 Service Unavailable:**
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "unhealthy",
    "ml_model": "healthy"
  }
}
```

---

### 3.2. Obtener Información del Modelo

**Endpoint:** `GET /model/info`

**Descripción:** Obtiene información sobre el modelo ML en uso.

**Autenticación:** No requerida

**Request:** Sin body

**Response 200 OK:**
```json
{
  "data": {
    "model_version": "v1.0.0",
    "model_type": "Random Forest Classifier",
    "trained_date": "2024-01-01T00:00:00Z",
    "metrics": {
      "accuracy": 0.87,
      "precision": 0.85,
      "recall": 0.89,
      "f1_score": 0.87,
      "auc_roc": 0.92
    },
    "features_count": 39,
    "training_samples": 246022
  }
}
```

---

## 4. Validaciones y Catálogos

### 4.1. Obtener Valores Permitidos

**Endpoint:** `GET /catalogs/{field_name}`

**Descripción:** Obtiene los valores permitidos para campos categóricos.

**Autenticación:** No requerida

**Request:** `GET /catalogs/general_health`

**Response 200 OK:**
```json
{
  "data": {
    "field_name": "general_health",
    "allowed_values": [
      "Excellent",
      "Very good",
      "Good",
      "Fair",
      "Poor"
    ],
    "description": "Estado de salud general del paciente"
  }
}
```

**Campos disponibles:**
- `general_health`
- `last_checkup_time`
- `smoker_status`
- `ecigarette_usage`
- `tetanus_last_10_tdap`
- `covid_pos`
- `had_diabetes`
- `removed_teeth`
- `age_category`
- `sex`

---

### 4.2. Obtener Variables Modificables

**Endpoint:** `GET /catalogs/modifiable-variables`

**Descripción:** Obtiene la lista de variables que pueden modificarse en simulaciones what-if, junto con sus rangos válidos.

**Autenticación:** No requerida

**Request:** `GET /catalogs/modifiable-variables`

**Response 200 OK:**
```json
{
  "data": {
    "modifiable_variables": [
      {
        "name": "weight_kilograms",
        "type": "numeric",
        "min": 20,
        "max": 300,
        "unit": "kg",
        "description": "Peso corporal en kilogramos"
      },
      {
        "name": "physical_activities",
        "type": "boolean",
        "description": "Realiza actividad física regular"
      },
      {
        "name": "sleep_hours",
        "type": "numeric",
        "min": 0,
        "max": 24,
        "unit": "hours",
        "description": "Horas de sueño promedio por noche"
      },
      {
        "name": "smoker_status",
        "type": "categorical",
        "allowed_values": [
          "Never smoked",
          "Former smoker",
          "Current smoker - now smokes some days",
          "Current smoker - now smokes every day"
        ],
        "description": "Estado de fumador"
      },
      {
        "name": "ecigarette_usage",
        "type": "categorical",
        "allowed_values": [
          "Never used e-cigarettes in my entire life",
          "Not at all (right now)",
          "Use them some days",
          "Use them every day"
        ],
        "description": "Uso de cigarrillos electrónicos"
      },
      {
        "name": "alcohol_drinkers",
        "type": "boolean",
        "description": "Consume alcohol regularmente"
      },
      {
        "name": "general_health",
        "type": "categorical",
        "allowed_values": [
          "Excellent",
          "Very good",
          "Good",
          "Fair",
          "Poor"
        ],
        "description": "Estado de salud general percibido"
      },
      {
        "name": "physical_health_days",
        "type": "numeric",
        "min": 0,
        "max": 30,
        "unit": "days",
        "description": "Días con mala salud física en el último mes"
      },
      {
        "name": "mental_health_days",
        "type": "numeric",
        "min": 0,
        "max": 30,
        "unit": "days",
        "description": "Días con mala salud mental en el último mes"
      }
    ],
    "fixed_variables": [
      "sex",
      "age_category",
      "height_meters",
      "race_ethnicity_category",
      "had_angina",
      "had_stroke",
      "had_asthma",
      "had_copd",
      "had_skin_cancer",
      "had_depressive_disorder",
      "had_kidney_disease",
      "had_arthritis",
      "had_diabetes",
      "deaf_or_hard_of_hearing",
      "blind_or_vision_difficulty",
      "difficulty_concentrating",
      "difficulty_walking",
      "difficulty_dressing_bathing",
      "difficulty_errands"
    ]
  }
}
```

---

## 4. Simulaciones What-If

### 4.1. Calcular Simulación What-If

**Endpoint:** `POST /predictions/{prediction_id}/simulate`

**Descripción:** Calcula una simulación what-if en tiempo real modificando variables modificables de una predicción existente. La simulación NO se guarda en la base de datos - es una operación de solo lectura que retorna resultados inmediatos para exploración del usuario.

**Autenticación:** Requerida (JWT) - Solo puede simular sobre sus propias predicciones

**Request Body:**
```json
{
  "modified_variables": {
    "weight_kilograms": 75.0,
    "physical_activities": true,
    "sleep_hours": 8.0,
    "smoker_status": "Former smoker",
    "alcohol_drinkers": false,
    "general_health": "Very good"
  }
}
```

**Variables Modificables Permitidas:**
- `weight_kilograms` (20-300 kg)
- `physical_activities` (boolean)
- `sleep_hours` (0-24 horas)
- `smoker_status` ("Never smoked", "Former smoker", "Current smoker - now smokes some days", "Current smoker - now smokes every day")
- `ecigarette_usage` ("Never used e-cigarettes in my entire life", "Not at all (right now)", "Use them some days", "Use them every day")
- `alcohol_drinkers` (boolean)
- `general_health` ("Excellent", "Very good", "Good", "Fair", "Poor")
- `physical_health_days` (0-30)
- `mental_health_days` (0-30)

**Nota:** Solo se envían las variables que se desean modificar. Las variables no incluidas mantienen sus valores originales de la predicción base. Las variables demográficas y condiciones médicas crónicas NO pueden modificarse.

**Response 200 OK:**
```json
{
  "data": {
    "original_prediction_id": "uuid",
    "simulated_at": "2024-01-15T11:00:00Z",
    "prediction_probability": 12.3,
    "risk_level": "Low",
    "bmi": 24.49,
    "model_version": "v1.0.0",
    "comparison": {
      "original_probability": 15.8,
      "original_risk_level": "Low",
      "probability_change": -3.5,
      "probability_change_percentage": -22.15,
      "risk_level_changed": false,
      "interpretation": "Tu riesgo disminuiría de 15.8% a 12.3% (reducción de 22.15%)"
    },
    "modified_variables": {
      "weight_kilograms": {
        "original": 85.5,
        "modified": 75.0,
        "impact_score": -2.1,
        "interpretation": "Reducir peso de 85.5 kg a 75.0 kg disminuye tu riesgo significativamente"
      },
      "smoker_status": {
        "original": "Never smoked",
        "modified": "Former smoker",
        "impact_score": 0.3,
        "interpretation": "Este cambio tiene un impacto mínimo en tu riesgo"
      },
      "general_health": {
        "original": "Good",
        "modified": "Very good",
        "impact_score": -1.2,
        "interpretation": "Mejorar tu salud general reduce tu riesgo"
      }
    },
    "top_impact_factors": [
      {
        "variable": "weight_kilograms",
        "impact_score": -2.1,
        "rank": 1
      },
      {
        "variable": "general_health",
        "impact_score": -1.2,
        "rank": 2
      },
      {
        "variable": "smoker_status",
        "impact_score": 0.3,
        "rank": 3
      }
    ],
    "explanations": [
      {
        "feature_name": "BMI",
        "feature_value": "24.49",
        "contribution_score": -0.187,
        "rank": 1,
        "interpretation": "Tu nuevo IMC está en rango saludable"
      },
      {
        "feature_name": "GeneralHealth",
        "feature_value": "Very good",
        "contribution_score": -0.156,
        "rank": 2,
        "interpretation": "Tu estado de salud general 'Very good' reduce significativamente tu riesgo"
      }
    ]
  }
}
```

**Response 400 Bad Request:**
```json
{
  "error": {
    "code": "INVALID_VARIABLE",
    "message": "Variable no modificable",
    "details": {
      "field": "had_diabetes",
      "reason": "Las condiciones médicas crónicas no pueden modificarse en simulaciones"
    }
  }
}
```

**Response 404 Not Found:**
```json
{
  "error": {
    "code": "PREDICTION_NOT_FOUND",
    "message": "Predicción original no encontrada"
  }
}
```

**Nota Importante:** Las simulaciones son cálculos en tiempo real que NO se persisten en la base de datos. Cada llamada a este endpoint recalcula la simulación desde cero. Esto mantiene las simulaciones como herramientas exploratorias temporales sin contaminar el historial de predicciones reales del usuario.

---

## 5. Resumen de Endpoints

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Registro de usuario |
| POST | `/auth/login` | No | Login de usuario |
| GET | `/users/me` | Sí | Obtener perfil |
| PUT | `/users/me/profile` | Sí | Actualizar perfil |
| PUT | `/users/me/medical-conditions` | Sí | Actualizar condiciones médicas |
| POST | `/predictions` | Sí | Crear predicción (registrado) |
| POST | `/predictions/anonymous` | No | Crear predicción (no registrado) |
| GET | `/predictions/history` | Sí | Historial de predicciones |
| GET | `/predictions/{id}` | Sí | Detalle de predicción |
| GET | `/predictions/{id}/export/pdf` | Sí | Exportar a PDF |
| POST | `/predictions/{id}/simulate` | Sí | Calcular simulación what-if (no persiste) |
| GET | `/health` | No | Health check |
| GET | `/model/info` | No | Info del modelo |
| GET | `/catalogs/{field}` | No | Valores permitidos |

---

## 6. Notas de Implementación

### 6.1. Seguridad

- Todos los endpoints deben usar HTTPS
- JWT tokens expiran en 24 horas
- Passwords deben hashearse con bcrypt (salt rounds: 12)
- Implementar rate limiting: 100 requests/minuto por IP
- Validar todos los inputs en backend (no confiar en frontend)

### 6.2. Performance

- Implementar cache para catálogos (TTL: 1 hora)
- Implementar cache para perfil de usuario (TTL: 5 minutos)
- Índices en BD ya definidos en schema SQL
- Paginación obligatoria para listas (max 50 items)

### 6.3. Logging

- Loggear todas las predicciones con request_id
- NO loggear datos médicos sensibles en logs
- Loggear errores con stack trace
- Incluir X-Request-ID en todos los responses

### 6.4. CORS

Permitir requests desde:
- `http://localhost:4200` (desarrollo)
- `https://app.heart-prediction.com` (producción)

Headers permitidos:
- `Content-Type`
- `Authorization`
- `X-Request-ID`

### 6.5. Versionado

- API versionada en URL: `/v1/`
- Mantener compatibilidad hacia atrás
- Deprecar endpoints con 6 meses de anticipación

### 6.6. Características Especiales

#### Explicabilidad (XAI)
- Calcular SHAP values para cada predicción usando el modelo entrenado
- Almacenar top 5 factores en `prediction_explanations` table
- Generar interpretaciones en lenguaje natural basadas en contribution_score
- Valores positivos = aumentan riesgo, valores negativos = disminuyen riesgo

#### Simulaciones What-If
- Solo usuarios autenticados pueden crear simulaciones
- Simulaciones NO se persisten en base de datos - son cálculos en tiempo real
- Variables modificables: peso, actividad física, sueño, tabaco, alcohol, salud general, días de mala salud
- Variables fijas: demográficos, condiciones médicas crónicas, historial médico
- Calcular impacto individual de cada variable modificada comparando con original
- Ordenar variables por impacto absoluto para mostrar cuáles tienen mayor efecto
- Cada simulación es independiente - no hay historial de simulaciones guardado

#### Categorización de Riesgo
- Aplicar umbrales consistentes: <30% = Low, 30-70% = Medium, >70% = High
- Incluir `risk_level` en todas las respuestas de predicción
- Frontend debe usar colores consistentes: verde (Low), amarillo (Medium), rojo (High)

---

## 7. Ejemplos de Uso

### Flujo Completo: Usuario Registrado

```bash
# 1. Registro
curl -X POST https://api.heart-prediction.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "profile": {...},
    "medical_conditions": {...}
  }'

# 2. Login (si ya está registrado)
curl -X POST https://api.heart-prediction.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'

# 3. Crear predicción
curl -X POST https://api.heart-prediction.com/v1/predictions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "weight_kilograms": 85.5,
    "general_health": "Good",
    ...
  }'

# 4. Ver historial
curl -X GET https://api.heart-prediction.com/v1/predictions/history \
  -H "Authorization: Bearer {token}"

# 5. Crear simulación what-if (no se guarda)
curl -X POST https://api.heart-prediction.com/v1/predictions/{prediction_id}/simulate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "modified_variables": {
      "weight_kilograms": 75.0,
      "smoker_status": "Never smoked",
      "physical_activities": true,
      "sleep_hours": 8.0
    }
  }'

# 6. Exportar PDF
curl -X GET https://api.heart-prediction.com/v1/predictions/{id}/export/pdf \
  -H "Authorization: Bearer {token}" \
  --output report.pdf
```

### Flujo Completo: Usuario No Registrado

```bash
# 1. Crear predicción anónima
curl -X POST https://api.heart-prediction.com/v1/predictions/anonymous \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "temp_uuid",
    "demographic_data": {...},
    "medical_conditions": {...},
    "current_health_data": {...}
  }'

# Nota: Los usuarios no registrados NO pueden crear simulaciones what-if
# ni acceder a historial. Deben crear una cuenta para estas funcionalidades.
```

### Ejemplo de Respuesta: Predicción con XAI

```json
{
  "data": {
    "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
    "prediction_probability": 45.7,
    "risk_level": "Medium",
    "bmi": 29.3,
    "explanations": [
      {
        "feature_name": "SmokerStatus",
        "feature_value": "Current smoker - now smokes every day",
        "contribution_score": 0.187,
        "rank": 1,
        "interpretation": "Fumar diariamente aumenta significativamente tu riesgo"
      },
      {
        "feature_name": "BMI",
        "feature_value": "29.3",
        "contribution_score": 0.142,
        "rank": 2,
        "interpretation": "Tu IMC está en rango de sobrepeso, lo que aumenta tu riesgo"
      },
      {
        "feature_name": "Age",
        "feature_value": "Age 55 to 59",
        "contribution_score": 0.098,
        "rank": 3,
        "interpretation": "Tu grupo de edad tiene un riesgo moderado-alto"
      },
      {
        "feature_name": "PhysicalActivities",
        "feature_value": "No",
        "contribution_score": 0.076,
        "rank": 4,
        "interpretation": "La falta de actividad física aumenta tu riesgo"
      },
      {
        "feature_name": "GeneralHealth",
        "feature_value": "Fair",
        "contribution_score": 0.065,
        "rank": 5,
        "interpretation": "Tu estado de salud general 'Fair' contribuye al riesgo"
      }
    ],
    "recommendations": [
      {
        "text": "IMPORTANTE: Tu riesgo es MEDIO. Consulta con un médico para evaluación cardiovascular completa.",
        "category": "Medical Consultation",
        "priority": 1
      },
      {
        "text": "Considera un programa de cesación de tabaco. Dejar de fumar es la acción más efectiva para reducir tu riesgo.",
        "category": "Smoking Cessation",
        "priority": 2
      },
      {
        "text": "Reduce tu peso a un IMC saludable (18.5-24.9). Tu IMC actual es 29.3.",
        "category": "Nutrition",
        "priority": 3
      },
      {
        "text": "Incorpora actividad física regular: al menos 150 minutos de ejercicio moderado por semana.",
        "category": "Physical Activity",
        "priority": 4
      }
    ]
  }
}
```

### Ejemplo de Respuesta: Simulación What-If (Cálculo en Tiempo Real)

```json
{
  "data": {
    "original_prediction_id": "550e8400-e29b-41d4-a716-446655440000",
    "simulated_at": "2024-01-15T11:00:00Z",
    "prediction_probability": 28.4,
    "risk_level": "Low",
    "comparison": {
      "original_probability": 45.7,
      "original_risk_level": "Medium",
      "probability_change": -17.3,
      "probability_change_percentage": -37.86,
      "risk_level_changed": true,
      "interpretation": "¡Excelente! Tu riesgo disminuiría de MEDIO (45.7%) a BAJO (28.4%), una reducción de 37.86%"
    },
    "modified_variables": {
      "smoker_status": {
        "original": "Current smoker - now smokes every day",
        "modified": "Never smoked",
        "impact_score": -8.9,
        "interpretation": "Dejar de fumar reduciría tu riesgo en 8.9 puntos porcentuales - el cambio más impactante"
      },
      "weight_kilograms": {
        "original": 95.0,
        "modified": 75.0,
        "impact_score": -5.2,
        "interpretation": "Reducir 20 kg disminuiría tu riesgo en 5.2 puntos porcentuales"
      },
      "physical_activities": {
        "original": false,
        "modified": true,
        "impact_score": -2.4,
        "interpretation": "Incorporar actividad física regular reduciría tu riesgo en 2.4 puntos"
      },
      "sleep_hours": {
        "original": 5.5,
        "modified": 8.0,
        "impact_score": -0.8,
        "interpretation": "Mejorar tus horas de sueño tendría un impacto positivo moderado"
      }
    },
    "top_impact_factors": [
      {
        "variable": "smoker_status",
        "impact_score": -8.9,
        "rank": 1
      },
      {
        "variable": "weight_kilograms",
        "impact_score": -5.2,
        "rank": 2
      },
      {
        "variable": "physical_activities",
        "impact_score": -2.4,
        "rank": 3
      }
    ]
  }
}
```
