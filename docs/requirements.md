# Requirements Document: Sistema de Predicción de Riesgo de Ataque Cardíaco

## Introduction

Este documento especifica los requerimientos para un sistema web de predicción de riesgo de ataque cardíaco, desarrollado como proyecto de tesis de pregrado. El sistema utiliza machine learning para analizar datos médicos de pacientes y proporcionar una evaluación de riesgo que sirva como herramienta de apoyo para profesionales de la salud.

El sistema incorpora tres características innovadoras que lo diferencian:
1. **Explicabilidad mediante XAI**: Utiliza SHAP values para explicar qué factores contribuyen al riesgo calculado
2. **Categorización de riesgo**: Traduce porcentajes a categorías comprensibles (Bajo/Medio/Alto)
3. **Simulador What-If**: Permite a los usuarios simular cambios en hábitos modificables y ver el impacto potencial en su riesgo

El sistema está diseñado para ser desarrollado por dos estudiantes: uno enfocado en ML e infraestructura, y otro en backend y frontend. Este documento sirve como contrato entre ambos desarrolladores.

## Glossary

- **Sistema**: El sistema completo de predicción de riesgo de ataque cardíaco
- **Predictor_ML**: El componente de machine learning que calcula probabilidades de riesgo
- **API_Backend**: El servicio FastAPI que expone endpoints REST
- **Frontend_Web**: La aplicación Angular que presenta la interfaz de usuario
- **Base_Datos**: La base de datos PostgreSQL que almacena información de usuarios y predicciones
- **Usuario**: Paciente que utiliza el sistema para evaluar su riesgo
- **Médico**: Profesional de salud que utiliza los resultados como herramienta de apoyo
- **Predicción**: Resultado del análisis ML que incluye probabilidad de riesgo (0-100%)
- **Nivel_Riesgo**: Categorización del riesgo en Bajo (<30%), Medio (30-70%), Alto (>70%)
- **Feature_Importance**: Medida de la contribución de cada variable al resultado de predicción
- **SHAP_Values**: Valores SHapley Additive exPlanations que explican la contribución de cada característica
- **Datos_Médicos**: Información de salud del paciente requerida para la predicción
- **Historial**: Registro de predicciones anteriores de un usuario
- **Simulación_WhatIf**: Predicción hipotética basada en cambios en variables modificables del usuario
- **Variables_Modificables**: Características relacionadas con hábitos de vida que el usuario puede cambiar (peso, ejercicio, sueño, tabaco, alcohol)
- **Variables_Fijas**: Características demográficas y condiciones médicas permanentes que no cambian en simulaciones
- **Reporte_PDF**: Documento descargable con resultados de predicción para el médico
- **Dataset**: heart_2022_no_nans.csv con 39 columnas de datos médicos
- **XAI**: Explainable AI (Inteligencia Artificial Explicable) - técnicas para hacer transparente el modelo ML

## Requirements

### Requirement 1: Predicción de Riesgo con Machine Learning

**User Story:** Como usuario, quiero ingresar mis datos médicos y recibir una predicción de mi riesgo de ataque cardíaco, para poder tomar decisiones informadas sobre mi salud con mi médico.

#### Acceptance Criteria

1. WHEN el Usuario envía datos médicos completos, THE Predictor_ML SHALL calcular una probabilidad de riesgo entre 0% y 100%
2. WHEN el Predictor_ML procesa una solicitud, THE Sistema SHALL retornar el resultado en menos de 2 segundos
3. WHEN el Predictor_ML calcula el riesgo, THE Sistema SHALL categorizar el resultado en Bajo, Medio o Alto según los umbrales definidos
4. WHEN el modelo ML es entrenado, THE Predictor_ML SHALL utilizar el Dataset completo con las 39 columnas disponibles
5. WHEN el Predictor_ML genera una predicción, THE Sistema SHALL incluir un identificador único para trazabilidad

### Requirement 2: Registro de Usuario con Perfil Médico

**User Story:** Como paciente, quiero registrarme en el sistema proporcionando mi información médica básica, para no tener que ingresarla cada vez que haga una predicción.

#### Acceptance Criteria

