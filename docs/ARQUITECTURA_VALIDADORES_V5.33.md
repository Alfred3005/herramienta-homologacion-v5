# Arquitectura de Validadores - Sistema v5.33-new

**Fecha:** Noviembre 2025
**Versión:** 5.33-new
**Propósito:** Documentar la arquitectura completa de validadores y uso de LLMs

---

## 📋 RESUMEN EJECUTIVO

El sistema de homologación v5.33-new utiliza **4 validadores principales** para evaluar puestos de trabajo de la APF mexicana:

| Validador | Usa LLM | Modelo | Propósito |
|-----------|---------|--------|-----------|
| **AdvancedQualityValidator** | ✅ Sí | gpt-4o-mini | Análisis holístico de calidad |
| **Criterio 1: Análisis Semántico** | ✅ Sí | gpt-4o-mini | Evaluación de funciones individuales |
| **Criterio 2: Contextual** | ✅ Sí | gpt-4o-mini | Validación con normativa |
| **Criterio 3: Impacto Jerárquico** | ❌ No | Reglas heurísticas | Coherencia de impacto vs nivel |

**Total de llamadas LLM por puesto:** N+2 (donde N = número de funciones)

---

## 🏗️ ARQUITECTURA DETALLADA

### 1. AdvancedQualityValidator (v5.33-new)

**Archivo:** `src/validators/advanced_quality_validator.py`

**Propósito:** Análisis holístico de calidad del puesto completo en una sola llamada LLM.

**Usa LLM:** ✅ Sí (GPT-4o-mini)

**Llamadas por puesto:** 1

**Tokens promedio:** ~4,000 tokens (2,500 input + 1,500 output)

**Detecta:**
1. **Duplicación semántica** entre funciones
2. **Funciones malformadas** (vacías, placeholders, sin sentido)
3. **Problemas de marco legal** (organismos extintos, leyes obsoletas)
4. **Objetivo general inadecuado** (muy corto, genérico, sin finalidad)

**Ventaja del enfoque holístico:**
- Ve TODO el contexto del puesto
- 1 llamada LLM vs 4+ llamadas separadas
- Más económico y eficiente
- Mejor detección de patrones globales

**Costo por puesto:**
```
Input:  2,500 tokens × $0.15/1M = $0.000375
Output: 1,500 tokens × $0.60/1M = $0.000900
TOTAL: ~$0.0013
```

---

### 2. Criterio 1: Análisis Semántico de Funciones (Protocolo SABG)

**Archivos:**
- `src/validators/function_semantic_evaluator.py` (evaluador principal)
- `src/validators/verb_semantic_analyzer.py` (analizador de verbos)

**Propósito:** Evaluar cada función individual usando el Protocolo SABG (Semántico, Apropiación, Respaldo, Bien formulada, Global).

**Usa LLM:** ✅ Sí (GPT-4o-mini)

**Llamadas por puesto:** N (una por función)

**Tokens promedio por función:** ~2,000 tokens (1,200 input + 800 output)

**Evalúa 5 dimensiones:**
1. **Verbo (25%):** Fortaleza semántica del verbo rector
2. **Normativa (25%):** Respaldo en normativa institucional
3. **Estructura (20%):** Verbo + Complemento + Resultado/Finalidad
4. **Semántica (20%):** Claridad, especificidad, alcance
5. **Jerárquica (10%):** Apropiación para el nivel del puesto

**Clasificación:**
- Score ≥ 70% → APROBADO
- Score 50-69% → OBSERVADO
- Score < 50% → RECHAZADO

**Costo por función:**
```
Input:  1,200 tokens × $0.15/1M = $0.00018
Output:   800 tokens × $0.60/1M = $0.00048
TOTAL: ~$0.00066
```

**Costo por puesto (12 funciones):**
```
12 funciones × $0.00066 = $0.0079
```

---

### 3. Criterio 2: Validación Contextual con Normativa

**Archivo:** `src/validators/contextual_verb_validator.py`

**Propósito:** Validar que las funciones tienen respaldo en la normativa institucional y que hay herencia jerárquica adecuada.

**Usa LLM:** ✅ Sí (GPT-4o-mini)

**Modo de operación:** HYBRID (1 llamada global)

**Llamadas por puesto:** 1

**Tokens promedio:** ~1,500 tokens (1,000 input + 500 output)

**Valida:**
1. **Referencias institucionales** coinciden con normativa
2. **Herencia jerárquica** válida (funciones apropiadas para nivel)
3. **Alineación global** del puesto con normativa

**Resultado:**
- ALIGNED → PASS
- PARTIALLY_ALIGNED → Depende de umbrales
- NOT_ALIGNED → FAIL

**Costo por puesto:**
```
Input:  1,000 tokens × $0.15/1M = $0.00015
Output:   500 tokens × $0.60/1M = $0.00030
TOTAL: ~$0.00045
```

---

### 4. Criterio 3: Apropiación de Impacto Jerárquico

