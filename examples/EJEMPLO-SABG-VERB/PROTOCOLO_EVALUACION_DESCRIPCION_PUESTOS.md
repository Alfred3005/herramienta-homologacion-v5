# PROTOCOLO DE EVALUACIÓN DE DESCRIPCIÓN DE PUESTOS
## Análisis Semántico Normativo + Validación Jerárquica

**Versión:** 1.0  
**Fecha de Creación:** 7 de noviembre de 2025  
**Clasificación:** Metodología Transferible a LLMs  
**Autor:** Desarrollador Senior  
**Público:** Equipos técnicos, especialistas de RH, LLMs

---

## I. PROPÓSITO Y ALCANCE

### A. Propósito General

Este protocolo establece un **procedimiento sistemático y replicable** para evaluar descripciones de puestos en organizaciones públicas mexicanas contra:

1. **Marco normativo** (Leyes, Reglamentos, Decretos)
2. **Matriz de verbos autorizados** (Estructura jerárquica)
3. **Alineación semántica** (Correspondencia de significados)
4. **Estructura funcional** (Formato VERBO+COMPLEMENTO+RESULTADO)

### B. Aplicabilidad

✅ Puestos de Dirección General o equivalente  
✅ Instituciones públicas federales mexicanas  
✅ Evaluaciones pre-aprobación de descripción/perfil de puestos  
✅ Validación de atribuciones delegadas  

### C. Umbral de Aprobación

**Versión 1.0:** 95% funciones conformes (máximo 5% no conformes)  
**Versión 1.1 (Permisiva):** 50% funciones conformes (mínimo 50% no conformes = rechazo)

---

## II. PREPARACIÓN PREVIA (FASE 0)

### Paso 0.1: Recopilación de Documentos Base

**Documentos OBLIGATORIOS a obtener:**

| Documento | Prioridad | Descripción | Uso |
|-----------|-----------|-------------|-----|
| Descripción del Puesto | 🔴 CRÍTICA | Documento bajo evaluación | Comparación función por función |
| Reglamento Interior | 🔴 CRÍTICA | Marco legal de la institución | Extracción de atribuciones |
| Matriz de Verbos | 🔴 CRÍTICA | Guía de verbos por nivel jerárquico | Validación de cada verbo |
| Manual de Descripción | 🟡 IMPORTANTE | Instructivo de formato | Validación de estructura |
| Ley Orgánica | 🟡 IMPORTANTE | Ley de creación de la institución | Contexto general |

**Acciones concretas:**
```
□ Obtener documento PDF/TXT de descripción
□ Extraer artículos relevantes del Reglamento Interior
□ Identificar matriz de verbos (típicamente en anexos)
□ Guardar copia local de cada documento
□ Crear carpeta de trabajo con todos los archivos
```

### Paso 0.2: Definir el Nivel Jerárquico del Puesto

**Información ESENCIAL a determinar:**

```
Pregunta 1: ¿Cuál es el nivel jerárquico exacto?
Respuestas posibles: Dirección General, Subdirección, Jefatura de Departamento, etc.

Pregunta 2: ¿En qué grupo salarial está clasificado?
Ejemplo: G11 = Secretario de Estado (Dirección General)

Pregunta 3: ¿Es de libre designación, carrera o gabinete?
Esto afecta las atribuciones que puede tener.

Pregunta 4: ¿Existe una entidad superior o es máximo nivel en su área?
Define si tiene poder de decisión o solo recomendación.
```

**Acción operativa:**
```python
# Crear matriz de contexto del puesto
contexto_puesto = {
    "nombre": "SECRETARIA(O) ANTICORRUPCION Y BUEN GOBIERNO",
    "nivel_jerarquico": "Dirección General",
    "grupo_salarial": "G11",
    "caracteristica": "Designación Directa",
    "superior_inmediato": "Presidente Federal",
    "dependientes_directos": 2652,
    "entidad_superior": "Ejecutivo Federal"
}
```

### Paso 0.3: Definir la Estructura de Evaluación

**Crear matriz de decisión:**

```
ESTRUCTURA BASE DE EVALUACIÓN:

Para cada FUNCIÓN se evaluará:
├─ Verbo (¿está autorizado?)
├─ Fuente Normativa (¿hay respaldo legal?)
├─ Estructura (¿cumple VERBO+COMPLEMENTO+RESULTADO?)
├─ Correspondencia Semántica (¿significado alínea?)
├─ Alineación Jerárquica (¿corresponde al nivel?)
└─ Veredicto (✅ APROBADO / ❌ RECHAZADO / 🟡 OBSERVACIÓN)
```

---

## III. FASE 1: EXTRACCIÓN DE MARCO NORMATIVO

### Paso 1.1: Identificar Atribuciones Indelegables (Fuente Primaria)

**Objetivo:** Encontrar las atribuciones originarias del puesto en la ley/reglamento

**Procedimiento:**

```
PASO 1: Localizar el artículo que describe atribuciones del Secretario
   └─ Típicamente llamado "Artículo [N]. El Secretario tiene las atribuciones siguientes:"

PASO 2: Extraer TODOS los incisos (I, II, III, ... hasta final)
   └─ Copiar textualmente cada inciso
   └─ Guardar en documento separado

PASO 3: Numerar y catalogar cada atribución
   └─ Atribución 1: [texto completo inciso I]
   └─ Atribución 2: [texto completo inciso II]
   └─ ... hasta completar
```

**Ejemplo de resultado esperado:**

