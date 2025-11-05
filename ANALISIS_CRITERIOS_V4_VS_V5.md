# 📊 Análisis Comparativo: Sistema de Validación v4 vs v5

**Fecha**: 2025-11-05
**Objetivo**: Documentar hallazgos de v4 y proponer mejora para v5
**Estado**: ✅ Análisis Completo

---

## 🔍 Resumen Ejecutivo

### Hallazgos Principales

1. **v4 tiene 3 CRITERIOS completos**, v5 solo tiene 2 implementados
2. **Criterio 2 (Impacto y Magnitud)** en v4 es **MUY SOFISTICADO**
3. El Criterio 2 ya evalúa el **complemento/"para qué?"** que el usuario pidió
4. Sistema de decisión binaria: **2 de 3 criterios deben pasar**

### Brecha Identificada

```
v4 (COMPLETO)                    v5 (INCOMPLETO)
├─ Criterio 1: Congruencia      ├─ Criterio 1: Congruencia ✅
├─ Criterio 2: Impacto          │  (Weak verbs threshold)
│  └─ Impacto funcional         │
│  └─ Complemento "para qué?"   └─ Criterio 2: Contextual Validator ✅
│  └─ Magnitud                     └─ Solo referencias institucionales
├─ Criterio 3: Compliance
   └─ Normativo                 ❌ FALTA: Criterio de impacto completo
   └─ Apropiación jerárquica    ❌ FALTA: Criterio 3 (compliance)
```

---

## 📋 Criterios en v4 (Documentación Completa)

### Criterio 1: Congruencia de Verbos

**Archivo**: `agente_2_evaluador.py:650-725`

**Qué evalúa**:
- Verbos débiles sin respaldo normativo
- Threshold: 50% de funciones con verbos CRÍTICOS falla el criterio
- Clasificación CRITICAL vs MODERATE según respaldo

**Decisión**:
```python
# PASS: ≤50% de funciones con verbos críticos
# FAIL: >50% de funciones con verbos críticos
```

**Ya implementado en v5**: ✅

---

### Criterio 2: Impacto y Magnitud Funcional

**Archivo**: `agente_2_evaluador.py:726-835`

**¡ESTE ES EL CRITERIO CLAVE QUE EL USUARIO BUSCABA!**

#### Qué evalúa (3 dimensiones):

1. **Alcance de Decisiones** (Decision Scope)
   - Detecta indicadores: "nacional", "país", "interinstitucional", "departamental"
   - Compara contra perfil esperado por nivel
   - 4 niveles: `local → institutional → interinstitutional → strategic_national`

2. **Magnitud Presupuestaria** (Resource Magnitude)
   - Detecta: "millones", "presupuesto nacional", "recursos estratégicos", "suministros"
   - 5 niveles: `minimal → moderate → significant → major → strategic`

3. **Consecuencias de Errores** (Error Consequences)
   - Inferidas desde complejidad + alcance
   - 4 niveles: `operational → tactical → strategic → systemic`

#### Perfil de Impacto por Nivel (VERB_HIERARCHY)

**Archivo**: `shared_utilities.py:64-178`

```python
VERB_HIERARCHY = {
    "G": {  # Secretario
        "impact_profile": {
            "decision_scope": "strategic_national",
            "budget_range": "strategic",
            "error_consequences": "systemic",
            "complexity_level": "transformational"
        }
    },
    "J": {  # Titular OAD
        "impact_profile": {
            "decision_scope": "interinstitutional",
            "budget_range": "major",
            "error_consequences": "strategic",
            "complexity_level": "innovative"
        }
    },
    "M": {  # Director
        "impact_profile": {
            "decision_scope": "institutional",
            "budget_range": "significant",
            "error_consequences": "tactical",
            "complexity_level": "analytical"
        }
    },
    "O": {  # Jefe Depto
        "impact_profile": {
            "decision_scope": "local",
            "budget_range": "moderate",
            "error_consequences": "operational",
            "complexity_level": "routine"
        }
    },
    "P": {  # Enlace
        "impact_profile": {
            "decision_scope": "local",
            "budget_range": "minimal",
            "error_consequences": "operational",
            "complexity_level": "routine"
        }
    }
}
```

#### Análisis de Indicadores de Impacto

**Método**: `_analyze_impact_indicators()` (línea 971)