1. WHEN un nuevo Usuario se registra, THE Sistema SHALL solicitar email, contraseña y datos demográficos (sexo, fecha de nacimiento, altura, raza/etnicidad)
2. WHEN un nuevo Usuario se registra, THE Sistema SHALL solicitar historial médico permanente (condiciones crónicas como diabetes, asma, COPD, etc.)
3. WHEN el Sistema valida el registro, THE API_Backend SHALL verificar que todos los datos demográficos estén en rangos médicos válidos
4. WHEN el Sistema guarda el registro, THE Base_Datos SHALL crear registros en tablas users, user_profiles y medical_conditions
5. WHEN el registro es exitoso, THE Sistema SHALL retornar confirmación y permitir acceso inmediato al sistema
6. WHEN el Usuario proporciona fecha de nacimiento, THE Sistema SHALL calcular y almacenar la categoría de edad según rangos del Dataset

### Requirement 3: Formulario Inteligente para Usuarios Registrados

**User Story:** Como usuario registrado, quiero completar un formulario corto que solo pregunte datos variables, para hacer predicciones rápidamente sin repetir información permanente.

#### Acceptance Criteria

1. WHEN un Usuario registrado inicia una predicción, THE Sistema SHALL cargar automáticamente datos demográficos y condiciones médicas permanentes desde Base_Datos
2. WHEN el Frontend_Web muestra el formulario para usuario registrado, THE Sistema SHALL solicitar únicamente datos variables (peso actual, salud general, días de mala salud física/mental, última revisión médica, actividad física, horas de sueño, estado de fumador, uso de cigarrillos electrónicos, consumo de alcohol, vacunas recientes, COVID-19)
3. WHEN el Usuario registrado completa el formulario, THE Sistema SHALL requerir aproximadamente 15-20 campos variables
4. WHEN el Usuario ingresa un valor en un campo, THE Frontend_Web SHALL validar que esté dentro del rango médico válido antes de permitir el envío
5. WHEN el Usuario deja un campo obligatorio vacío, THE Frontend_Web SHALL prevenir el envío y mostrar un mensaje de error claro
6. WHEN el formulario se carga, THE Frontend_Web SHALL mostrar ayuda contextual para cada campo médico

### Requirement 4: Formulario Completo para Usuarios No Registrados

**User Story:** Como visitante sin cuenta, quiero realizar una predicción de riesgo cardíaco sin necesidad de crear una cuenta, para evaluar mi riesgo de forma rápida y anónima.

#### Acceptance Criteria

1. WHEN un Usuario no registrado inicia una predicción, THE Frontend_Web SHALL mostrar un formulario completo con todos los campos necesarios (demográficos + historial médico + datos variables)
2. WHEN el Usuario no registrado completa el formulario, THE Sistema SHALL requerir aproximadamente 35-40 campos totales
3. WHEN el Sistema procesa la predicción de usuario no registrado, THE Base_Datos SHALL almacenar la predicción con user_id NULL y un session_id temporal
4. WHEN el Sistema genera resultados para usuario no registrado, THE Frontend_Web SHALL ofrecer opción de crear cuenta para guardar el resultado
5. WHEN el Usuario ingresa datos en el formulario completo, THE Frontend_Web SHALL validar todos los campos según rangos médicos válidos
6. WHEN el formulario completo se carga, THE Frontend_Web SHALL organizar campos en secciones lógicas (Información Personal, Historial Médico, Salud Actual)

### Requirement 5: Validación de Datos Médicos

**User Story:** Como desarrollador del sistema, quiero validar que todos los datos médicos estén dentro de rangos clínicamente válidos, para garantizar predicciones confiables y prevenir errores.

#### Acceptance Criteria

1. WHEN el API_Backend recibe datos de entrada, THE Sistema SHALL validar que BMI esté entre 10 y 100
2. WHEN el API_Backend recibe datos de entrada, THE Sistema SHALL validar que SleepHours esté entre 0 y 24
3. WHEN el API_Backend recibe datos de entrada, THE Sistema SHALL validar que HeightInMeters esté entre 0.5 y 2.5
4. WHEN el API_Backend recibe datos de entrada, THE Sistema SHALL validar que WeightInKilograms esté entre 20 y 300
5. WHEN el API_Backend recibe datos de entrada, THE Sistema SHALL validar que PhysicalHealthDays y MentalHealthDays estén entre 0 y 30
6. WHEN el API_Backend detecta un valor fuera de rango, THE Sistema SHALL retornar un error HTTP 400 con detalles específicos del campo inválido
7. WHEN el API_Backend recibe variables categóricas, THE Sistema SHALL validar que los valores pertenezcan al conjunto permitido del Dataset