```
ATRIBUCIONES INDELEGABLES DEL SECRETARIO (Art. 6)
=================================================

Atribución 1 (Inc. I): "Elaborar y conducir las políticas públicas 
competencia de la Secretaría"

Atribución 2 (Inc. II): "Acordar con la persona titular del Ejecutivo 
Federal los asuntos relevantes de la Secretaría"

Atribución 3 (Inc. III): "Desempeñar las comisiones y funciones 
especiales que la persona titular del Ejecutivo Federal le confiera..."

[... continuar hasta completar todos los incisos]
```

**Nota técnica:** En México, estas atribuciones suelen estar en:
- Artículos 6-15 del Reglamento Interior (típico)
- Pueden incluir atribuciones delegables en artículos posteriores
- **CRÍTICO:** Distinguir entre "indelegables" y "delegables"

### Paso 1.2: Crear Matriz de Correspondencia Normativa

**Objetivo:** Mapear qué atribuciones del Reglamento se cubren en la descripción

**Procedimiento:**

```
Crear tabla de 3 columnas:

| Atribución Normativa (Art. 6) | Función Descrita | ¿Corresponde? |
|-------------------------------|------------------|--------------|
| I - Elaborar políticas        | Función 1        | ✅ SÍ       |
| II - Acordar con Presidente   | [Buscar]         | 🟡 NO CLARO |
| III - Desempeñar comisiones   | Función 7        | ✅ SÍ       |
| ... continuar con todos       |                  |              |
```

**Acción:**
- Revisar CADA atribución normativa
- Buscar si existe función descrita que le corresponda
- Si no existe: NOTA como "COBERTURA INCOMPLETA"

### Paso 1.3: Identificar Atribuciones Delegables (Fuente Secundaria)

**Objetivo:** Entender qué funciones pueden estar delegadas legalmente

**Procedimiento:**

```
BÚSQUEDA PATTERN:

1. Localizar artículos de SUBSECRETARIOS u DIRECTORES
   └─ Típicamente: "Artículo [N]. La Subsecretaría tiene..."
   └─ O: "Artículo [N]. La Dirección General tiene..."

2. Extraer atribuciones similares a las del Secretario
   └─ Si Subsecretario "emite políticas", es delegación del Secretario
   └─ Si Subsecretario "propone cambios", Secretario aprueba

3. Catalogar qué se PUEDE DELEGAR
   └─ Esto define el "espacio de autoridad real" del Secretario
```

**Resultado esperado:**

```
ATRIBUCIONES DELEGABLES (pueden estar en descripción como delegadas):

├─ Emisión de políticas (delegable a Subsecretarios)
├─ Propuestas de iniciativas (delegable a Coordinadores)
├─ Ejecución de acciones (delegable a Directores)
└─ [... completar según normativa específica]

ATRIBUCIONES NO DELEGABLES (DEBEN estar en descripción):

├─ Designar nivel inmediato inferior
├─ Refrendar normas presidenciales
├─ Resolver recursos administrativos
└─ [... completar según Art. 6]
```

---

## IV. FASE 2: CONSTRUCCIÓN DE MATRIZ DE VERBOS

### Paso 2.1: Extraer Matriz de Verbos Autorizados por Nivel

**Objetivo:** Obtener lista oficial de verbos permitidos para el nivel jerárquico

**Procedimiento:**

```
PASO 1: Localizar documento "Relación de Verbos por Nivel Jerárquico"
        └─ Típicamente en: Anexo de Manual de Descripción

PASO 2: Identificar la columna del nivel del puesto
        └─ Buscar: "DIRECCIÓN GENERAL"
        └─ O equivalente en la institución

PASO 3: Extraer TODOS los verbos listados
        └─ Copiar completo

PASO 4: Eliminar duplicados y crear lista limpia

PASO 5: Guardar como referencia permanente
```

**Formato de resultado:**

```
VERBOS AUTORIZADOS PARA DIRECCIÓN GENERAL
============================================

Nivel 1 (Verbos más comunes):
- ACREDITAR
- ASESORAR
- AUTORIZAR
- CONDUCIR
- EMITIR
- ESTABLECER
- EVALUAR
- INFORMAR
- [... continuar lista completa]

Total de verbos autorizados: [N]
```

### Paso 2.2: Identificar Verbos NO Autorizados que Requieren Excepción

**Objetivo:** Reconocer verbos fuera de matriz que podrían tener respaldo normativo directo

**Procedimiento:**

```
PASO 1: Durante evaluación de funciones, si encuentras un verbo 
        NO en la matriz, PAUSA

PASO 2: Busca ese verbo en el Reglamento Interior
        └─ Ctrl+F: "[VERBO] la persona titular de la Secretaría"
        └─ Ejemplo: "REFRENDAR la persona titular"

PASO 3: Si encuentras respaldo → Es EXCEPCIÓN VÁLIDA
        └─ Documenta: "Art. [N], Inc. [X] autoriza REFRENDAR"

PASO 4: Si NO encuentras respaldo → Es VIOLACIÓN
        └─ Marca como: "VERBO NO AUTORIZADO, SIN RESPALDO NORMATIVO"
```

**Ejemplos de excepciones válidas (típicas en puestos de Secretario):**

```
├─ REFRENDAR → Art. 6, Inc. XI (Refrendar decretos presidenciales)
├─ RESOLVER → Art. 6, Inc. XIV (Resolver recursos administrativos)
├─ DESIGNAR → Art. 6, Inc. V, VI, VII (Designar funcionarios)
└─ [... documentar según institución]
```

### Paso 2.3: Crear Matriz Maestra de Verbos

**Objetivo:** Documento de referencia única para toda la evaluación