```python
def _analyze_impact_indicators(functions):
    combined_text = ""
    for func in functions:
        combined_text += func.get("descripcion_completa", "") + " "
        combined_text += func.get("que_hace", "") + " "
        combined_text += func.get("para_que_lo_hace", "") + " "  # ← COMPLEMENTO!

    # Detecta alcance
    scope_indicators = {
        "strategic_national": ["nacional", "país", "república", "federal", "sectorial"],
        "interinstitutional": ["interinstitucional", "coordinación", "otras dependencias"],
        "institutional": ["institucional", "secretaría", "dependencia", "interno"],
        "local": ["departamental", "área", "local", "específico", "operativo"]
    }

    # Detecta magnitud presupuestaria
    budget_indicators = {
        "strategic": ["millones", "presupuesto nacional", "recursos estratégicos"],
        "major": ["presupuesto", "recursos institucionales", "fondos significativos"],
        "significant": ["recursos", "fondos", "asignaciones", "inversión"],
        "moderate": ["recursos limitados", "presupuesto operativo"],
        "minimal": ["gastos", "suministros", "materiales"]
    }

    # Detecta complejidad
    complexity_indicators = {
        "transformational": ["transformar", "reestructurar", "rediseñar", "innovar"],
        "strategic": ["estratégico", "políticas", "lineamientos", "directrices"],
        "analytical": ["analizar", "evaluar", "diagnosticar", "estudiar"],
        "routine": ["ejecutar", "realizar", "tramitar", "procesar"]
    }

    return {
        "detected_scope": max_matches(scope_indicators),
        "detected_budget": max_matches(budget_indicators),
        "detected_complexity": max_matches(complexity_indicators)
    }
```

#### Evaluación de Coherencia (3 sub-evaluaciones)

1. **`_evaluate_decision_scope_coherence()`** (línea 1046)
   ```python
   # Jerarquía de alcances
   scope_hierarchy = {
       "local": 1,
       "institutional": 2,
       "interinstitutional": 3,
       "strategic_national": 4
   }

   # Tolerancia: ±1 nivel
   is_coherent = abs(detected_level - expected_level) <= 1

   # Si incoherencia > 2 niveles → CRITICAL flag
   # Si 1-2 niveles → MODERATE flag
   ```

2. **`_evaluate_resource_magnitude_coherence()`** (línea 1092)
   ```python
   budget_hierarchy = {
       "minimal": 1, "moderate": 2, "significant": 3,
       "major": 4, "strategic": 5
   }

   # Tolerancia amplia: ±2 niveles (difícil de detectar)
   is_coherent = abs(detected_level - expected_level) <= 2

   # Solo MODERATE flags (no CRITICAL)
   ```

3. **`_evaluate_error_consequences_coherence()`** (línea 1141)
   ```python
   # Inferir consecuencias desde complejidad + alcance
   consequence_mapping = {
       ("transformational", "strategic_national"): "systemic",
       ("strategic", "interinstitutional"): "strategic",
       ("analytical", "institutional"): "tactical",
       ("routine", "local"): "operational"
   }

   consequence_hierarchy = {
       "operational": 1, "tactical": 2,
       "strategic": 3, "systemic": 4
   }

   # Tolerancia: ±1 nivel
   is_coherent = abs(inferred_level - expected_level) <= 1
   ```

#### Lógica de PASS/FAIL

```python
# Consolidar flags de las 3 dimensiones
critical_inconsistencies = count(flags where severity == "CRITICAL")
moderate_inconsistencies = count(flags where severity == "MODERATE")

# PASS si: 0 críticas Y máximo 1 moderada
is_passing = (critical_inconsistencies == 0 and moderate_inconsistencies <= 1)

# Confianza = promedio de coherence_scores (0.0 - 1.0)
coherence_score = (scope + resource + consequence) / 3
```

**Estado en v5**: ❌ NO IMPLEMENTADO (solo validación institucional)

---

### Criterio 3: Compliance Normativo

**Archivo**: `agente_2_evaluador.py:837-969`

**Qué evalúa**:

1. **Validación contra normativa**:
   - Búsqueda semántica en documentos normativos
   - Detección de violaciones y warnings
   - Verificación de número de funciones esperadas vs reales

2. **Inferencia de unidad administrativa**:
   ```python
   unit_keywords = {
       "Transparencia": ["transparencia", "acceso", "información"],
       "Anticorrupción": ["anticorrupción", "integridad", "ética"],
       "Gobierno Abierto": ["gobierno abierto", "participación"]
   }
   ```

