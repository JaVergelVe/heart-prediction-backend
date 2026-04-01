# Mapeo de Variables Dataset → Base de Datos

## Resumen de Tablas

El diseño de base de datos separa la información en 5 tablas principales:

1. **users**: Autenticación y control de acceso
2. **user_profiles**: Datos demográficos permanentes
3. **medical_conditions**: Condiciones médicas crónicas
4. **predictions**: Datos variables y resultados de predicción
5. **prediction_explanations**: Explicabilidad del modelo (feature importance)
6. **recommendations**: Recomendaciones personalizadas

## Pipeline del Modelo Predictivo

El modelo entrenado (`best_mlp_model.joblib`) usa los siguientes artefactos de preprocesamiento:

| Artefacto | Archivo | Aplicado a |
|-----------|---------|------------|
| OneHotEncoder | `one_hot_encoder.joblib` | Variables categóricas (GeneralHealth, LastCheckupTime, RemovedTeeth, HadDiabetes, SmokerStatus, ECigaretteUsage, AgeCategory, TetanusLast10Tdap, CovidPos) |
| StandardScaler | `standard_scaler.joblib` | Variables numéricas continuas (PhysicalHealthDays, MentalHealthDays, SleepHours, HeightInMeters, WeightInKilograms, BMI) |
| LabelEncoder | `label_encoder.joblib` | Variable target (HadHeartAttack → 0/1) |

> Los datos se almacenan en la DB con sus valores originales (sin escalar/encodear). El preprocesamiento se aplica en tiempo de inferencia antes de pasar al modelo.

## Mapeo Detallado: Dataset → Tablas

### Variables en `user_profiles` (Datos Demográficos Permanentes)

| Variable Dataset | Columna DB | Tipo | Notas |
|-----------------|------------|------|-------|
| Sex | sex | VARCHAR(10) | 'Male' o 'Female' |
| AgeCategory | age_category | VARCHAR(20) | Calculado desde birth_date |
| HeightInMeters | height_meters | DECIMAL(4,2) | Rango: 0.5 - 2.5 |
| RemovedTeeth | removed_teeth | VARCHAR(20) | Cantidad de dientes removidos |
| - | birth_date | DATE | Para calcular age_category automáticamente |

> `State` y `RaceEthnicityCategory` fueron eliminadas del dataset durante el preprocesamiento y no forman parte del modelo.

### Variables en `medical_conditions` (Condiciones Crónicas)

| Variable Dataset | Columna DB | Tipo | Notas |
|-----------------|------------|------|-------|
| HadAngina | had_angina | TINYINT(1) | Historial de angina |
| HadStroke | had_stroke | TINYINT(1) | Historial de derrame cerebral |
| HadAsthma | had_asthma | TINYINT(1) | Diagnóstico de asma |
| HadSkinCancer | had_skin_cancer | TINYINT(1) | Historial de cáncer de piel |
| HadCOPD | had_copd | TINYINT(1) | Diagnóstico de COPD |
| HadDepressiveDisorder | had_depressive_disorder | TINYINT(1) | Trastorno depresivo |
| HadKidneyDisease | had_kidney_disease | TINYINT(1) | Enfermedad renal |
| HadArthritis | had_arthritis | TINYINT(1) | Diagnóstico de artritis |
| HadDiabetes | had_diabetes | VARCHAR(50) | 'No', 'Yes', 'No, pre-diabetes or borderline diabetes', 'Yes, but only during pregnancy (female)' |
| DeafOrHardOfHearing | deaf_or_hard_of_hearing | TINYINT(1) | Dificultad auditiva |
| BlindOrVisionDifficulty | blind_or_vision_difficulty | TINYINT(1) | Dificultad visual |
| DifficultyConcentrating | difficulty_concentrating | TINYINT(1) | Dificultad para concentrarse |
| DifficultyWalking | difficulty_walking | TINYINT(1) | Dificultad para caminar |
| DifficultyDressingBathing | difficulty_dressing_bathing | TINYINT(1) | Dificultad para vestirse/bañarse |
| DifficultyErrands | difficulty_errands | TINYINT(1) | Dificultad para hacer mandados |

### Variables en `predictions` (Datos Variables + Resultados)