```
MATRIZ MAESTRA DE VERBOS - PUESTO: SECRETARIO

┌─────────────────────────────────────────────────┐
│ VERBOS AUTORIZADOS (Matriz Oficial)             │
├─────────────────────────────────────────────────┤
│ ✅ ACREDITAR, ASESORAR, AUTORIZAR, ...          │
│ Total: 26 verbos                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ EXCEPCIONES CON RESPALDO NORMATIVO              │
├─────────────────────────────────────────────────┤
│ 🟡 REFRENDAR → Art. 6, Inc. XI                  │
│ 🟡 RESOLVER → Art. 6, Inc. XIV                  │
│ 🟡 DESIGNAR → Art. 6, Inc. V, VI, VII           │
│ Total: 3 excepciones                            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ VERBOS PROHIBIDOS (No autorizados)              │
├─────────────────────────────────────────────────┤
│ ❌ ENCOMENDAR (verbo operacional)               │
│ ❌ INTERPRETAR (típicamente jurídico delegado)  │
│ ❌ EJECUTAR (verbo de nivel operacional)        │
│ Total: [N] verbos                               │
└─────────────────────────────────────────────────┘
```

---

## V. FASE 3: ANÁLISIS SEMÁNTICO (EL CORAZÓN DEL PROTOCOLO)

### Paso 3.1: Metodología de Análisis Semántico

**Objetivo:** Comparar SIGNIFICADOS no solo palabras

**Este es el paso diferenciador que usan LLMs inteligentemente**

#### Substep 3.1.1: Extracción de Núcleo Semántico

Para CADA función descrita, extraer su **significado esencial**:

```
EJEMPLO - Función 1: "Emitir las políticas, de conformidad con los 
objetivos, estrategias y prioridades del Plan Nacional de Desarrollo..."

ANÁLISIS SEMÁNTICO:
├─ Verbo: EMITIR
├─ Significado del verbo: "Poner en circulación, hacer público, producir normas"
├─ Objeto: "políticas"
├─ Contexto: "de conformidad con objetivos, estrategias, prioridades"
├─ Resultado: "dar atención a fiscalización, control, auditoría"
└─ NÚCLEO SEMÁNTICO: "Crear y comunicar directrices de política pública 
                      para la fiscalización y control interno"
```

#### Substep 3.1.2: Extracción de Núcleo Normativo

Para CADA atribución normativa, extraer su **significado esencial**:

```
EJEMPLO - Art. 6, Inc. I: "Elaborar y conducir las políticas públicas 
competencia de la Secretaría"

ANÁLISIS SEMÁNTICO:
├─ Verbos: ELABORAR, CONDUCIR
├─ Significado: "Crear y dirigir la orientación de políticas públicas"
├─ Alcance: "de la Secretaría"
├─ Implicación: "Liderazgo en definición de política pública"
└─ NÚCLEO NORMATIVO: "Responsable de crear, comunicar y dirigir las 
                      políticas públicas bajo su competencia"
```

#### Substep 3.1.3: Comparación de Núcleos

```
PREGUNTA CLAVE: ¿El NÚCLEO SEMÁNTICO (función descrita) 
                CORRESPONDE al NÚCLEO NORMATIVO (atribución)?

NÚCLEO SEMÁNTICO:  "Crear y comunicar directrices de política pública 
                    para fiscalización y control interno"

NÚCLEO NORMATIVO:  "Responsable de crear, comunicar y dirigir políticas 
                    públicas bajo su competencia"

RESULTADO: ✅ ALINEACIÓN = Los significados esenciales coinciden
```

### Paso 3.2: Análisis de Variantes Semánticas

**Objetivo:** Entender que un mismo concepto puede expresarse de múltiples formas

#### Tabla de Equivalencias Semánticas

```
┌─────────────────────────────┬────────────────────────────────────┐
│ CONCEPTO BASE               │ VARIANTES SEMÁNTICAMENTE VÁLIDAS   │
├─────────────────────────────┼────────────────────────────────────┤
│ Creación de normas          │ • Emitir normas                    │
│                             │ • Expedir disposiciones            │
│                             │ • Establecer reglas                │
│                             │ • Crear políticas                  │
├─────────────────────────────┼────────────────────────────────────┤
│ Validación de documentos    │ • Aprobar documentos               │
│                             │ • Autorizar proyectos              │
│                             │ • Validar iniciativas              │
├─────────────────────────────┼────────────────────────────────────┤
│ Dirección de personas       │ • Conducir                         │
│                             │ • Dirigir                          │
│                             │ • Ordenar (en contexto)            │
│                             │ • ❌ NO: Encomendar (delegación)   │
├─────────────────────────────┼────────────────────────────────────┤
│ Representación legal        │ • Representar                      │
│                             │ • Fungir en nombre de              │
│                             │ • Actuar en representación de      │
└─────────────────────────────┴────────────────────────────────────┘
```

**Cómo usar esta tabla:**

```
Si encuentras verbo que no reconoces, PREGÚNTATE:
1. ¿Cuál es el concepto base de lo que hace?
2. ¿Está ese concepto en la tabla?
3. Si SÍ → Es variante válida
4. Si NO → Requiere búsqueda adicional o es rechazable
```

### Paso 3.3: Evaluación de Contexto Semántico

**Objetivo:** Entender que el significado depende también del CONTEXTO

```
PRINCIPIO: Un verbo puede ser apropiado o inapropiado según contexto

EJEMPLO - Verbo ENCOMENDAR:

En contexto operacional bajo:
  "Encomendar a un empleado que compile datos"
  → Válido, es delegación apropiada

En contexto de Dirección General:
  "Encomendar la ejecución de acciones de competencia del Secretario"
  → INVÁLIDO, debe ser "ORDENAR" (mandato de autoridad)

REGLA SEMÁNTICA: La autoridad debe usar verbos de MANDATO, 
                 no de PETICIÓN
```

---

## VI. FASE 4: EVALUACIÓN FUNCIÓN POR FUNCIÓN