3. **Conteo de funciones esperadas**:
   - Busca en normativa: "Artículo X. Funciones de [unidad]:"
   - Cuenta numerales romanos (I, II, III) o arábigos (1, 2, 3)
   - Si discrepancia > 50% → CRITICAL/MODERATE flag

**Decisión**:
```python
# PASS: No violaciones críticas, compliance_result.is_compliant == True
# FAIL: Violaciones detectadas o discrepancia significativa
```

**Estado en v5**: ❌ NO IMPLEMENTADO

---

## 🎯 Sistema de Decisión Binaria v4

### Matriz de Decisión (2 de 3 criterios)

**Archivo**: `agente_2_evaluador.py:140-161`

```python
DECISION_MATRIX = {
    3: {  # 3 criterios PASS
        "resultado": "APROBADO",
        "clasificacion": "EXCELENTE",
        "accion": "Sin modificaciones necesarias"
    },
    2: {  # 2 criterios PASS
        "resultado": "APROBADO_CON_OBSERVACIONES",
        "clasificacion": "ACEPTABLE",
        "accion": "Implementar mejoras menores en el criterio fallido"
    },
    1: {  # 1 criterio PASS
        "resultado": "RECHAZADO",
        "clasificacion": "DEFICIENTE",
        "accion": "Revisión sustancial requerida - fallan 2 criterios"
    },
    0: {  # 0 criterios PASS
        "resultado": "RECHAZADO",
        "clasificacion": "CRITICO",
        "accion": "Reescritura completa necesaria"
    }
}
```

### Lógica de Evaluación

```python
# Evaluar los 3 criterios independientemente
criterion_1 = _evaluate_criterion_1_congruencia()
criterion_2 = _evaluate_criterion_2_impact_magnitude()
criterion_3 = _evaluate_criterion_3_normative_compliance()

# Contar PASS
criteria_passed = sum([
    criterion_1.result == "PASS",
    criterion_2.result == "PASS",
    criterion_3.result == "PASS"
])

# Aplicar matriz
final_result = DECISION_MATRIX[criteria_passed]
```

---

## 💡 Propuesta: Criterio 3 Mejorado para v5

### Nombre Propuesto
**"Apropiación de Impacto Jerárquico con Validación Normativa"**

### Objetivos del Criterio

Combinar lo mejor de v4 con las mejoras sugeridas por el usuario:

1. **Evaluación de verbos apropiados por nivel** (v4 Criterio 3)
2. **Evaluación de impacto funcional** (v4 Criterio 2)
3. **Validación de complemento/"para qué?"** (v4 Criterio 2)
4. **Respaldo normativo de discrepancias** (nueva lógica propuesta por usuario)

### Arquitectura Propuesta

```
Criterio 3: Apropiación de Impacto Jerárquico
├─ Paso 1: Evaluación de Verbos Apropiados
│  ├─ Comparar verbos usados vs VERB_HIERARCHY[nivel].appropriate_verbs
│  ├─ Detectar verbos prohibidos (forbidden_verbs)
│  └─ Generar flags: CRITICAL si forbidden, MODERATE si inapropiados
│
├─ Paso 2: Evaluación de Impacto Funcional
│  ├─ Analizar complemento/"para qué?" con LLM
│  ├─ Detectar alcance de decisiones (scope)
│  ├─ Inferir magnitud presupuestaria (budget)
│  ├─ Evaluar consecuencias de errores (consequences)
│  └─ Comparar contra impact_profile esperado
│
├─ Paso 3: Validación de Discrepancias
│  ├─ Para cada incoherencia detectada:
│  │  ├─ Buscar respaldo en normativa con semantic search
│  │  ├─ Si HAY respaldo → Generar WARNING (anotación)
│  │  └─ Si NO hay respaldo → Generar CRITICAL flag
│  └─ Aplicar threshold: >50% CRITICAL → FAIL
│
└─ Decisión Final
   ├─ PASS si: ≤50% funciones con flags CRITICAL
   └─ FAIL si: >50% funciones con flags CRITICAL
```

### Implementación Detallada

#### Estructura de Datos