### Requirement 6: Visualización de Resultados

**User Story:** Como usuario, quiero ver mis resultados de forma clara y visual, para entender fácilmente mi nivel de riesgo sin necesitar conocimientos técnicos.

#### Acceptance Criteria

1. WHEN el Sistema calcula una predicción, THE Frontend_Web SHALL mostrar el porcentaje de riesgo con un indicador visual tipo semáforo
2. WHEN el nivel de riesgo es Bajo, THE Frontend_Web SHALL mostrar el indicador en color verde
3. WHEN el nivel de riesgo es Medio, THE Frontend_Web SHALL mostrar el indicador en color amarillo
4. WHEN el nivel de riesgo es Alto, THE Frontend_Web SHALL mostrar el indicador en color rojo
5. WHEN el Frontend_Web muestra resultados, THE Sistema SHALL incluir un mensaje interpretativo apropiado para cada nivel de riesgo
6. WHEN el Frontend_Web presenta resultados, THE Sistema SHALL mostrar la fecha y hora de la predicción

### Requirement 7: Gestión de Historial Personal

**User Story:** Como usuario, quiero ver mis predicciones anteriores, para poder monitorear cambios en mi riesgo a lo largo del tiempo.

#### Acceptance Criteria

1. WHEN el Usuario solicita su historial, THE API_Backend SHALL retornar todas las predicciones ordenadas por fecha descendente
2. WHEN el Sistema guarda una predicción, THE Base_Datos SHALL almacenar el resultado, fecha, hora y datos de entrada utilizados
3. WHEN el Usuario visualiza su historial, THE Frontend_Web SHALL mostrar una lista con fecha, nivel de riesgo y porcentaje de cada predicción
4. WHEN el Usuario selecciona una predicción del historial, THE Frontend_Web SHALL mostrar los detalles completos de esa evaluación
5. WHEN el Sistema almacena predicciones, THE Base_Datos SHALL asociar cada predicción con el identificador único del Usuario

### Requirement 8: Explicabilidad del Modelo con XAI

**User Story:** Como usuario, quiero entender qué factores están influyendo en mi resultado mediante visualizaciones explicativas, para saber en qué aspectos de mi salud debo enfocarme y tomar decisiones informadas.

#### Acceptance Criteria

1. WHEN el Predictor_ML genera una predicción, THE Sistema SHALL calcular la contribución de cada variable al resultado final utilizando SHAP (SHapley Additive exPlanations)
2. WHEN el Frontend_Web muestra resultados, THE Sistema SHALL presentar los 5 factores que más contribuyen al riesgo calculado ordenados por importancia
3. WHEN el Sistema presenta factores de riesgo, THE Frontend_Web SHALL mostrar si cada factor aumenta o disminuye el riesgo con indicadores visuales (flechas arriba/abajo o colores)
4. WHEN el Sistema calcula contribuciones SHAP, THE Predictor_ML SHALL generar valores SHAP para cada característica de entrada del modelo
5. WHEN el Frontend_Web muestra factores, THE Sistema SHALL presentar valores en lenguaje comprensible para usuarios no técnicos (ej: "Fumar aumenta tu riesgo en 15%")
6. WHEN el Sistema genera explicaciones, THE API_Backend SHALL incluir tanto el valor SHAP numérico como una descripción textual interpretable
7. WHEN el Usuario visualiza explicaciones, THE Frontend_Web SHALL mostrar gráficos de barras horizontales con los factores principales y su impacto relativo

### Requirement 9: Recomendaciones de Prevención

**User Story:** Como usuario, quiero recibir recomendaciones básicas de prevención, para tener orientación sobre acciones que puedo tomar para reducir mi riesgo.

#### Acceptance Criteria