### Paso 4.1: Estructura de Evaluación de Una Función

**Para CADA función descrita, aplicar sistemáticamente:**

```
TEMPLATE DE EVALUACIÓN POR FUNCIÓN:

┌──────────────────────────────────────────────────────────┐
│ FUNCIÓN [N]: [Nombre resumido]                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ TEXTO COMPLETO:                                          │
│ "[Texto completo de la función según documento]"         │
│                                                           │
│ CRITERIO 1: VERBO                                        │
│ ├─ Verbo extraído: [VERBO IDENTIFICADO]                 │
│ ├─ ¿Está en matriz autorizada?: ✅ SÍ / ❌ NO          │
│ ├─ Si NO: ¿Tiene respaldo normativo?: ✅ SÍ / ❌ NO    │
│ └─ Veredicto parcial: [✅/❌/🟡]                         │
│                                                           │
│ CRITERIO 2: FUENTE NORMATIVA                             │
│ ├─ Artículo correspondiente: [Art. X, Inc. Y]           │
│ ├─ Texto normativo: "[Cita exacta]"                     │
│ ├─ ¿Hay correspondencia?: ✅ DIRECTA / 🟡 INDIRECTA     │
│ └─ Veredicto parcial: [✅/❌/🟡]                         │
│                                                           │
│ CRITERIO 3: ESTRUCTURA (VERBO+COMPLEMENTO+RESULTADO)    │
│ ├─ Verbo: [✅/❌/🟡]                                     │
│ ├─ Complemento: [✅/❌/🟡]                               │
│ ├─ Resultado: [✅/❌/🟡]                                 │
│ └─ Veredicto parcial: [✅/❌/🟡]                         │
│                                                           │
│ CRITERIO 4: CORRESPONDENCIA SEMÁNTICA                    │
│ ├─ Núcleo semántico: "[Significado esencial]"           │
│ ├─ Núcleo normativo: "[Significado normativo]"          │
│ ├─ ¿Hay alineación?: ✅ SÍ / 🟡 PARCIAL / ❌ NO        │
│ └─ Veredicto parcial: [✅/❌/🟡]                         │
│                                                           │
│ CRITERIO 5: ALINEACIÓN JERÁRQUICA                        │
│ ├─ ¿Corresponde al nivel?: ✅ SÍ / ❌ NO                │
│ ├─ ¿Hay inversión jerárquica?: ✅ NO / ❌ SÍ            │
│ ├─ Nota: [Explicación si aplica]                        │
│ └─ Veredicto parcial: [✅/❌/🟡]                         │
│                                                           │
│ VEREDICTO FINAL:                                         │
│ ├─ Resultado: [✅ APROBADO / ❌ RECHAZADO / 🟡 OBS.]    │
│ ├─ Justificación: [1-2 párrafos]                        │
│ ├─ Recomendación: [Si aplica corrección]                │
│ └─ Prioridad: [CRÍTICA / IMPORTANTE / MENOR]            │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Paso 4.2: Criterios de Decisión por Criterio

#### Criterio 1: VERBO

```
ÁRBOL DE DECISIÓN:

¿Está en matriz autorizada?
├─ SÍ → ✅ APROBADO
└─ NO → ¿Tiene respaldo normativo directo?
    ├─ SÍ (encontrado en Art. 6 u equivalente) → 🟡 EXCEPCIÓN VÁLIDA
    └─ NO → ❌ RECHAZADO - VERBO NO AUTORIZADO

UMBRAL DE APROBACIÓN: 
- ✅ + 🟡 = ACEPTABLE para continuar análisis
- ❌ = FALLO CRÍTICO (pero sigue evaluando otros criterios)
```

#### Criterio 2: FUENTE NORMATIVA

```
ÁRBOL DE DECISIÓN:

¿Existe artículo normativo que respalda esta función?
├─ SÍ, DIRECTO (mismo texto, mismo concepto) → ✅ CORRESPONDENCIA DIRECTA
├─ SÍ, INDIRECTO (mismo concepto, palabras diferentes) → 🟡 CORRESPONDENCIA SEMÁNTICA
├─ SÍ, LEJANO (concepto relacionado pero no claro) → 🟡 REQUIERE ANÁLISIS PROFUNDO
└─ NO (no existe en normativa) → ❌ SIN RESPALDO

UMBRAL:
- ✅ + 🟡 (directo/semántico) = ACEPTABLE
- 🟡 (lejano) = REQUIERE REVISIÓN MANUAL
- ❌ = POTENCIAL RECHAZO (a menos que sea cobertura de Art. final - "demás")
```

#### Criterio 3: ESTRUCTURA

```
VALIDACIÓN DE COMPONENTES:

VERBO: ¿Hay verbo de acción explícito?
└─ ✅ SÍ / ❌ NO

COMPLEMENTO: ¿Hay objeto directo claro (qué, a quién)?
└─ ✅ CLARO / 🟡 IMPLÍCITO / ❌ AUSENTE

RESULTADO: ¿Hay resultado o propósito explícito (para qué)?
└─ ✅ EXPLÍCITO / 🟡 IMPLÍCITO / ❌ AUSENTE

DECISIÓN:
├─ Todos 3 ✅ → ✅ ESTRUCTURA COMPLETA
├─ 2 ✅ + 1 🟡 → ✅ ESTRUCTURA ACEPTABLE
├─ 1 ✅ + 2 🟡 → 🟡 ESTRUCTURA MEJORABLE
└─ Cualquier ❌ → 🟡 REQUIERE REDACCIÓN

NOTA: Estructura débil no es fallo automático si normativa es débil también
```

#### Criterio 4: CORRESPONDENCIA SEMÁNTICA

```
METODOLOGÍA:

1. EXTRAER NÚCLEO SEMÁNTICO DE FUNCIÓN DESCRITA
   "¿Cuál es el significado esencial en 1 línea?"
   
2. EXTRAER NÚCLEO NORMATIVO DE ATRIBUCIÓN
   "¿Cuál es el significado esencial en 1 línea?"
   
3. COMPARAR NÚCLEOS
   ├─ ¿Son equivalentes? → ✅ DIRECTA
   ├─ ¿Hay superposición clara? → 🟡 SEMÁNTICA (válida)
   ├─ ¿Hay superposición débil? → 🟡 REQUIERE ANÁLISIS
   └─ ¿Son distintos? → ❌ SIN CORRESPONDENCIA

EJEMPLO DE ANÁLISIS:

Función: "Emitir los procedimientos para la recopilación de información..."
Núcleo: "Crear normas de procedimiento administrativo"

Normativa Art. 6, Inc. XX: "Expedir disposiciones, reglas, normas..."
Núcleo: "Crear y distribuir normas de carácter general"

Comparación: Emitir procedimientos = Expedir normas
Resultado: ✅ CORRESPONDENCIA SEMÁNTICA DIRECTA
```

#### Criterio 5: ALINEACIÓN JERÁRQUICA

```
EVALUACIÓN:

PREGUNTA 1: ¿Esta función corresponde al nivel del puesto?
├─ Nivel DG debe: Crear política, tomar decisiones estratégicas
├─ Nivel DG NO debe: Tareas operacionales, ejecución
└─ Aplicar: ¿La función es estratégica o operacional?

PREGUNTA 2: ¿Hay inversión de jerarquía?
├─ Inversión = El Secretario hace tareas de nivel inferior
├─ Síntomas: "Interpretar normas" (tarea jurídica), "Ejecutar" (operacional)
└─ Resultado: ❌ RECHAZO si hay inversión clara

PREGUNTA 3: ¿Hay delegación impropia?
├─ Delegación impropia = Función debería estar en nivel superior
├─ Síntomas: "Proponer [lo que debería ordenar]"
└─ Análisis: ¿Debería ser orden en lugar de propuesta?

ÁRBOL:
Si hay inversión clara → ❌ RECHAZAR INMEDIATAMENTE
Si hay delegación impropia → 🟡 REQUIERE REDEFINICIÓN
Si está al nivel correcto → ✅ ACEPTAR
```

### Paso 4.3: Matriz de Decisión Final por Función

```
TABLA CONSOLIDADA (Aplicar para cada función):

┌─────────┬──────────┬──────────────┬───────────┬──────────┬──────────┐
│ Criterio│ Resultado│ Ponderación  │ Puntuación│ Resultado│ Acción   │
├─────────┼──────────┼──────────────┼───────────┼──────────┼──────────┤
│ Verbo   │ ✅/❌/🟡│ 25%          │ [0-1]     │ [0-0.25] │ Validar  │
│ Normativa│✅/❌/🟡│ 25%          │ [0-1]     │ [0-0.25] │ Validar  │
│ Estruct.│ ✅/❌/🟡│ 20%          │ [0-1]     │ [0-0.20] │ Validar  │
│ Semántica│✅/❌/🟡│ 20%          │ [0-1]     │ [0-0.20] │ Validar  │
│ Jerárquica│✅/❌/🟡│ 10%          │ [0-1]     │ [0-0.10] │ Validar  │
├─────────┼──────────┼──────────────┼───────────┼──────────┼──────────┤
│ TOTAL   │ [PROMEDIO]│ 100%        │ [0-1.0]   │ [Score]  │ Decidir  │
└─────────┴──────────┴──────────────┴───────────┴──────────┴──────────┘

INTERPRETACIÓN DE SCORE FINAL:

0.85 - 1.0 → ✅ APROBADO (función conforme)
0.60 - 0.84 → 🟡 OBSERVACIÓN (requiere corrección menor)
0.40 - 0.59 → 🟡 REQUIERE CORRECCIÓN (error moderado)
0.00 - 0.39 → ❌ RECHAZADO (error crítico)

IMPORTANTE: Un ❌ en Jerárquica puede anular función completa
            independientemente de otros criterios.
```

---

## VII. FASE 5: CONSOLIDACIÓN Y DECISIÓN FINAL

### Paso 5.1: Matriz Consolidada de Todas las Funciones

```
TABLA MAESTRA - TODAS LAS FUNCIONES:

┌──┬─────────────────┬──────┬────────┬──────────┬────────┬───────────┐
│#│ Función         │Verbo │Normativ│Semántica │Jerárqu │Veredicto  │
├──┼─────────────────┼──────┼────────┼──────────┼────────┼───────────┤
│1 │ Políticas       │✅    │✅      │✅        │✅      │✅ APROBADO│
│2 │ Presupuesto     │✅    │🟡      │🟡        │❌      │❌ RECHAZAR│
│3 │ Iniciativas     │✅    │✅      │✅        │✅      │✅ APROBADO│
│4 │ Encomendar      │❌    │🟡      │❌        │❌      │❌ RECHAZAR│
│5 │ Designar        │🟡    │✅      │✅        │✅      │✅ APROBADO│
│[…]                                                               │
│20│ Apertura        │✅    │✅      │✅        │✅      │✅ APROBADO│
├──┼─────────────────┼──────┼────────┼──────────┼────────┼───────────┤
│  │ TOTALES         │      │        │          │        │           │
│  │ Aprobadas: 16   │      │        │          │        │ 80%       │
│  │ Rechazadas: 3   │      │        │          │        │ 15%       │
│  │ Observadas: 1   │      │        │          │        │ 5%        │
└──┴─────────────────┴──────┴────────┴──────────┴────────┴───────────┘
```

### Paso 5.2: Cálculo del Porcentaje de Conformidad

```
FÓRMULA:

Conformidad (%) = (Funciones Aprobadas / Total Funciones) × 100

DESGLOSE:

Funciones Aprobadas     = 16
Funciones Rechazadas    = 3
Funciones Observadas    = 1
─────────────────────────────
TOTAL                   = 20

Conformidad = (16/20) × 100 = 80%

CLASIFICACIÓN DE FUNCIONES PROBLEMÁTICAS:

Rechazadas              = 3
Observadas (correcciones menores) = 1
─────────────────────────────
TOTAL CON PROBLEMAS     = 4 (20%)

Porcentaje de Errores   = (3/20) × 100 = 15%
```

### Paso 5.3: Aplicación del Umbral de Aprobación

```
VERSIÓN 1.0 (Estricta):
─────────────────────────
Umbral: 95% funciones conformes (máximo 5% no conformes)
Función Ejemplo: 80% conformes = ❌ NO APROBADO
Razón: 20% > 5% permitido

VERSIÓN 1.1 (Permisiva - USAR PARA ESTA EVALUACIÓN):
───────────────────────────────────
Umbral: 50% funciones conformes (mínimo 50% no conformes para rechazo)
Función Ejemplo: 80% conformes = ✅ APROBADO CON CORRECCIONES MENORES
Razón: 20% < 50% permitido

MATRIZ DE DECISIÓN POR UMBRAL:

Conformidad | Umbral 1.0 (95%) | Umbral 1.1 (50%) | Interpretación
─────────────────────────────────────────────────────────────────
100%        | ✅ APROBADO      | ✅ APROBADO      | Perfecto
90-99%      | 🟡 REVISAR       | ✅ APROBADO      | Muy conforme
80-89%      | ❌ RECHAZAR      | ✅ APROBADO      | Conforme con correcciones
50-79%      | ❌ RECHAZAR      | ✅ APROBADO      | En zona roja, pero supera 50%
<50%        | ❌ RECHAZAR      | ❌ RECHAZAR      | Fallo crítico
```

### Paso 5.4: Decisión Final (ALGORITMO)

```
IF porcentaje_conformidad >= 50% THEN
   estado = "APROBADO CON CORRECCIONES"
   prioridad = "ALTA"
   acciones_requeridas = [lista de correcciones]
   
ELSE (porcentaje_conformidad < 50%) THEN
   estado = "RECHAZADO"
   prioridad = "CRÍTICA"
   recomendacion = "Requiere revisión completa por equipo especialista"

END IF
```

---

## VIII. FASE 6: DOCUMENTACIÓN DE HALLAZGOS

### Paso 6.1: Reporte por Función Rechazada

Para CADA función rechazada, generar:

```
┌──────────────────────────────────────────────────────────┐
│ FUNCIÓN [N]: [Nombre]                                    │
│ VEREDICTO: ❌ RECHAZADA                                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ TEXTO ACTUAL:                                            │
│ "[Texto completo]"                                       │
│                                                           │
│ PROBLEMAS IDENTIFICADOS:                                 │
│                                                           │
│ 1. PROBLEMA PRINCIPAL                                    │
│    └─ Descripción: [Qué está mal]                       │
│    └─ Causa raíz: [Por qué ocurre]                      │
│    └─ Impacto: [Qué consecuencia]                       │
│                                                           │
│ 2. PROBLEMA SECUNDARIO (si aplica)                       │
│    └─ [Similar estructura]                              │
│                                                           │
│ ANÁLISIS NORMATIVO:                                      │
│    Normativa dice: "[Cita]"                             │
│    Descripción dice: "[Cita]"                           │
│    Brecha: "[Diferencia explícita]"                     │
│                                                           │
│ RECOMENDACIÓN DE CORRECCIÓN:                             │
│                                                           │
│ OPCIÓN 1 - ELIMINAR (si no es crítica):                 │
│    Justificación: [Por qué no es necesaria]             │
│                                                           │
│ OPCIÓN 2 - REDEFINIR (si es crítica):                   │
│    Texto nuevo: "[Redacción corregida]"                 │
│    Cambios: [Listado de cambios realizados]             │
│    Justificación: [Por qué es mejor]                    │
│                                                           │
│ PRIORIDAD: [CRÍTICA / IMPORTANTE / MENOR]               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Paso 6.2: Reporte Consolidado Final

```
┌────────────────────────────────────────────────────────────┐
│ REPORTE FINAL DE EVALUACIÓN                                │
│ Puesto: [Nombre]                                           │
│ Fecha: [Fecha]                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. RESUMEN EJECUTIVO                                       │
│    ├─ Total de funciones: 20                               │
│    ├─ Aprobadas: 16 (80%)                                  │
│    ├─ Rechazadas: 3 (15%)                                  │
│    ├─ Observadas: 1 (5%)                                   │
│    └─ VEREDICTO: ✅ APROBADO CON CORRECCIONES MENORES     │
│                                                             │
│ 2. UMBRAL APLICADO                                         │
│    ├─ Versión: 1.1 (Permisiva)                             │
│    ├─ Umbral: 50% funciones conformes                      │
│    ├─ Resultado: 80% conforme > 50% requerido             │
│    └─ Conclusión: ✅ Supera umbral                         │
│                                                             │
│ 3. FUNCIONES PROBLEMÁTICAS (3)                             │
│    ├─ Función 2: [Resumen problema]                        │
│    ├─ Función 4: [Resumen problema]                        │
│    └─ Función 11: [Resumen problema]                       │
│                                                             │
│ 4. ACCIONES REQUERIDAS (Ordenadas por prioridad)           │
│    ├─ CRÍTICA:                                             │
│    │  □ Corrección Función 11 (ELIMINAR)                   │
│    ├─ IMPORTANTE:                                          │
│    │  □ Corrección Función 2 (Redacción)                   │
│    │  □ Corrección Función 4 (Verbo)                       │
│    └─ Validación jurídica post-correcciones                │
│                                                             │
│ 5. RECOMENDACIONES                                         │
│    ├─ Establecer proceso de revisión con Asuntos Jurídicos │
│    ├─ Crear plantilla reusable para futuras descripciones  │
│    └─ Documentar excepciones normativas para referencia     │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## IX. ADAPTACIÓN PARA OTROS LLMs

### Paso 9.1: Instrucciones Transferibles

```
INSTRUCCIONES PARA OTROS LLMs:

1. CONTEXTO A PROPORCIONAR:
   ├─ Documento: Descripción de puesto completa
   ├─ Normativa: Reglamento Interior (completo o Art. 6+)
   ├─ Matriz: Guía de verbos autorizados
   ├─ Umbral: Especificar 1.0 (95%) o 1.1 (50%)
   └─ Criterios: Este protocolo completo

2. PROMPT PARA LLM:

   "Eres un evaluador especialista de descripciones de puestos.
   Tu tarea es evaluar 20 funciones descritas de un puesto de 
   Dirección General usando análisis semántico normativo.
   
   Sigue el PROTOCOLO DE EVALUACIÓN DE DESCRIPCIÓN DE PUESTOS 
   (versión 1.1, umbral 50%).
   
   Inputs:
   - [Documento de descripción]
   - [Reglamento Interior]
   - [Matriz de verbos]
   
   Outputs:
   - Matriz consolidada
   - Análisis por función
   - Reporte final
   - Recomendaciones"

3. VALIDACIONES CRÍTICAS:
   ├─ Verificar que usa análisis semántico, no solo lexical
   ├─ Confirmar que busca respaldo normativo para excepciones
   ├─ Validar que identifica inversiones jerárquicas
   ├─ Comprobar que aplica umbral 50% correctamente
   └─ Revisar que documentación es clara y justificada
```

### Paso 9.2: Puntos de Fallo Comunes

```
ERRORES QUE COMETER OTROS LLMs:

1. ❌ Análisis Lexical en lugar de Semántico
   └─ Buscan palabras exactas en lugar de significados
   └─ Solución: Insistir en "Análisis semántico = significados"

2. ❌ No verifican respaldo normativo de excepciones
   └─ Aceptan verbos no autorizados sin justificación
   └─ Solución: Crear tabla explícita de excepciones válidas

3. ❌ No detectan inversiones jerárquicas
   └─ Aceptan funciones operacionales en nivel estratégico
   └─ Solución: Ejemplo explícito: "Función X es operacional, rechazar"

4. ❌ Aplican umbral equivocado
   └─ Usan 95% cuando debería ser 50%
   └─ Solución: Especificar umbral en cada prompt

5. ❌ No documentan criterios individuales
   └─ Solo dicen "Aprobado" sin explicar por qué
   └─ Solución: Exigir matriz con 5 criterios por función
```

---

## X. GLOSARIO DE TÉRMINOS

```
ANÁLISIS SEMÁNTICO: Comparación de SIGNIFICADOS, no de palabras.
   Ejemplo: "Emitir" y "Expedir" son semánticamente equivalentes

ATRIBUCIONES INDELEGABLES: Funciones que NO pueden delegarse.
   Típicamente en Art. 6 de reglamentos internos

CORRESPONDENCIA NORMATIVA: Relación entre función descrita y atribución legal.
   Puede ser DIRECTA (mismas palabras) o SEMÁNTICA (mismo significado)

INVERSIÓN JERÁRQUICA: Asignar a un nivel funciones de nivel inferior.
   Síntoma: Secretario hace tareas operacionales

EXCEPCCIÓN CON RESPALDO: Verbo no en matriz pero autorizado en normativa.
   Ejemplo: REFRENDAR en Art. 6, Inc. XI

NÚCLEO SEMÁNTICO: Significado esencial de una función en 1-2 líneas.
   Se compara el núcleo descrito con el núcleo normativo

UMBRAL DE APROBACIÓN: Porcentaje mínimo de funciones conformes requerido.
   1.0: 95% | 1.1: 50%

VERBO DE MANDATO: Verbo que implica autoridad (Ordenar, Conducir, Determinar).
   Contrario a: Verbo de delegación (Encomendar, Sugerir)
```

---

## XI. CHECKLIST DE VALIDACIÓN DEL PROTOCOLO

**Usar esta checklist para confirmar que el protocolo se aplicó correctamente:**

```
PREPARACIÓN ✓
☐ Se definió nivel jerárquico del puesto
☐ Se obtuvieron todos los documentos base
☐ Se creó contexto de puesto estructurado
☐ Se definió umbral (especificar: 1.0 o 1.1)

EXTRACCIÓN NORMATIVA ✓
☐ Se extrajeron todas las atribuciones del Art. 6
☐ Se identificaron atribuciones delegables
☐ Se creó matriz de correspondencia
☐ Se documentó cada atribución con número de artículo

CONSTRUCCIÓN DE MATRIZ ✓
☐ Se extrajeron verbos autorizados
☐ Se identificaron excepciones con respaldo
☐ Se creó matriz maestra de verbos
☐ Se documentaron verbos prohibidos

ANÁLISIS SEMÁNTICO ✓
☐ Se extrajo núcleo semántico de CADA función
☐ Se extrajo núcleo normativo de CADA atribución
☐ Se compararon significados (no palabras)
☐ Se aplicó tabla de equivalencias semánticas