```python
@dataclass
class FunctionImpactAnalysis:
    """Análisis de impacto de una función individual"""
    funcion_id: str
    descripcion: str
    que_hace: str
    para_que_lo_hace: str  # ← COMPLEMENTO

    # Análisis de verbos
    verbo_principal: str
    es_verbo_apropiado: bool
    es_verbo_prohibido: bool

    # Análisis de impacto
    detected_scope: str  # local, institutional, interinstitutional, strategic_national
    detected_budget: str  # minimal, moderate, significant, major, strategic
    detected_consequences: str  # operational, tactical, strategic, systemic
    detected_complexity: str  # routine, analytical, strategic, transformational

    # Coherencia vs perfil esperado
    scope_coherent: bool
    budget_coherent: bool
    consequences_coherent: bool

    # Respaldo normativo
    normative_backing: Optional[str]  # Fragmento de normativa que respalda
    normative_confidence: float  # 0.0 - 1.0

    # Flags
    severity: str  # NONE, MODERATE, CRITICAL
    issue_detected: Optional[str]  # Descripción del problema
    suggested_fix: Optional[str]

@dataclass
class Criterion3Evaluation:
    """Resultado de evaluación del Criterio 3"""
    criterion_name: str = "APROPIACION_IMPACTO_JERARQUICO"
    result: str  # PASS / FAIL

    # Métricas
    total_functions: int
    functions_with_inappropriate_verbs: int
    functions_with_forbidden_verbs: int
    functions_with_impact_discrepancy: int
    functions_critical: int  # Sin respaldo normativo
    functions_moderate: int  # Con respaldo (anotación)

    # Threshold
    critical_rate: float  # % funciones CRITICAL
    threshold: float = 0.50

    # Detalles
    function_analyses: List[FunctionImpactAnalysis]
    flags_detected: List[EvaluationFlag]

    # Confianza
    confidence: float

    # Evidencia
    normative_fragments_used: List[str]
    reasoning: str
```

#### Método Principal

```python
def _evaluate_criterion_3_hierarchical_impact(
    self,
    data: Dict[str, Any],
    puesto_info: Dict[str, str]
) -> Criterion3Evaluation:
    """
    Criterio 3: Apropiación de Impacto Jerárquico

    Evalúa:
    1. Verbos apropiados por nivel
    2. Impacto funcional coherente con nivel
    3. Complemento/"para qué?" alineado
    4. Respaldo normativo de discrepancias
    """

    nivel_jerarquico = puesto_info["nivel_jerarquico"]
    functions = safe_get_nested(data, "funciones", [])

    # Obtener perfil esperado
    hierarchy_info = VERB_HIERARCHY.get(nivel_jerarquico, {})
    appropriate_verbs = hierarchy_info.get("appropriate_verbs", [])
    forbidden_verbs = hierarchy_info.get("forbidden_verbs", [])
    impact_profile = hierarchy_info.get("impact_profile", {})

    function_analyses = []
    critical_count = 0
    moderate_count = 0

    # PASO 1: Analizar cada función
    for func in functions:
        analysis = self._analyze_single_function_impact(
            func,
            nivel_jerarquico,
            appropriate_verbs,
            forbidden_verbs,
            impact_profile
        )

        function_analyses.append(analysis)

        if analysis.severity == "CRITICAL":
            critical_count += 1
        elif analysis.severity == "MODERATE":
            moderate_count += 1

    # PASO 2: Calcular threshold
    total_functions = len(functions)
    critical_rate = critical_count / total_functions if total_functions > 0 else 0.0

    # PASO 3: Decisión
    is_passing = critical_rate <= 0.50

    # PASO 4: Generar flags consolidados
    flags = self._generate_criterion_3_flags(function_analyses)

    # PASO 5: Confianza
    confidence = self._calculate_criterion_3_confidence(function_analyses)

    return Criterion3Evaluation(
        result="PASS" if is_passing else "FAIL",
        total_functions=total_functions,
        functions_critical=critical_count,
        functions_moderate=moderate_count,
        critical_rate=critical_rate,
        function_analyses=function_analyses,
        flags_detected=flags,
        confidence=confidence,
        reasoning=self._generate_criterion_3_reasoning(
            is_passing, critical_rate, function_analyses
        )
    )
```

#### Análisis de Función Individual

