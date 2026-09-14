# 🚗 Análisis de Hurto de Vehículos en Colombia

> **Proyecto de Minería de Datos**  
> Integración, limpieza, transformación y análisis del parque automotor, hurtos y recuperaciones de vehículos en Colombia.

---

## 📌 1. Descripción del proyecto

Este proyecto desarrolla un proceso de **minería de datos aplicado al análisis del hurto de vehículos en Colombia**, integrando información proveniente de tres fuentes principales:

- 🏢 **RUNT:** parque automotor registrado.
- 🚔 **Policía Nacional:** vehículos recuperados.
- ⚠️ **Registros de hurto:** denuncias de vehículos hurtados.

El objetivo es construir un **dataset único, limpio y validado**, organizado por:

> **Año × Municipio × Tipo de vehículo**

Esta estructura permite posteriormente realizar análisis estadísticos, identificar patrones geográficos y temporales y estudiar el comportamiento de los hurtos y recuperaciones frente al parque automotor registrado.

---

# 🎯 2. Objetivo

### Objetivo general

Construir un dataset integrado que permita analizar el comportamiento del **hurto y recuperación de vehículos en Colombia**, relacionando estas variables con el parque automotor registrado por municipio, año y tipo de vehículo.

### Objetivos específicos

- 🧹 Limpiar y estandarizar los datasets originales.
- 📅 Normalizar las fechas y obtener el año correspondiente.
- 📍 Homologar departamentos y municipios.
- 🗺️ Asignar códigos DANE a los municipios.
- 🚗 Clasificar los vehículos en **AUTOMOTOR** y **MOTOCICLETA**.
- 🔗 Integrar las tres fuentes mediante una clave común.
- ✅ Validar la calidad del dataset resultante.
- 📊 Identificar valores atípicos mediante el método IQR.
- 📈 Generar una base preparada para futuros análisis de minería de datos.

---

# 📂 3. Fuentes de datos

Los archivos originales se encuentran en:

```text
datasets/originales/
```

| Dataset | Fuente / descripción | Información principal |
|---|---|---|
| 🚘 `CrecimientoParqueAutomotor.csv` | RUNT | Departamento, municipio, estado, clase, año y vehículos registrados |
| 🚨 `HurtoVehiculos.csv` | Registros de hurto | Tipo de delito, departamento, municipio, fecha y cantidad |
| 👮 `RecuperacionPoliciaNacional.csv` | Policía Nacional | Departamento, municipio, código DANE, clase de bien, fecha y cantidad |

---

# 🏗️ 4. Arquitectura del proyecto

El proyecto está organizado separando los **datos originales, datos limpios, datos procesados y resultados finales**.

```text
ANALISIS-HURTO-VEHICULOS/
│
├── 📁 codigo/
│   ├── 🐍 main.py
│   ├── 🐍 library.py
│   └── 🐍 limpieza.py
│
├── 📁 datasets/
│   │
│   ├── 📥 originales/
│   │   ├── CrecimientoParqueAutomotor.csv
│   │   ├── HurtoVehiculos.csv
│   │   └── RecuperacionPoliciaNacional.csv
│   │
│   ├── 🧹 limpios/
│   │   ├── *_limpio.csv
│   │   └── bitacora_limpieza.csv
│   │
│   ├── ⚙️ procesados/
│   │   └── *_procesado.csv
│   │
│   └── 📊 resultados/
│       ├── dataset_final.csv
│       ├── correspondencia_municipios.csv
│       ├── clases_runt_no_mapeadas.csv
│       └── validacion_final.csv
│
└── 📄 README.md
```

### 🔎 Función de cada módulo

| Archivo | Responsabilidad |
|---|---|
| `main.py` | 🎛️ Orquesta y ejecuta todo el proceso |
| `library.py` | 🧰 Contiene funciones auxiliares, clasificadores y validadores |
| `limpieza.py` | 🧹 Realiza la limpieza de cada fuente y genera la bitácora |