1. WHEN el Sistema identifica factores de riesgo modificables, THE Sistema SHALL generar recomendaciones específicas basadas en esos factores
2. WHEN el nivel de riesgo es Alto, THE Sistema SHALL incluir una recomendación prioritaria de consultar con un médico
3. WHEN el Sistema genera recomendaciones, THE Frontend_Web SHALL presentar entre 3 y 5 sugerencias accionables
4. WHEN el Sistema detecta factores como SmokerStatus positivo, THE Sistema SHALL incluir recomendaciones relacionadas con cesación de tabaco
5. WHEN el Sistema detecta BMI fuera de rango saludable, THE Sistema SHALL incluir recomendaciones sobre actividad física y nutrición

### Requirement 10: Simulador de Escenarios "What-If"

**User Story:** Como usuario, quiero simular cambios en mis hábitos modificables y ver cómo afectarían mi riesgo de ataque cardíaco, para motivarme a realizar cambios positivos en mi estilo de vida y entender el impacto potencial de mis decisiones.

#### Acceptance Criteria

1. WHEN el Usuario visualiza sus resultados de predicción, THE Frontend_Web SHALL mostrar un botón o sección "Simular Cambios" que permita acceder al simulador
2. WHEN el Usuario accede al simulador, THE Sistema SHALL identificar y presentar únicamente variables modificables relacionadas con hábitos de vida (peso, actividad física, horas de sueño, estado de fumador, consumo de alcohol, salud general percibida)
3. WHEN el Usuario accede al simulador, THE Frontend_Web SHALL cargar los valores actuales de la predicción original como punto de partida
4. WHEN el Usuario modifica una variable en el simulador, THE Frontend_Web SHALL permitir ajustar el valor usando controles intuitivos (sliders, dropdowns, toggles)
5. WHEN el Usuario modifica variables en el simulador, THE Sistema SHALL mantener fijas las variables no modificables (edad, sexo, condiciones médicas crónicas, historial de enfermedades)
6. WHEN el Usuario solicita calcular el nuevo escenario, THE API_Backend SHALL generar una nueva predicción usando los valores modificados y los valores fijos originales
7. WHEN el Sistema calcula el escenario simulado, THE Frontend_Web SHALL mostrar el nuevo porcentaje de riesgo y su categoría (Bajo/Medio/Alto) junto al resultado original para comparación
8. WHEN el Sistema presenta resultados del simulador, THE Frontend_Web SHALL mostrar visualmente la diferencia entre el riesgo original y el simulado (ej: "Tu riesgo disminuiría de 65% a 42%")
9. WHEN el Sistema presenta resultados del simulador, THE Frontend_Web SHALL utilizar indicadores visuales claros (flechas, colores, gráficos comparativos) para mostrar si el riesgo aumenta o disminuye
10. WHEN el Usuario realiza múltiples simulaciones, THE Sistema SHALL permitir resetear los valores a los originales con un botón "Restaurar valores originales"
11. WHEN el Usuario realiza una simulación, THE Sistema SHALL calcular y mostrar qué variables modificadas tuvieron mayor impacto en el cambio de riesgo
12. WHEN el Sistema calcula simulaciones, THE API_Backend SHALL retornar resultados en tiempo real SIN persistir en Base_Datos (las simulaciones son exploratorias y temporales)

#### Variables Modificables para Simulación

Las siguientes variables pueden ser ajustadas en el simulador:
- **WeightInKilograms** (20-300 kg) → Afecta BMI automáticamente
- **PhysicalActivities** (Sí/No)
- **SleepHours** (0-24 horas)
- **SmokerStatus** (Never smoked / Former smoker / Current smoker - now smokes some days / Current smoker - now smokes every day)
- **ECigaretteUsage** (Never used / Use them some days / Use them every day / Not at all (right now))
- **AlcoholDrinkers** (Sí/No)
- **GeneralHealth** (Excellent / Very good / Good / Fair / Poor)
- **PhysicalHealthDays** (0-30 días)
- **MentalHealthDays** (0-30 días)

#### Variables NO Modificables (Fijas)