```python
def _analyze_single_function_impact(
    self,
    func: Dict[str, Any],
    nivel: str,
    appropriate_verbs: List[str],
    forbidden_verbs: List[str],
    expected_impact: Dict[str, str]
) -> FunctionImpactAnalysis:
    """Analiza una función individual en 4 pasos"""

    descripcion = func.get("descripcion_completa", "")
    que_hace = func.get("que_hace", "")
    para_que = func.get("para_que_lo_hace", "")

    # PASO 1: Extraer verbo principal
    verbo = self._extract_main_verb(que_hace)

    # PASO 2: Verificar apropiación de verbo
    es_apropiado = verbo.lower() in [v.lower() for v in appropriate_verbs]
    es_prohibido = verbo.lower() in [v.lower() for v in forbidden_verbs]

    # PASO 3: Analizar impacto (usando lógica de v4)
    impact_analysis = self._analyze_impact_indicators([func])

    detected_scope = impact_analysis["detected_scope"]
    detected_budget = impact_analysis["detected_budget"]
    detected_complexity = impact_analysis["detected_complexity"]

    # Inferir consecuencias
    detected_consequences = self._infer_consequences(
        detected_complexity, detected_scope
    )

    # PASO 4: Verificar coherencia con perfil esperado
    scope_coherent = self._check_scope_coherence(
        detected_scope, expected_impact.get("decision_scope")
    )
    budget_coherent = self._check_budget_coherence(
        detected_budget, expected_impact.get("budget_range")
    )
    consequences_coherent = self._check_consequences_coherence(
        detected_consequences, expected_impact.get("error_consequences")
    )

    # PASO 5: Determinar si hay discrepancia
    has_discrepancy = (
        es_prohibido or
        not es_apropiado or
        not scope_coherent or
        not consequences_coherent
        # budget_coherent es opcional (tolerancia amplia)
    )

    # PASO 6: Buscar respaldo normativo si hay discrepancia
    normative_backing = None
    normative_confidence = 0.0
    severity = "NONE"
    issue = None

    if has_discrepancy:
        # Buscar en normativa
        search_results = self.normativa_loader.search_all_documents(
            query=f"{que_hace} {para_que}",
            max_results=3
        )

        if search_results and search_results[0].similarity_score > 0.7:
            # HAY respaldo → MODERATE (anotación)
            normative_backing = search_results[0].content_snippet
            normative_confidence = search_results[0].similarity_score
            severity = "MODERATE"
            issue = f"Discrepancia detectada pero respaldada por normativa"
        else:
            # NO hay respaldo → CRITICAL
            severity = "CRITICAL"

            if es_prohibido:
                issue = f"Verbo prohibido '{verbo}' para nivel {nivel}"
            elif not es_apropiado:
                issue = f"Verbo '{verbo}' no apropiado para nivel {nivel}"
            elif not scope_coherent:
                issue = f"Alcance detectado '{detected_scope}' no coherente con nivel {nivel}"
            elif not consequences_coherent:
                issue = f"Consecuencias '{detected_consequences}' no coherentes con nivel {nivel}"

    return FunctionImpactAnalysis(
        funcion_id=func.get("id", ""),
        descripcion=descripcion,
        que_hace=que_hace,
        para_que_lo_hace=para_que,
        verbo_principal=verbo,
        es_verbo_apropiado=es_apropiado,
        es_verbo_prohibido=es_prohibido,
        detected_scope=detected_scope,
        detected_budget=detected_budget,
        detected_consequences=detected_consequences,
        detected_complexity=detected_complexity,
        scope_coherent=scope_coherent,
        budget_coherent=budget_coherent,
        consequences_coherent=consequences_coherent,
        normative_backing=normative_backing,
        normative_confidence=normative_confidence,
        severity=severity,
        issue_detected=issue,
        suggested_fix=self._generate_fix_suggestion(
            issue, verbo, nivel, appropriate_verbs[:3]
        ) if issue else None
    )
```

### Ventajas del Enfoque Propuesto

1. ✅ **Combina verbos + complemento**: No solo verbo, sino "para qué lo hace"
2. ✅ **Evalúa impacto multidimensional**: 4 dimensiones (scope, budget, consequences, complexity)
3. ✅ **Respaldo normativo inteligente**: Distingue anotaciones de fallos reales
4. ✅ **Threshold flexible**: 50% permite tolerancia realista
5. ✅ **Compatible con v4**: Usa VERB_HIERARCHY existente
6. ✅ **Mejora v4**: Añade validación normativa de discrepancias

---

## 🚀 Plan de Implementación en v5

### Fase 1: Preparación (1-2 horas)