---

# 🔄 5. Flujo del proceso de minería de datos

El procesamiento completo sigue un flujo ETL:

```text
📥 DATOS ORIGINALES
        │
        ▼
🧹 LIMPIEZA
        │
        ├── Eliminación de duplicados
        ├── Normalización de textos
        ├── Conversión de fechas
        └── Conversión de cantidades
        │
        ▼
⚙️ PREPARACIÓN
        │
        ├── Extracción del año
        ├── Normalización geográfica
        └── Clasificación del vehículo
        │
        ▼
🗺️ CORRESPONDENCIA DANE
        │
        ▼
📍 ASIGNACIÓN DE DANE AL RUNT
        │
        ▼
📊 AGREGACIÓN
        │
        ▼
🔗 INTEGRACIÓN DE DATASETS
        │
        ▼
✅ VALIDACIÓN
        │
        ▼
📈 DIAGNÓSTICO
        │
        ▼
🎯 DATASET FINAL
```

---

# 🧹 6. Etapa de limpieza

La primera etapa consiste en preparar los datos para garantizar consistencia entre las diferentes fuentes.

### Procesos aplicados

**1. Eliminación de duplicados**

Se identifican y eliminan registros repetidos.

**2. Normalización de texto**

Los campos de texto se estandarizan:

```text
minúsculas → MAYÚSCULAS
tildes → eliminadas
espacios innecesarios → eliminados
```

Por ejemplo:

```text
"Bogotá"
"BOGOTA"
"bogotá"
```

se normalizan como:

```text
BOGOTA
```

**3. Conversión de fechas**

Las fechas se transforman a un formato estándar para facilitar la extracción del año.

**4. Conversión de cantidades**

Los valores numéricos se convierten al tipo de dato correspondiente.

**5. Filtrado del RUNT**

Para el parque automotor se conservan únicamente los registros cuyo estado sea:

```text
ACTIVO
```

### 📝 Bitácora

Cada transformación queda registrada en:

```text
datasets/limpios/bitacora_limpieza.csv
```

Esto permite realizar **trazabilidad del proceso de limpieza**.

---

# ⚙️ 7. Preparación de los datos

Una vez realizada la limpieza, los datos se transforman para que las tres fuentes puedan trabajar bajo una estructura común.

### Variables principales generadas

| Variable | Descripción |
|---|---|
| `AÑO` | Año del registro |
| `DEPARTAMENTO` | Departamento normalizado |
| `MUNICIPIO` | Municipio normalizado |
| `CODIGO_DANE_MUNICIPIO` | Código geográfico DANE |
| `TIPO_VEHICULO` | AUTOMOTOR / MOTOCICLETA |
| `CANTIDAD` | Número de vehículos |

---

# 🚗 8. Clasificación de vehículos

Para facilitar la integración se establece una clasificación general:

```text
                 VEHÍCULOS
                     │
          ┌──────────┴──────────┐
          │                     │
     AUTOMOTOR             MOTOCICLETA
```

El clasificador analiza las clases de vehículo presentes en el RUNT y determina a cuál de las dos categorías pertenece cada registro.

Las clases que no pueden ser clasificadas automáticamente se conservan en:

```text
clases_runt_no_mapeadas.csv
```

Esto permite **no perder información y mantener trazabilidad sobre los registros que requieren revisión**.

---

# 🗺️ 9. Correspondencia geográfica

Uno de los puntos importantes del proyecto es lograr que las diferentes fuentes utilicen una misma referencia geográfica.

Para esto se construye una correspondencia:

```text
CÓDIGO DANE
     │
     ├── Departamento
     │
     └── Municipio
```

El resultado se almacena en:

```text
datasets/resultados/correspondencia_municipios.csv
```

Posteriormente, esta correspondencia permite asignar el código DANE al dataset del RUNT.

---

# 📊 10. Agregación

Los registros se agrupan utilizando una clave común:

```text
AÑO
+
CODIGO_DANE_MUNICIPIO
+
TIPO_VEHICULO
```

Por ejemplo:

| Año | DANE | Tipo | Registrados | Hurtados | Recuperados |
|---:|---:|---|---:|---:|---:|
| 2024 | 730001 | AUTOMOTOR | ... | ... | ... |
| 2024 | 730001 | MOTOCICLETA | ... | ... | ... |
| 2024 | 730026 | AUTOMOTOR | ... | ... | ... |

De esta manera, cada fila representa una combinación única de:

> **un año + un municipio + un tipo de vehículo**

---

# 🔗 11. Integración de las fuentes

Los tres datasets son integrados mediante un **`outer join`**, utilizando como clave:

```text
AÑO
CODIGO_DANE_MUNICIPIO
TIPO_VEHICULO
```

El uso de `outer join` permite conservar información aunque una combinación determinada exista únicamente en una de las fuentes.

Conceptualmente:

```text
       🚘 RUNT
          │
          │
          ├──────────┐
          │          │
          ▼          ▼
       🚨 HURTOS   👮 RECUPERACIONES
          │          │
          └────┬─────┘
               │
               ▼
        📊 DATASET FINAL
```

---

# ✅ 12. Validación del dataset

Después de la integración se ejecutan diferentes controles de calidad.

### Validaciones realizadas

| Validación | Resultado |
|---|---|
| 🔍 Valores nulos | ✅ 0 |
| ♻️ Registros duplicados | ✅ 0 |
| 🔑 Claves | ✅ Validadas |
| 🚗 Tipos de vehículo | ✅ Validados |
| 🗺️ Códigos DANE | ✅ Validados |
| 📏 Formato de DANE | ✅ 5 dígitos |

El resultado completo queda registrado en:

```text
datasets/resultados/validacion_final.csv
```

---

# 📈 13. Resultados del procesamiento

La última ejecución produjo:

## 📊 Dataset final

| Indicador | Resultado |
|---|---:|
| 📄 Filas | **48.602** |
| 📋 Columnas | **8** |
| 🗺️ Departamentos | **33** |
| 📍 Municipios | **1.005** |
| ❌ Nulos | **0** |
| ♻️ Duplicados | **0** |
| 🔢 Códigos DANE válidos | **100%** |

### 🚗 Distribución por tipo de vehículo

```text
AUTOMOTOR
25.282 registros
██████████████████████████

MOTOCICLETA
23.320 registros
████████████████████████
```

| Tipo de vehículo | Registros | Participación |
|---|---:|---:|
| 🚘 AUTOMOTOR | 25.282 | 52,0% |
| 🏍️ MOTOCICLETA | 23.320 | 48,0% |
| **Total** | **48.602** | **100%** |

---

# 📌 14. Detección de valores atípicos

Se aplicó el método estadístico **IQR (Rango Intercuartílico)** para identificar posibles valores atípicos.

> ⚠️ Los valores detectados **no fueron eliminados automáticamente**, ya que un valor extremo en este contexto puede representar una situación real, como un municipio con una cantidad significativamente mayor de vehículos, hurtos o recuperaciones.

### Resultados

| Variable | Valores atípicos |
|---|---:|
| 🚘 Registrados | **8.551** |
| 🚨 Hurtados | **6.851** |
| 👮 Recuperados | **6.799** |

La detección de estos valores se utiliza como mecanismo de **diagnóstico y control de calidad**, no como criterio automático de eliminación.

---

# 📤 15. Productos generados

| Archivo | Propósito |
|---|---|
| 📝 `bitacora_limpieza.csv` | Registro de las transformaciones realizadas |
| 🧹 `*_limpio.csv` | Datos limpios de cada fuente |
| ⚙️ `*_procesado.csv` | Datos preparados para integración |
| 🎯 `dataset_final.csv` | Dataset consolidado |
| 🗺️ `correspondencia_municipios.csv` | Relación DANE → municipio/departamento |
| ⚠️ `clases_runt_no_mapeadas.csv` | Clases RUNT pendientes de clasificación |
| ✅ `validacion_final.csv` | Resultados de los controles de calidad |