Las siguientes variables permanecen constantes en simulaciones:
- Datos demográficos: Sex, AgeCategory, State, RaceEthnicityCategory, HeightInMeters
- Condiciones médicas crónicas: HadAngina, HadStroke, HadAsthma, HadCOPD, HadSkinCancer, HadDepressiveDisorder, HadKidneyDisease, HadArthritis, HadDiabetes
- Condiciones físicas permanentes: DeafOrHardOfHearing, BlindOrVisionDifficulty, DifficultyConcentrating, DifficultyWalking, DifficultyDressingBathing, DifficultyErrands
- Historial médico: RemovedTeeth, LastCheckupTime, ChestScan, HIVTesting, FluVaxLast12, PneumoVaxEver, TetanusLast10Tdap, HighRiskLastYear, CovidPos

### Requirement 11: Exportación de Reporte PDF

**User Story:** Como usuario, quiero descargar un reporte en PDF de mi evaluación, para poder llevarlo a mi consulta médica y discutirlo con mi doctor.

#### Acceptance Criteria

1. WHEN el Usuario solicita exportar resultados, THE API_Backend SHALL generar un documento PDF con la información completa de la predicción
2. WHEN el Sistema genera el PDF, THE Reporte_PDF SHALL incluir el porcentaje de riesgo, nivel, fecha y datos de entrada utilizados
3. WHEN el Sistema genera el PDF, THE Reporte_PDF SHALL incluir los factores principales que contribuyen al resultado
4. WHEN el Sistema genera el PDF, THE Reporte_PDF SHALL incluir las recomendaciones de prevención generadas
5. WHEN el Sistema genera el PDF, THE Reporte_PDF SHALL incluir un disclaimer indicando que es una herramienta de apoyo y no reemplaza diagnóstico médico
6. WHEN el Usuario descarga el PDF, THE Frontend_Web SHALL iniciar la descarga con un nombre de archivo descriptivo que incluya la fecha

### Requirement 12: Autenticación y Gestión de Usuarios

**User Story:** Como usuario, quiero crear una cuenta y acceder de forma segura, para que mis datos médicos estén protegidos y solo yo pueda verlos.

#### Acceptance Criteria

1. WHEN un nuevo Usuario se registra, THE API_Backend SHALL crear una cuenta con email y contraseña hasheada
2. WHEN un Usuario intenta iniciar sesión, THE API_Backend SHALL validar credenciales y retornar un token JWT válido por 24 horas
3. WHEN un Usuario accede a endpoints protegidos, THE API_Backend SHALL validar el token JWT antes de procesar la solicitud
4. WHEN un token JWT expira, THE Sistema SHALL retornar error HTTP 401 y requerir nuevo inicio de sesión
5. WHEN un Usuario se registra, THE Sistema SHALL validar que el email tenga formato válido y no esté duplicado
6. WHEN un Usuario crea una contraseña, THE Sistema SHALL requerir mínimo 8 caracteres con al menos una letra y un número

### Requirement 13: Persistencia de Datos

**User Story:** Como desarrollador del sistema, quiero almacenar de forma estructurada usuarios y predicciones, para garantizar integridad y trazabilidad de los datos.

#### Acceptance Criteria

1. WHEN el Sistema almacena datos, THE Base_Datos SHALL utilizar PostgreSQL como motor de base de datos
2. WHEN el Sistema guarda un Usuario, THE Base_Datos SHALL crear registros en tres tablas: users (autenticación), user_profiles (demográficos) y medical_conditions (condiciones crónicas)
3. WHEN el Sistema guarda una Predicción, THE Base_Datos SHALL almacenar en predictions: id, user_id (nullable), session_id, datos variables, prediction_probability, risk_level, model_version, prediction_timestamp
4. WHEN el Sistema guarda explicaciones, THE Base_Datos SHALL almacenar en prediction_explanations los top 5 factores con mayor contribución (SHAP values)
5. WHEN el Sistema genera recomendaciones, THE Base_Datos SHALL almacenar en recommendations entre 3-5 sugerencias con categoría y prioridad
6. WHEN el Sistema guarda una Predicción, THE Base_Datos SHALL mantener integridad referencial mediante foreign keys con CASCADE delete
7. WHEN el Sistema consulta predicciones, THE Base_Datos SHALL utilizar índices en user_id, session_id y prediction_timestamp para optimizar consultas
8. WHEN el Sistema almacena contraseñas, THE Base_Datos SHALL almacenar solo password_hash, nunca contraseñas en texto plano

#### Database Schema