1. ✅ Crear este documento de análisis
2. ⏳ Migrar `VERB_HIERARCHY` de v4 a v5
3. ⏳ Crear dataclasses (`FunctionImpactAnalysis`, `Criterion3Evaluation`)

### Fase 2: Implementación Core (3-4 horas)

1. ⏳ Implementar `_analyze_impact_indicators()` (portar desde v4)
2. ⏳ Implementar `_analyze_single_function_impact()`
3. ⏳ Implementar `_evaluate_criterion_3_hierarchical_impact()`
4. ⏳ Integrar con sistema de validación existente

### Fase 3: Testing (1-2 horas)

1. ⏳ Probar con caso TURISMO (25 puestos)
2. ⏳ Validar threshold 50%
3. ⏳ Verificar respaldo normativo funciona

### Fase 4: Documentación (1 hora)

1. ⏳ Actualizar `FLUJO_ANALISIS_DETALLADO.md`
2. ⏳ Crear ejemplos de evaluación
3. ⏳ Documentar matriz de decisión 2-of-3

---

## 📊 Comparativa Final

| Aspecto | v4 | v5 Actual | v5 Propuesto |
|---------|----|-----------|--------------|
| **Criterio 1: Verbos Débiles** | ✅ Threshold 50% | ✅ Threshold 50% | ✅ Mantenido |
| **Criterio 2: Impacto** | ✅ 3 dimensiones | ❌ Solo institucional | ✅ 4 dimensiones + normativa |
| **Criterio 3: Compliance** | ✅ Normativo básico | ❌ No existe | ✅ Apropiación jerárquica |
| **Complemento/"para qué?"** | ✅ Analizado | ❌ No usado | ✅ Analizado + validado |
| **Respaldo normativo** | ⚠️ Parcial | ⚠️ Solo referencias | ✅ Por función con threshold |
| **Matriz 2-of-3** | ✅ Implementada | ❌ No existe | ✅ Reimplementar |
| **LLM para impacto** | ✅ Opcional | ❌ No | ✅ Recomendado |

---

## 🎯 Decisión Recomendada

### Opción A: Implementar 3 Criterios Separados (v4-style)

**Ventaja**: Clara separación de responsabilidades
**Desventaja**: Más complejo de mantener

```
Criterio 1: Congruencia de Verbos (weak verbs)
Criterio 2: Impacto Multidimensional (scope + budget + consequences)
Criterio 3: Apropiación Jerárquica (verb hierarchy + normativa)
```

### Opción B: Fusionar Criterios 2+3 (Simplificado)

**Ventaja**: Menos código duplicado
**Desventaja**: Pierde granularidad de v4

```
Criterio 1: Congruencia de Verbos
Criterio 2: Apropiación de Impacto Jerárquico
  └─ Verbos apropiados
  └─ Impacto multidimensional
  └─ Validación normativa
```

### ✅ Recomendación: **Opción A**

**Justificación**:
1. Mantiene compatibilidad conceptual con v4
2. Permite matriz 2-of-3 más flexible
3. Facilita debugging (cada criterio independiente)
4. Usuario mencionó "SISTEMA COMPLETO DE 3 CRITERIOS"

---

## 📝 Siguiente Paso

**Pregunta para el usuario**:

> He analizado completamente v4 y encontré que:
>
> 1. **v4 YA tiene evaluación de impacto funcional** (Criterio 2) que incluye:
>    - Análisis del complemento/"para qué?"
>    - Detección de alcance de decisiones
>    - Magnitud presupuestaria
>    - Consecuencias de errores
>
> 2. **v4 usa matriz 2-of-3** para decisión final
>
> 3. **Tu propuesta mejora esto** añadiendo validación normativa de discrepancias
>
> **¿Quieres que implemente**:
> - **Opción A**: 3 criterios separados (como v4) + mejora de respaldo normativo
> - **Opción B**: 2 criterios fusionando impacto + apropiación jerárquica
>
> **Mi recomendación**: Opción A (3 criterios) para mantener la matriz 2-of-3 que funciona bien en v4.

---

**Documento creado**: 2025-11-05
**Análisis basado en**:
- `/home/alfred/HerramientaHomologaci-nDocker/notebooks/agente_2_evaluador.py`
- `/home/alfred/HerramientaHomologaci-nDocker/notebooks/shared_utilities.py`
- `/home/alfred/HerramientaHomologaci-nDocker/notebooks/contextual_verb_validator.py`