---

# ⚠️ 16. Consideraciones sobre las clases RUNT

Durante la clasificación se identificaron algunas clases de vehículos que no pueden asignarse automáticamente a las categorías definidas.

Entre ellas pueden encontrarse registros como:

```text
TRACTOCAMION
MOTOCARRO
SEMI...
```

Estos registros **no deben eliminarse sin análisis previo**, porque podrían contener información relevante para el estudio.

Por esta razón se generan de manera independiente en:

```text
clases_runt_no_mapeadas.csv
```

Esto permite realizar posteriormente una **revisión y ampliación del clasificador**.

---

# 🧠 17. Valor del dataset construido

El principal resultado del proyecto no es solamente la limpieza de los archivos originales, sino la construcción de una **fuente de datos integrada y consistente**.

El dataset final permite relacionar:

```text
       🗓️ AÑO
          +
       📍 MUNICIPIO
          +
       🚗 VEHÍCULO
          │
          ▼
 ┌───────────────────────┐
 │ VEHÍCULOS REGISTRADOS │
 │ VEHÍCULOS HURTADOS    │
 │ VEHÍCULOS RECUPERADOS │
 └───────────────────────┘
```

Esto deja preparada la información para futuras etapas de:

- 📊 análisis exploratorio de datos;
- 📈 visualización de tendencias;
- 🗺️ análisis geográfico;
- 🔎 identificación de patrones;
- 🤖 modelos de minería de datos;
- 📉 análisis de comportamiento de los hurtos;
- 🎯 generación de indicadores.

---

# ▶️ 18. Ejecución

### Requisitos

- Python **3.9 o superior**
- Pandas

### Ejecución del proyecto

Desde la carpeta `codigo`:

```bash
cd codigo
python3 main.py
```

El programa ejecuta de forma secuencial:

```text
Limpieza
   ↓
Preparación
   ↓
Correspondencia geográfica
   ↓
Asignación DANE
   ↓
Agregación
   ↓
Integración
   ↓
Validación
   ↓
Diagnóstico
```

---

# 🏁 19. Conclusión

El proyecto permite transformar tres fuentes de información independientes y con estructuras diferentes en un **dataset integrado, estandarizado y validado**, utilizando como unidad de análisis la combinación **año × municipio × tipo de vehículo**.

El resultado final cuenta con **48.602 registros, 8 variables, 33 departamentos y 1.005 municipios**, sin valores nulos ni duplicados y con el **100 % de los códigos DANE validados**.

Además, el proceso conserva una bitácora de limpieza y archivos auxiliares que permiten identificar transformaciones, registros no clasificados y posibles valores atípicos, fortaleciendo la **trazabilidad, reproducibilidad y calidad del proceso de minería de datos**.

---

# 📁 20. Estructura recomendada para el repositorio

Para mantener una organización profesional, se recomienda la siguiente estructura:

```text
📦 ANALISIS-HURTO-VEHICULOS
│
├── 📁 codigo
│   ├── main.py
│   ├── library.py
│   └── limpieza.py
│
├── 📁 datasets
│   ├── 📥 originales
│   ├── 🧹 limpios
│   ├── ⚙️ procesados
│   └── 📊 resultados
│
├── 📁 docs
│   ├── arquitectura.png
│   ├── flujo_proceso.png
│   └── diccionario_datos.md
│
├── 📁 notebooks
│   └── analisis_exploratorio.ipynb
│
├── 📄 README.md
├── 📄 requirements.txt
└── 📄 .gitignore
```

### 🏷️ Tecnologías y conceptos

`Python` · `Pandas` · `ETL` · `Minería de Datos` · `Limpieza de Datos` · `Integración de Datos` · `IQR` · `RUNT` · `DANE` · `Policía Nacional`