EVALUACIÓN POR FUNCIÓN ✓
☐ Se evaluó CADA función con 5 criterios
☐ Se documentó cada criterio con justificación
☐ Se llegó a veredicto por función
☐ Se aplicó ponderación correcta

CONSOLIDACIÓN ✓
☐ Se creó matriz consolidada de todas las funciones
☐ Se calculó porcentaje de conformidad
☐ Se aplicó umbral correctamente
☐ Se llegó a veredicto final

DOCUMENTACIÓN ✓
☐ Se documentó cada función rechazada
☐ Se propusieron correcciones con justificación
☐ Se creó reporte ejecutivo
☐ Se generó reporte técnico completo

TRANSFERIBILIDAD ✓
☐ Se documentó protocolo para otros LLMs
☐ Se especificaron puntos de fallo común
☐ Se creó glosario de términos
☐ Se proporcionaron ejemplos concretos
```

---

## XII. EJEMPLO COMPLETO: APLICACIÓN DEL PROTOCOLO

**A continuación, se muestra la aplicación PASO A PASO en un caso real:**

### Ejemplo: Evaluación de Función 11 (Interpretación)

```
PASO 1: EXTRACCIÓN
─────────────────
Función 11 (Texto): "Interpretar el Reglamento Interior de la Secretaría 
de la Función Pública, con auxilio de la Unidad de Asuntos Jurídicos, 
y las unidades competentes para la solución de contradicciones en su 
aplicación."

PASO 2: ANÁLISIS DE VERBO
─────────────────────────
Verbo identificado: INTERPRETAR

¿Está en matriz?
└─ NO (no aparece en lista de verbos DG)

¿Tiene respaldo normativo?
└─ Buscar: "INTERPRETAR" en Art. 6
   └─ NO ENCONTRADO en Art. 6

¿Existe en nivel delegable (subsecretarios)?
└─ Buscar: "INTERPRETAR" en Art. 11
   └─ SÍ ENCONTRADO: "Interpretar... disposiciones jurídicas 
                      en materia de administración"
   └─ PERO: Es función de COORDINADORES/DIRECTORES, no Secretario

Veredicto de Verbo: ❌ NO AUTORIZADO

PASO 3: ANÁLISIS DE NORMATIVA
─────────────────────────────
¿Existe en Art. 6 (atribuciones del Secretario)?
└─ NO existe "interpretar" como función del Secretario

¿Existe delegada?
└─ SÍ, en Art. 11 (para directores)

Implicación: ❌ Esta es función OPERACIONAL delegable, 
            no atribución del Secretario

Veredicto de Normativa: ❌ SIN RESPALDO

PASO 4: ANÁLISIS SEMÁNTICO
──────────────────────────
Núcleo semántico de función: 
"El Secretario personalmente interpreta y emite criterios 
sobre aplicación de normas internas"

Núcleo normativo de Art. 6:
[No existe función de interpretación]

Comparación: ❌ NO HAY NÚCLEO NORMATIVO EQUIVALENTE

Veredicto de Semántica: ❌ SIN CORRESPONDENCIA

PASO 5: ALINEACIÓN JERÁRQUICA
─────────────────────────────
¿Corresponde al nivel DG?
└─ NO. Interpretar normas es trabajo operacional/jurídico

¿Hay inversión jerárquica?
└─ SÍ. El Secretario haría trabajo que debería delegar 
      a la Unidad Jurídica

¿Debería estar en descripción?
└─ NO. Debería estar que "ordena a la Unidad Jurídica 
      que interprete", no que el Secretario interpreta

Veredicto Jerárquico: ❌ INVERSIÓN JERÁRQUICA CLARA

PASO 6: VEREDICTO FINAL
───────────────────────
Verbo:          ❌ NO AUTORIZADO
Normativa:      ❌ SIN RESPALDO
Estructura:     🟡 FORMAL (pero innecesaria)
Semántica:      ❌ SIN CORRESPONDENCIA
Jerárquica:     ❌ INVERSIÓN

SCORE: (0 + 0 + 0.5 + 0 + 0) / 5 = 0.10 (10%)

VEREDICTO FINAL: ❌ RECHAZADA

RECOMENDACIÓN:
├─ Opción 1 (PREFERIDA): ELIMINAR por completo
├─ Opción 2 (Si crítica): Redefinir como:
│  "Ordenar a la Unidad de Asuntos Jurídicos la interpretación 
│   del Reglamento Interior y la emisión de criterios vinculantes 
│   para la solución uniforme de contradicciones en su aplicación."
└─ Prioridad: CRÍTICA (porque invierte jerarquía)
```

---

## XIII. CONCLUSIÓN Y PRÓXIMOS PASOS

Este protocolo proporciona:

✅ **Sistematicidad:** Proceso paso a paso, no arbitrario  
✅ **Reproducibilidad:** Otros LLMs pueden replicar exactamente  
✅ **Justificabilidad:** Cada decisión tiene fundamento documentado  
✅ **Escalabilidad:** Funciona para 5 funciones o 100 funciones  
✅ **Validez normativa:** Anclado en ley/reglamento, no opinión  

**Para implementar con otros LLMs:**

1. Proporcione ESTE protocolo completo
2. Especifique UMBRAL (1.0 o 1.1)
3. Adjunte documentos (Descripción + Normativa + Matriz)
4. Solicite salida estructurada (matriz + análisis + reporte)
5. Valide contra checklist de validación (Sección XI)

---

**Documento Preparado Por:** Desarrollador Senior  
**Metodología:** Análisis Semántico Normativo Sistemático  
**Versión del Protocolo:** 1.1 (Umbral 50%)  
**Fecha:** 7 de noviembre de 2025  
**Clasificación:** Protocolo Técnico - Transferible a LLMs