**Tabla: users**
```sql
- id (UUID, PK)
- email (VARCHAR, UNIQUE, NOT NULL)
- password_hash (VARCHAR, NOT NULL)
- is_active (BOOLEAN, DEFAULT TRUE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- last_login (TIMESTAMP)
```

**Tabla: user_profiles**
```sql
- id (UUID, PK)
- user_id (UUID, FK → users.id, UNIQUE)
- state (VARCHAR) -- Estado de residencia
- sex (VARCHAR: 'Male'|'Female')
- birth_date (DATE)
- age_category (VARCHAR) -- Calculado desde birth_date
- height_meters (DECIMAL: 0.5-2.5)
- race_ethnicity_category (VARCHAR)
- removed_teeth (VARCHAR: 'None of them'|'1 to 5'|'6 or more, but not all'|'All')
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

**Tabla: medical_conditions**
```sql
- id (UUID, PK)
- user_id (UUID, FK → users.id, UNIQUE)
- had_angina (BOOLEAN)
- had_stroke (BOOLEAN)
- had_asthma (BOOLEAN)
- had_copd (BOOLEAN)
- had_skin_cancer (BOOLEAN)
- had_depressive_disorder (BOOLEAN)
- had_kidney_disease (BOOLEAN)
- had_arthritis (BOOLEAN)
- had_diabetes (VARCHAR: 'No'|'Yes'|'No, pre-diabetes...'|'Yes, but only during pregnancy...')
- deaf_or_hard_of_hearing (BOOLEAN)
- blind_or_vision_difficulty (BOOLEAN)
- difficulty_concentrating (BOOLEAN)
- difficulty_walking (BOOLEAN)
- difficulty_dressing_bathing (BOOLEAN)
- difficulty_errands (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

**Tabla: predictions**
```sql
- id (UUID, PK)
- user_id (UUID, FK → users.id, NULLABLE)
- session_id (VARCHAR, para usuarios no registrados)
- weight_kilograms (DECIMAL: 20-300)
- bmi (DECIMAL: 10-100, calculado)
- general_health (VARCHAR: 'Excellent'|'Very good'|'Good'|'Fair'|'Poor')
- physical_health_days (INTEGER: 0-30)
- mental_health_days (INTEGER: 0-30)
- last_checkup_time (VARCHAR)
- physical_activities (BOOLEAN)
- sleep_hours (DECIMAL: 0-24)
- smoker_status (VARCHAR)
- ecigarette_usage (VARCHAR)
- alcohol_drinkers (BOOLEAN)
- chest_scan (BOOLEAN)
- hiv_testing (BOOLEAN)
- flu_vax_last_12 (BOOLEAN)
- pneumo_vax_ever (BOOLEAN)
- tetanus_last_10_tdap (VARCHAR)
- high_risk_last_year (BOOLEAN)
- covid_pos (VARCHAR: 'Yes'|'No'|'Tested positive using home test...')
- prediction_probability (DECIMAL: 0-100)
- risk_level (VARCHAR: 'Low'|'Medium'|'High')
- model_version (VARCHAR)
- prediction_timestamp (TIMESTAMP)
- CONSTRAINT: (user_id IS NOT NULL AND session_id IS NULL) OR (user_id IS NULL AND session_id IS NOT NULL)
```

**Tabla: prediction_explanations**
```sql
- id (UUID, PK)
- prediction_id (UUID, FK → predictions.id)
- feature_name (VARCHAR)
- feature_value (TEXT)
- contribution_score (DECIMAL) -- SHAP value
- rank (INTEGER: 1-5)
- created_at (TIMESTAMP)
```

**Tabla: recommendations**
```sql
- id (UUID, PK)
- prediction_id (UUID, FK → predictions.id)
- recommendation_text (TEXT)
- category (VARCHAR: 'Medical Consultation'|'Lifestyle'|'Nutrition'|'Physical Activity'|'Smoking Cessation'|'Stress Management'|'Preventive Care')
- priority (INTEGER: 1-5)
- created_at (TIMESTAMP)
```

### Requirement 14: API REST con Contratos Definidos

**User Story:** Como desarrollador frontend, quiero consumir una API REST bien documentada con contratos claros, para integrar fácilmente el backend con el frontend.

#### Acceptance Criteria

1. WHEN el API_Backend expone endpoints, THE Sistema SHALL seguir convenciones REST para métodos HTTP y rutas
2. WHEN el API_Backend retorna respuestas, THE Sistema SHALL utilizar códigos de estado HTTP apropiados (200, 201, 400, 401, 404, 500)
3. WHEN el API_Backend recibe requests, THE Sistema SHALL validar schemas de entrada usando Pydantic models
4. WHEN el API_Backend retorna errores, THE Sistema SHALL incluir mensajes descriptivos en formato JSON consistente
5. WHEN el API_Backend expone endpoints, THE Sistema SHALL generar documentación automática OpenAPI/Swagger
6. WHEN el API_Backend procesa requests, THE Sistema SHALL incluir CORS headers para permitir requests desde el Frontend_Web

### Requirement 15: Entrenamiento y Versionado del Modelo ML

**User Story:** Como desarrollador de ML, quiero entrenar y versionar modelos de forma reproducible, para poder mejorar el sistema y mantener trazabilidad de versiones.

#### Acceptance Criteria

1. WHEN el Predictor_ML entrena un modelo, THE Sistema SHALL utilizar el Dataset heart_2022_no_nans.csv como fuente de datos
2. WHEN el Predictor_ML entrena un modelo, THE Sistema SHALL dividir datos en train (70%), validation (15%) y test (15%)
3. WHEN el Predictor_ML entrena un modelo, THE Sistema SHALL evaluar métricas de accuracy, precision, recall, F1-score y AUC-ROC
4. WHEN el Predictor_ML guarda un modelo, THE Sistema SHALL serializar el modelo entrenado en formato pickle o joblib
5. WHEN el Predictor_ML versiona un modelo, THE Sistema SHALL incluir metadata con fecha, métricas de evaluación y hiperparámetros utilizados
6. WHEN el API_Backend carga el modelo, THE Sistema SHALL utilizar la versión más reciente disponible en el directorio de modelos

### Requirement 16: Infraestructura Cloud en AWS

**User Story:** Como desarrollador de infraestructura, quiero desplegar el sistema en AWS usando IaC, para garantizar reproducibilidad y escalabilidad del ambiente productivo.

#### Acceptance Criteria

1. WHEN el Sistema se despliega, THE infraestructura SHALL utilizar AWS ECS Fargate para ejecutar contenedores del API_Backend
2. WHEN el Sistema se despliega, THE infraestructura SHALL utilizar AWS RDS PostgreSQL para la Base_Datos
3. WHEN el Sistema se despliega, THE infraestructura SHALL utilizar AWS Application Load Balancer para distribuir tráfico
4. WHEN el Sistema se despliega, THE infraestructura SHALL utilizar AWS S3 para almacenar modelos ML y archivos estáticos del Frontend_Web
5. WHEN el Sistema se despliega, THE infraestructura SHALL definir todos los recursos usando AWS CDK en Python
6. WHEN el Sistema se despliega, THE infraestructura SHALL configurar security groups para permitir solo tráfico HTTPS en puerto 443
7. WHEN el Sistema se despliega, THE infraestructura SHALL configurar auto-scaling para el ECS service basado en CPU y memoria

### Requirement 17: Disponibilidad y Monitoreo

**User Story:** Como administrador del sistema, quiero monitorear la salud y disponibilidad del sistema, para detectar y resolver problemas proactivamente.

#### Acceptance Criteria

1. WHEN el Sistema está en producción, THE infraestructura SHALL mantener disponibilidad de 99% uptime mensual
2. WHEN el API_Backend está ejecutándose, THE Sistema SHALL exponer un endpoint /health que retorne status 200 si está saludable
3. WHEN el Load Balancer verifica salud, THE infraestructura SHALL realizar health checks cada 30 segundos al endpoint /health
4. WHEN un contenedor falla health checks, THE infraestructura SHALL reemplazarlo automáticamente con uno nuevo
5. WHEN el Sistema procesa requests, THE API_Backend SHALL registrar logs estructurados con nivel, timestamp y mensaje
6. WHEN el Sistema genera logs, THE infraestructura SHALL enviar logs a AWS CloudWatch para análisis y alertas

### Requirement 18: Seguridad de Datos Médicos

**User Story:** Como responsable del sistema, quiero implementar medidas de seguridad para datos médicos sensibles, para cumplir con buenas prácticas de protección de información de salud.

#### Acceptance Criteria

1. WHEN el Sistema transmite datos, THE infraestructura SHALL utilizar HTTPS/TLS para todas las comunicaciones
2. WHEN el Sistema almacena contraseñas, THE API_Backend SHALL utilizar bcrypt con salt para hashear contraseñas
3. WHEN el Sistema almacena datos médicos, THE Base_Datos SHALL encriptar datos en reposo usando AWS RDS encryption
4. WHEN el Sistema procesa datos médicos, THE API_Backend SHALL no registrar información sensible en logs
5. WHEN el Sistema expone la API, THE infraestructura SHALL implementar rate limiting para prevenir abuso
6. WHEN el Sistema maneja errores, THE API_Backend SHALL no exponer detalles internos de implementación en mensajes de error

### Requirement 19: Experiencia de Usuario en Frontend

**User Story:** Como usuario sin conocimientos técnicos, quiero una interfaz intuitiva y responsiva, para poder usar el sistema fácilmente desde cualquier dispositivo.

#### Acceptance Criteria

1. WHEN el Usuario accede al sistema, THE Frontend_Web SHALL utilizar Angular Material para componentes de UI consistentes
2. WHEN el Usuario navega en el sistema, THE Frontend_Web SHALL ser responsivo y funcionar en dispositivos móviles, tablets y desktop
3. WHEN el Usuario interactúa con formularios, THE Frontend_Web SHALL mostrar feedback visual inmediato de validación
4. WHEN el Sistema procesa una predicción, THE Frontend_Web SHALL mostrar un indicador de carga mientras espera respuesta
5. WHEN el Sistema retorna un error, THE Frontend_Web SHALL mostrar mensajes de error amigables sin jerga técnica
6. WHEN el Usuario navega entre secciones, THE Frontend_Web SHALL mantener estado de sesión y no requerir re-autenticación innecesaria

### Requirement 20: Pipeline de Preprocesamiento de Datos

**User Story:** Como desarrollador de ML, quiero un pipeline reproducible de preprocesamiento, para garantizar que datos de entrada sean transformados consistentemente entre entrenamiento y predicción.

#### Acceptance Criteria

1. WHEN el Predictor_ML preprocesa datos, THE Sistema SHALL aplicar las mismas transformaciones usadas durante entrenamiento
2. WHEN el Predictor_ML procesa variables categóricas, THE Sistema SHALL aplicar encoding consistente (one-hot o label encoding)
3. WHEN el Predictor_ML procesa variables numéricas, THE Sistema SHALL aplicar normalización o estandarización según lo definido en entrenamiento
4. WHEN el Predictor_ML maneja valores faltantes, THE Sistema SHALL aplicar estrategia de imputación definida (media, mediana o moda)
5. WHEN el Predictor_ML guarda el pipeline, THE Sistema SHALL serializar transformadores junto con el modelo para garantizar consistencia
6. WHEN el API_Backend recibe datos para predicción, THE Sistema SHALL aplicar el pipeline de preprocesamiento antes de invocar el modelo

### Requirement 21: Testing y Calidad de Código

**User Story:** Como desarrollador del sistema, quiero implementar tests automatizados, para garantizar calidad y prevenir regresiones en el código.

#### Acceptance Criteria

1. WHEN el código del API_Backend se desarrolla, THE Sistema SHALL incluir unit tests para funciones de validación y lógica de negocio
2. WHEN el código del Predictor_ML se desarrolla, THE Sistema SHALL incluir tests para verificar que predicciones estén en rango 0-100%
3. WHEN el código se integra, THE Sistema SHALL ejecutar tests automatizados en CI/CD pipeline antes de desplegar
4. WHEN el código del Frontend_Web se desarrolla, THE Sistema SHALL incluir tests unitarios para componentes críticos
5. WHEN el API_Backend se prueba, THE Sistema SHALL incluir integration tests para endpoints principales
6. WHEN el código se escribe, THE Sistema SHALL mantener cobertura de tests mínima de 70% para backend y ML