| Variable Dataset | Columna DB | Tipo | Notas |
|-----------------|------------|------|-------|
| WeightInKilograms | weight_kilograms | DECIMAL(5,2) | Peso actual (20-300 kg) |
| BMI | bmi | DECIMAL(5,2) | Calculado: weight / (height²) |
| GeneralHealth | general_health | VARCHAR(20) | Estado de salud general |
| PhysicalHealthDays | physical_health_days | INT | Días con mala salud física (0-30) |
| MentalHealthDays | mental_health_days | INT | Días con mala salud mental (0-30) |
| LastCheckupTime | last_checkup_time | VARCHAR(100) | Última revisión médica |
| PhysicalActivities | physical_activities | TINYINT(1) | Realiza actividad física |
| SleepHours | sleep_hours | DECIMAL(3,1) | Horas de sueño promedio (0-24) |
| SmokerStatus | smoker_status | VARCHAR(50) | Estado de fumador |
| ECigaretteUsage | ecigarette_usage | VARCHAR(100) | Uso de cigarrillos electrónicos |
| AlcoholDrinkers | alcohol_drinkers | TINYINT(1) | Consume alcohol |
| ChestScan | chest_scan | TINYINT(1) | Ha tenido TC/TAC de tórax |
| HIVTesting | hiv_testing | TINYINT(1) | Se ha hecho prueba de VIH |
| FluVaxLast12 | flu_vax_last_12 | TINYINT(1) | Vacuna de gripe último año |
| PneumoVaxEver | pneumo_vax_ever | TINYINT(1) | Vacuna de neumonía alguna vez |
| TetanusLast10Tdap | tetanus_last_10_tdap | VARCHAR(100) | Vacuna de tétanos últimos 10 años |
| HighRiskLastYear | high_risk_last_year | TINYINT(1) | Comportamiento de alto riesgo |
| CovidPos | covid_pos | VARCHAR(100) | 'Yes', 'No', 'Tested positive using home test without a health professional' |
| - | prediction_probability | DECIMAL(5,2) | RESULTADO: Probabilidad 0-100% |
| - | risk_level | VARCHAR(10) | RESULTADO: 'Low', 'Medium', 'High' |
| - | model_version | VARCHAR(50) | METADATA: Versión del modelo usado |

### Variable NO incluida (Target)

| Variable Dataset | Razón |
|-----------------|-------|
| HadHeartAttack | Variable TARGET — no se solicita al usuario, es lo que predecimos (codificada como 0/1 por LabelEncoder) |

## Flujo de Datos

### Para Usuario Registrado:

```
1. REGISTRO:
   ├─ users (email, password)
   ├─ user_profiles (datos demográficos)
   └─ medical_conditions (condiciones crónicas)

2. PREDICCIÓN:
   ├─ Cargar: user_profiles + medical_conditions
   ├─ Solicitar: datos variables (peso, salud actual, hábitos)
   ├─ Calcular: BMI automáticamente
   ├─ Preprocesar: OHE + StandardScaler (en backend, antes del modelo)
   ├─ Predecir: best_mlp_model.joblib
   └─ Guardar: predictions + prediction_explanations + recommendations
```

### Para Usuario No Registrado:

```
1. PREDICCIÓN:
   ├─ Solicitar: TODOS los datos (demográficos + condiciones + variables)
   ├─ Calcular: BMI automáticamente
   ├─ Preprocesar: OHE + StandardScaler (en backend, antes del modelo)
   ├─ Predecir: best_mlp_model.joblib
   └─ Guardar: predictions (con session_id, user_id = NULL)
```

## Queries Comunes (MySQL)

### 1. Obtener perfil completo de usuario para predicción

```sql
SELECT 
    up.sex, up.age_category, up.height_meters, up.removed_teeth,
    mc.had_angina, mc.had_stroke, mc.had_asthma, mc.had_copd,
    mc.had_skin_cancer, mc.had_depressive_disorder,
    mc.had_kidney_disease, mc.had_arthritis, mc.had_diabetes,
    mc.deaf_or_hard_of_hearing, mc.blind_or_vision_difficulty,
    mc.difficulty_concentrating, mc.difficulty_walking,
    mc.difficulty_dressing_bathing, mc.difficulty_errands
FROM user_profiles up
JOIN medical_conditions mc ON up.user_id = mc.user_id
WHERE up.user_id = ?;
```