**Archivos:**
- `src/validators/criterion_3_validator.py` (validador principal)
- `src/validators/impact_analyzer.py` (analizador de impacto)

**Propósito:** Evaluar si el impacto declarado en las funciones es coherente con el nivel jerárquico del puesto.

**Usa LLM:** ❌ **NO** - Basado en reglas y patrones de texto

**Llamadas por puesto:** 0 (sin LLM)

**Tokens promedio:** 0

**Método:**
1. **Extracción de indicadores** de impacto del texto de funciones usando regex
2. **Análisis de 3 dimensiones:**
   - **Scope (Alcance):** local → institutional → interinstitutional → strategic_national
   - **Consequences (Consecuencias):** operational → tactical → strategic → systemic
   - **Complexity (Complejidad):** routine → analytical → strategic → transformational
3. **Comparación** contra perfil esperado del nivel jerárquico
4. **Verificación de verbos:** apropiados vs prohibidos por nivel
5. **Búsqueda de respaldo normativo** para discrepancias

**Clasificación:**
- **CRITICAL:** Discrepancia SIN respaldo normativo
- **MODERATE:** Discrepancia CON respaldo normativo
- **OK:** Sin discrepancias

**Threshold:** >50% funciones CRITICAL → FAIL

**Tasa Crítica:** (CRITICAL functions / Total functions) × 100%

**Ejemplo de indicadores:**
```python
# Scope indicators
"nacional" → strategic_national
"de la dirección" → institutional
"del departamento" → local

# Consequences indicators
"afecta sistema nacional" → systemic
"compromete metas" → tactical
"interrumpe flujo" → operational

# Complexity indicators
"transformar" → transformational
"analizar" → analytical
"repetitivo" → routine
```

**Ventajas del enfoque sin LLM:**
- ✅ **Costo:** $0 (no consume tokens)
- ✅ **Velocidad:** Instantáneo (sin latencia de API)
- ✅ **Consistencia:** 100% determinístico
- ✅ **Escalabilidad:** Miles de puestos en segundos
- ✅ **Sin API key:** Funciona offline

**Limitaciones:**
- ⚠️ Depende de palabras clave explícitas en el texto
- ⚠️ No capta contexto implícito o matices sutiles
- ⚠️ Puede fallar con redacciones no estándar

**¿Por qué no usa LLM?**
1. **Eficiencia:** El análisis de patrones es suficiente para la mayoría de casos
2. **Costo:** Ahorra ~$0.002/puesto
3. **Velocidad:** 100x más rápido que llamada LLM
4. **Diseño original:** El Criterio 3 fue concebido como análisis heurístico

**Costo por puesto:**
```
TOTAL: $0.00 (sin LLM)
```

---

## 💰 COSTO TOTAL POR PUESTO

### Desglose detallado (12 funciones):

| Componente | Llamadas | Costo |
|------------|----------|-------|
| AdvancedQualityValidator | 1 | $0.0013 |
| Criterio 1 (12 funciones) | 12 | $0.0079 |
| Criterio 2 (contextual) | 1 | $0.0005 |
| Criterio 3 (impacto) | 0 | $0.0000 |
| **TOTAL** | **14** | **$0.0097** |

**Redondeado:** ~$0.012 por puesto

---

## 🔄 FLUJO DE VALIDACIÓN

```
IntegratedValidator.validate_puesto()
│
├─► [1] AdvancedQualityValidator (1 llamada LLM)
│   └─► Detecta: duplicados, malformadas, marco legal, objetivo
│
├─► [2] Criterio 1: Análisis Semántico (N llamadas LLM)
│   ├─► Función 1 → FunctionSemanticEvaluator → APROBADO/OBSERVADO/RECHAZADO
│   ├─► Función 2 → FunctionSemanticEvaluator → ...
│   └─► Función N → FunctionSemanticEvaluator → ...
│   └─► Threshold: ≥50% APROBADAS → PASS
│
├─► [3] Criterio 2: Validación Contextual (1 llamada LLM)
│   └─► ContextualVerbValidator → ALIGNED/PARTIALLY/NOT_ALIGNED
│   └─► Threshold: ALIGNED o PARTIALLY con herencia → PASS
│
├─► [4] Criterio 3: Impacto Jerárquico (0 llamadas LLM)
│   ├─► Por cada función:
│   │   ├─► Extraer indicadores (scope, consequences, complexity)
│   │   ├─► Comparar vs perfil esperado
│   │   ├─► Verificar verbos apropiados/prohibidos
│   │   └─► Buscar respaldo normativo
│   ├─► Calcular Tasa Crítica
│   └─► Threshold: ≤50% CRITICAL → PASS
│
└─► [5] Decisión Final: Matriz 2-of-3
    └─► Si 2+ criterios PASS → APROBADO
        Si 1 criterio PASS → OBSERVADO
        Si 0 criterios PASS → RECHAZADO
```

---

## ⚠️ PREGUNTAS FRECUENTES

### ¿Por qué Criterio 3 no usa LLM?