### 2. Guardar predicción completa

```sql
-- Insertar predicción
INSERT INTO predictions (
    user_id, weight_kilograms, bmi, general_health,
    physical_health_days, mental_health_days, last_checkup_time,
    physical_activities, sleep_hours, smoker_status, ecigarette_usage,
    alcohol_drinkers, chest_scan, hiv_testing, flu_vax_last_12,
    pneumo_vax_ever, tetanus_last_10_tdap, high_risk_last_year, covid_pos,
    prediction_probability, risk_level, model_version
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

-- Insertar explicaciones (top N features)
INSERT INTO prediction_explanations (
    prediction_id, feature_name, feature_value, contribution_score, `rank`
) VALUES
    (LAST_INSERT_ID(), 'GeneralHealth', 'Poor', 0.234, 1),
    (LAST_INSERT_ID(), 'AgeCategory', 'Age 65 to 69', 0.189, 2),
    (LAST_INSERT_ID(), 'BMI', '32.5', 0.156, 3),
    (LAST_INSERT_ID(), 'SmokerStatus', 'Current smoker - now smokes every day', 0.142, 4),
    (LAST_INSERT_ID(), 'HadDiabetes', 'Yes', 0.098, 5);

-- Insertar recomendaciones
INSERT INTO recommendations (prediction_id, recommendation_text, category, priority)
VALUES
    (LAST_INSERT_ID(), 'Consulte con su médico lo antes posible...', 'Medical Consultation', 1),
    (LAST_INSERT_ID(), 'Considere un programa de cesación de tabaco...', 'Smoking Cessation', 2),
    (LAST_INSERT_ID(), 'Incorpore 30 minutos de actividad física...', 'Physical Activity', 3);
```

### 3. Obtener historial de predicciones

```sql
SELECT 
    p.id,
    p.prediction_probability,
    p.risk_level,
    p.prediction_timestamp,
    p.bmi,
    p.general_health,
    p.weight_kilograms
FROM predictions p
WHERE p.user_id = ?
ORDER BY p.prediction_timestamp DESC
LIMIT 10;
```

### 4. Obtener predicción completa con explicaciones

```sql
SELECT 
    p.*,
    JSON_ARRAYAGG(
        JSON_OBJECT(
            'feature', pe.feature_name,
            'value', pe.feature_value,
            'contribution', pe.contribution_score,
            'rank', pe.`rank`
        )
    ) AS explanations
FROM predictions p
LEFT JOIN prediction_explanations pe ON p.id = pe.prediction_id
WHERE p.id = ?
GROUP BY p.id;
```

## Validaciones Importantes

### Rangos Válidos

- `height_meters`: 0.5 - 2.5
- `weight_kilograms`: 20 - 300
- `bmi`: 10 - 100
- `sleep_hours`: 0 - 24
- `physical_health_days`: 0 - 30
- `mental_health_days`: 0 - 30
- `prediction_probability`: 0 - 100

### Valores Categóricos

Todos los campos categóricos tienen constraints ENUM o CHECK que validan los valores permitidos según el dataset preprocesado.

## Consideraciones de Performance

1. Índices creados:
   - `users.email` (búsqueda de login)
   - `predictions.user_id` (historial)
   - `predictions.prediction_timestamp` (ordenamiento)
   - `predictions.session_id` (usuarios no registrados)

2. Foreign Keys con CASCADE:
   - Al eliminar un usuario se eliminan automáticamente sus profiles, conditions y predictions

3. Triggers automáticos:
   - `updated_at` se actualiza automáticamente en users, user_profiles y medical_conditions

4. Motor de almacenamiento:
   - Todas las tablas usan InnoDB para soporte de transacciones y foreign keys

## Conexión a la Base de Datos (Ambiente de Pruebas)

Datos para conectarse desde DBeaver u otro cliente MySQL:

| Parámetro | Valor |
|-----------|-------|
| Host | heart-attack-db.c8b06ios85re.us-east-1.rds.amazonaws.com |
| Port | 3306 |
| Database | heart_attack_prediction |
| Username | root |
| Password | Root1234 |

En DBeaver: New Connection → MySQL → ingresar los datos anteriores → Test Connection → Finish.