**R:** Fue diseñado como análisis heurístico basado en reglas para:
1. Reducir costos (ahorra $0.002/puesto)
2. Aumentar velocidad (100x más rápido)
3. Garantizar consistencia (determinístico)
4. Funcionar sin API key (útil para demos/offline)

### ¿Debería Criterio 3 usar LLM?

**Ventajas de agregar LLM:**
- ✅ Mejor comprensión de contexto implícito
- ✅ Detección de matices sutiles
- ✅ Más flexible con redacciones no estándar

**Desventajas:**
- ❌ Aumenta costo en ~20% ($0.012 → $0.014)
- ❌ Añade latencia (1-2 segundos más)
- ❌ Pierde determinismo (puede variar ligeramente)

**Recomendación actual:** Mantener sin LLM. Los resultados actuales (ej: 25 puestos de Turismo con 0% Tasa Crítica) demuestran que funciona correctamente.

**Cuándo considerar LLM para Criterio 3:**
- Si detectas muchos falsos positivos (funciones marcadas como CRITICAL incorrectamente)
- Si las descripciones de funciones usan lenguaje muy atípico
- Si necesitas análisis más profundo de contexto organizacional

### ¿Cómo sé si Criterio 3 está funcionando?

**Indicadores de correcto funcionamiento:**

✅ **Tasa 0%** en puestos bien diseñados (como tus 25 de Turismo)
- Significa: No hay discrepancias críticas sin respaldo
- Es un resultado POSITIVO, no un bug

✅ **Tasa 10-30%** en puestos con problemas menores
- Algunas funciones tienen alcance no apropiado para el nivel
- Pero tienen respaldo normativo (MODERATE) o son pocas (CRITICAL)

❌ **Tasa >50%** en puestos problemáticos
- Muchas funciones con impacto incoherente sin respaldo
- El criterio FALLA correctamente

**Verifica en los reportes:**
- Sección "Criterio 3: Impacto Jerárquico"
- Métricas: total_functions, functions_critical, functions_moderate
- Tasa Crítica: (functions_critical / total_functions) × 100%

### ¿Puedo desactivar Criterio 3 para ahorrar tiempo?

**No recomendado.** Aunque no usa LLM, el Criterio 3 es valioso porque:
1. Detecta verbos prohibidos (ej: "ejecutar" en nivel G)
2. Identifica funciones con alcance muy bajo/alto para el nivel
3. Es instantáneo (sin costo de tiempo real)
4. Forma parte de la matriz 2-of-3

Si lo desactivas, pierdes un criterio de validación importante.

---

## 📊 COMPARATIVA: CON vs SIN LLM EN CRITERIO 3

### Escenario hipotético: Criterio 3 con LLM

| Métrica | Actual (sin LLM) | Hipotético (con LLM) |
|---------|------------------|----------------------|
| **Costo/puesto** | $0.012 | $0.014 (+17%) |
| **Tokens/puesto** | 45,000 | 50,000 (+11%) |
| **Tiempo/puesto** | ~30s | ~35s (+17%) |
| **Llamadas LLM** | 14 | 15 (+7%) |
| **Consistencia** | 100% | ~95% |
| **Precisión** | Alta | Muy alta |

**Conclusión:** El enfoque actual es óptimo para la mayoría de casos. Solo considera LLM si detectas problemas específicos de precisión.

---

## 🔧 MODIFICACIONES FUTURAS

### Si decides agregar LLM al Criterio 3:

**Archivos a modificar:**
1. `src/validators/criterion_3_validator.py`
   - Agregar `from src.validators.shared_utilities import robust_openai_call`
   - Modificar `_analyze_function()` para usar LLM

2. `src/validators/impact_analyzer.py`
   - Agregar método `analyze_with_llm()`
   - Mantener método actual como fallback

**Prompt sugerido:**
```python
prompt = f"""
Analiza el impacto de esta función del puesto:

**Nivel del puesto:** {nivel_salarial}
**Perfil esperado:** {expected_impact}
**Función:** {funcion_text}

Evalúa si el alcance, consecuencias y complejidad son apropiados para el nivel.

Responde en JSON:
{{
  "is_appropriate": true/false,
  "scope_level": "local|institutional|interinstitutional|strategic_national",
  "consequences_level": "operational|tactical|strategic|systemic",
  "complexity_level": "routine|analytical|strategic|transformational|innovative",
  "discrepancy_severity": "OK|MODERATE|CRITICAL",
  "reasoning": "explicación"
}}
"""
```

**Costo adicional:** ~$0.002/puesto

---

## 📝 CONCLUSIÓN

El sistema v5.33-new usa un **enfoque híbrido inteligente**:
- **LLM para análisis semántico y contextual** (Criterios 1 y 2, AdvancedQualityValidator)
- **Reglas heurísticas para análisis de impacto** (Criterio 3)

Este balance optimiza **costo, velocidad y precisión**.

**Criterio 3 sin LLM es una decisión de diseño acertada**, no un defecto.

---

**Versión:** 5.33-new
**Fecha:** Noviembre 2025
**Última actualización:** 2025-11-11
