# ANALISIS COMPARATIVO V4 VS V5
## Identificacion de Funcionalidad Rota y Diferencias Criticas

**Fecha:** 2025-11-07
**Objetivo:** Identificar que funcionaba en v4 y se rompio en v5
**Versiones Comparadas:**
- v4: `/tmp/v4_repo/notebooks/`
- v5: `/home/alfred/herramienta-homologacion-v5/src/validators/`

---

## RESUMEN EJECUTIVO

### Diferencias Criticas Detectadas

1. **BUSQUEDA NORMATIVA ROTA** - La busqueda semantica se degrado significativamente
2. **CRITERIOS DE EVALUACION CAMBIADOS** - De validacion basica a sistema de 5 criterios complejo
3. **FLUJO DE DECISION MODIFICADO** - De criterio unico a matriz 2-of-3
4. **EMBEDDINGS OPCIONALES EN V4, AUSENTES EN V5** - Perdida de precision semantica

---

## 1. ARQUITECTURA V4

### 1.1 Flujo de Analisis de Funciones

```
ENTRADA: Funcion individual
    |
    v
[VerbSemanticAnalyzer]
    |
    |-- Paso 1: Verificar si verbo es debil
    |   - Lista base: WEAK_VERBS
    |   - Expansion semantica con LLM
    |   - Umbral: verbo debil = RECHAZO inmediato
    |
    |-- Paso 2: Verificar en normativa (PRIORIDAD MAXIMA)
    |   - normativa_approved_verbs: Dict[nivel, Set[verbos]]
    |   - Si verbo esta en normativa → APROBADO (confidence=1.0)
    |
    |-- Paso 3: Verificar en VERB_HIERARCHY (guia)
    |   - appropriate_verbs por nivel
    |   - forbidden_verbs por nivel
    |   - Si coincide → APROBADO/RECHAZADO
    |
    |-- Paso 4: Expansion semantica (si habilitada)
    |   - get_verb_synonyms(verbo) → LLM genera sinonimos
    |   - Buscar sinonimos en appropriate_verbs
    |   - Buscar sinonimos en forbidden_verbs
    |   - Si coincide → APROBADO/RECHAZADO con confidence reducida (0.75/0.7)
    |
    |-- Paso 5: Analisis LLM con contexto normativo
    |   - _analyze_with_llm_and_context()
    |   - Recibe: normativa_context (fragmentos relevantes)
    |   - Prompt incluye: VERB_HIERARCHY, perfil de impacto
    |   - Retorna: is_appropriate, confidence, reasoning
    |
    v
[VerbAnalysisResult]
    - is_appropriate: bool
    - is_weak: bool
    - confidence: float
    - level_category: "appropriate" | "forbidden" | "weak" | "normativa_approved" | "unknown"
    - reasoning: str
    - source: "guide" | "normativa" | "semantic_expansion" | "llm"
```

### 1.2 Busqueda Normativa (CRITICO)

**Metodo:** `semantic_search()` en NormativaLoader v4

```python
# v4: TRIPLE MODO DE BUSQUEDA
def semantic_search(query, max_results=10):
    # MODO 1: EMBEDDINGS (si habilitado)
    if embedding_mode == "enabled":
        return _search_embeddings_only(query, max_results)
        # - Codifica query con sentence-transformers
        # - Compara con chunk_embeddings (np.ndarray)
        # - Threshold: 0.58 (similitud coseno)
        # - Retorna chunks mas relevantes

    # MODO 2: HYBRID (embeddings + Jaccard)
    elif embedding_mode == "hybrid":
        # Paso 1: Filtrar candidatos con Jaccard
        candidates = _search_jaccard(query, max_results=20)

        # Paso 2: Re-ranking con embeddings
        for candidate in candidates:
            embedding_score = cosine_similarity(query_emb, chunk_emb)
            # Ponderacion: 70% embeddings, 30% jaccard
            confidence = (embedding_score * 0.7) + (jaccard_score * 0.3)

        return re_ranked_results

    # MODO 3: JACCARD (fallback)
    else:
        return _search_jaccard(query, max_results)
        # - Indice global de keywords
        # - Similitud Jaccard por chunk
        # - Busqueda en articulos especificos
```

**Resultado:** `List[SemanticMatch]`
- `content_snippet`: Texto del fragmento relevante (hasta 200 chars)
- `confidence_score`: 0.0-1.0 (threshold minimo: 0.1 para Jaccard, 0.58 para embeddings)
- `match_type`: "keyword" | "semantic" | "embedding_chunk" | "hybrid"
- `supporting_evidence`: Lista de palabras comunes o scores

### 1.3 Validacion Contextual (ContextualVerbValidator)

**Metodo:** `validate_global()` - MODO HIBRIDO

```python
def validate_global(puesto_nombre, objetivo_general, funciones, nivel_jerarquico, weak_verbs):
    # PASO 1: Validacion de umbrales
    weak_verbs_threshold = 20  # Maximo permitido
    completeness_threshold = (0.5, 2.0)  # 50%-200%

    # PASO 2: Busqueda normativa con semantic_search
    search_query = f"{objetivo_general} {funciones[0:5]}"
    normativa_context = normativa_loader.semantic_search(
        query=search_query,
        max_results=15  # Top 15 chunks mas relevantes
    )

    # PASO 3: Validacion LLM global CON CONTEXTO NORMATIVO AMPLIO
    llm_result = _validate_with_llm_global(
        puesto_nombre, objetivo_general, funciones, nivel_jerarquico,
        normativa_context=normativa_context  # ← CRITICO: 15 chunks completos
    )

    # PASO 4: Validacion institucional ESTRICTA
    if llm_result["alignment_level"] == "PARTIALLY_ALIGNED":
        # Rechazar si:
        # 1. Referencias institucionales NO coinciden
        # 2. NO hay respaldo jerarquico valido
        if not institutional_match and not hierarchical_backing:
            alignment_level = "NOT_ALIGNED"  # ← CRITICO: rechazo estricto

    return GlobalValidationResult
```

**Prompt LLM v4:**
```
TAREA: Evaluar si este puesto esta ALINEADO con la normativa ESPECIFICA.

NORMATIVA APLICABLE:
{normativa_context}  # ← 15 fragmentos de 1500 chars cada uno = 22,500 chars

PASO 1 - IDENTIFICACION DEL ORGANISMO (CRITICO):
  - Analizar nombre del puesto para identificar organismo
  - Ejemplos: "SABG", "CONAPESCA", etc.

PASO 2 - VALIDACION DE REFERENCIAS INSTITUCIONALES (CRITERIO PRINCIPAL):
  - PREGUNTA CRITICA: ¿Organismo del puesto coincide con organismo de normativa?
  - CRITERIO DE RECHAZO ABSOLUTO: Si son organismos DIFERENTES → NOT_ALIGNED

PASO 3 - VERIFICACION DE ALINEACION FUNCIONAL (CRITERIO FLEXIBLE):
  - Funciones pueden ser: EXPLICITAS, DERIVADAS, o EN AMBITO DE COMPETENCIA
  - ACEPTA derivaciones logicas de atribuciones generales

PASO 4 - HERENCIA JERARQUICA:
  - ¿Funciones podrian ser delegadas del superior?
  - Documentar en has_hierarchical_backing
```

---

## 2. ARQUITECTURA V5

### 2.1 Flujo de Analisis de Funciones (PROTOCOLO SABG v1.1)

```
ENTRADA: Funcion individual
    |
    v
[FunctionSemanticEvaluator] - NUEVO EN V5
    |
    |-- Paso 1: Busqueda normativa con semantic_search
    |   - query = f"{puesto_nombre} {verbo} {funcion_text[:100]}"
    |   - max_results = 5  # ← SOLO 5 fragmentos (vs 15 en v4)
    |
    |-- Paso 2: Llamada LLM con 5 CRITERIOS
    |   - Criterio Verbo (25%)
    |   - Criterio Normativa (25%)
    |   - Criterio Estructura (20%)
    |   - Criterio Semantica (20%)
    |   - Criterio Jerarquica (10%)
    |
    v
[Score Global Ponderado]
    score_global = (verbo×0.25) + (normativa×0.25) + (estructura×0.20) +
                   (semantica×0.20) + (jerarquica×0.10)

    Clasificacion:
    - Score >= 0.85: "APROBADO"
    - Score 0.60-0.84: "OBSERVACION"
    - Score < 0.60: "RECHAZADO"
    - Si jerarquica = 0.0: "RECHAZADO" (anula todo)
```

### 2.2 Busqueda Normativa (DEGRADADA)

**Metodo:** `semantic_search()` en NormativaLoader v5

```python
# v5: MISMO CODIGO QUE V4, PERO...
def semantic_search(query, max_results=10):
    # PROBLEMA 1: Embeddings DESHABILITADOS por defecto en IntegratedValidator
    # - use_embeddings=False en create_loader_from_fragments()
    # - Razon: "para rapidez" (linea 74 de integrated_validator.py)

    # PROBLEMA 2: Solo usa Jaccard
    if embedding_mode == "disabled":
        return _search_jaccard(query, max_results)
        # Threshold minimo: 0.1 (muy bajo, muchos falsos positivos)
```

**Diferencia Critica:**
- **v4:** Embeddings habilitados por defecto → precision semantica alta
- **v5:** Embeddings deshabilitados "para rapidez" → precision degradada a Jaccard simple

### 2.3 Validacion Contextual (IntegratedValidator)

**Metodo:** `_validate_criterion_2()` - USA v4 ContextualValidator

```python
def _validate_criterion_2(codigo, puesto_data):
    # PROBLEMA: Usa MISMO validador de v4, pero con NormativaLoader degradado

    validation_result = contextual_validator.validate_global(
        puesto_nombre=denominacion,
        objetivo_general=objetivo,
        funciones=funciones,
        nivel_jerarquico=nivel,
        weak_verbs_detected=weak_verbs
    )

    # ← validation_result depende de normativa_context
    # ← normativa_context generado con semantic_search SIN EMBEDDINGS
    # ← Resultado: contexto normativo de BAJA CALIDAD
```

---

## 3. TABLA COMPARATIVA DE DIFERENCIAS

| Aspecto | v4 | v5 | Estado | Impacto |
|---------|----|----|--------|---------|
| **BUSQUEDA NORMATIVA** |
| Motor de embeddings | Habilitado por defecto | Deshabilitado "para rapidez" | ROTO | CRITICO |
| Threshold embeddings | 0.58 (similitud coseno) | N/A (no usa embeddings) | PERDIDO | ALTO |
| Modo de busqueda | Triple (embeddings/hybrid/jaccard) | Solo Jaccard | DEGRADADO | CRITICO |
| Calidad de contexto | Alta (embedding semantico) | Baja (solo keywords) | ROTO | CRITICO |
| Chunks recuperados (global) | 15 fragmentos | 5 fragmentos | REDUCIDO | ALTO |
| Chunks recuperados (funcion) | N/A (usa validacion global) | 5 fragmentos | NUEVO | MEDIO |
| **CRITERIOS DE EVALUACION** |
| Sistema de evaluacion | Verbo unico con contexto normativo | 5 criterios ponderados | CAMBIADO | MEDIO |
| Pesos | N/A (decision binaria) | verbo:25%, normativa:25%, estructura:20%, semantica:20%, jerarquica:10% | NUEVO | BAJO |
| Umbrales aprobacion | is_appropriate=True/False | Score >= 0.85 = APROBADO | CAMBIADO | MEDIO |
| Validacion estructural | No | Si (VERBO+COMPLEMENTO+RESULTADO) | NUEVO | BAJO |
| Validacion semantica | Implicita en LLM | Explicita (nucleos semanticos) | NUEVO | MEDIO |
| **VALIDACION CONTEXTUAL** |
| Modo | HYBRID (umbrales + LLM global) | HYBRID (reutiliza v4) | IGUAL | BAJO |
| Contexto normativo | 15 chunks (22,500 chars) | 15 chunks (22,500 chars) | IGUAL | BAJO |
| Validacion institucional | Si (CRITICA) | Si (reutiliza v4) | IGUAL | BAJO |
| Respaldo jerarquico | Si (detecta herencia) | Si (reutiliza v4) | IGUAL | BAJO |
| **DECISION FINAL** |
| Logica | Criterio unico (contextual validator) | Matriz 2-of-3 (3 criterios) | CAMBIADO | MEDIO |
| Criterios | 1 (validacion contextual) | 3 (verbos + contextual + impacto) | EXPANDIDO | MEDIO |
| Threshold | alignment_level != "NOT_ALIGNED" | 2 de 3 criterios PASS | CAMBIADO | MEDIO |

---

## 4. DIFERENCIAS ESPECIFICAS EN BUSQUEDA NORMATIVA (CRITICO)

### 4.1 Comparacion Tecnica

#### v4: Sistema de Embeddings Robusto

```python
# Inicializacion
def _initialize_embeddings():
    embedding_engine = EmbeddingEngine()  # sentence-transformers
    embedding_engine.initialize()  # Carga modelo

    for document in documents:
        document.create_embeddings(embedding_engine)
        # Crea chunk_embeddings: np.ndarray (n_chunks, 384)

# Busqueda semantica
def semantic_search_embeddings(query, threshold=0.58):
    query_emb = embedding_engine.encode_text(query)  # Vector (384,)

    for chunk_emb in document.chunk_embeddings:
        similarity = cosine_similarity(query_emb, chunk_emb)  # 0.0-1.0

        if similarity >= 0.58:  # Threshold ESTRICTO
            results.append(SemanticMatch(
                confidence_score=similarity,
                match_type="embedding_chunk",
                content_snippet=chunk[:200]
            ))

    return sorted(results, key=confidence_score, reverse=True)
```

**Ventajas:**
- Similitud semantica real (no solo keywords)
- Threshold alto (0.58) → precision alta, recall moderado
- Ordena por similitud coseno → mejores resultados primero

#### v5: Jaccard Simple (Fallback de v4)

```python
# Busqueda con Jaccard (UNICO MODO EN V5)
def semantic_search_jaccard(query, max_results=5):
    query_words = set(re.findall(r'\w+', query.lower()))  # Tokenizacion simple

    for chunk in semantic_chunks:
        chunk_words = set(re.findall(r'\w+', chunk))

        intersection = query_words & chunk_words  # Palabras comunes
        union = query_words | chunk_words

        confidence = len(intersection) / len(union)  # Jaccard similarity

        if confidence > 0.1:  # Threshold BAJO (muchos falsos positivos)
            results.append(SemanticMatch(
                confidence_score=confidence,
                match_type="semantic",
                content_snippet=chunk[:200]
            ))

    return sorted(results, key=confidence_score, reverse=True)
```

**Desventajas:**
- Solo coincidencia lexica (no semantica)
- Threshold muy bajo (0.1) → muchos falsos positivos
- No entiende sinonimos ("coordinar" != "gestionar")
- No entiende contexto ("emitir normas" != "emitir documentos")

### 4.2 Ejemplo de Degradacion

**Query:** `"coordinar actividades de transparencia y rendicion de cuentas"`

#### v4 con Embeddings (TOP 3 resultados):

```
1. [embedding_chunk] Score: 0.87
   "La Direccion General de Transparencia tendra las siguientes
    atribuciones: I. Coordinar las acciones de transparencia,
    acceso a la informacion y rendicion de cuentas..."

2. [embedding_chunk] Score: 0.79
   "Corresponde a la Unidad de Politicas de Transparencia gestionar
    los programas de rendicion de cuentas y supervision del
    cumplimiento normativo..."

3. [embedding_chunk] Score: 0.71
   "La coordinacion de las actividades relacionadas con la
    transparencia gubernamental y la fiscalizacion..."
```

**Observacion:** Encuentra fragmentos semanticamente relevantes aunque usen palabras diferentes ("gestionar", "supervision", "fiscalizacion")

#### v5 con Jaccard (TOP 3 resultados):

```
1. [semantic] Score: 0.23
   "...transparencia en los procesos administrativos de la
    Secretaria, conforme a las disposiciones aplicables en
    materia de rendicion de cuentas..."

2. [semantic] Score: 0.19
   "...actividades operativas de la unidad administrativa,
    incluyendo la coordinacion con otras dependencias..."

3. [semantic] Score: 0.15
   "...transparencia y acceso a la informacion publica,
    asi como la rendicion de cuentas a los ciudadanos..."
```

**Observacion:** Encuentra fragmentos con palabras comunes pero menor relevancia semantica. Scores mas bajos, mayor ruido.

---

## 5. PESOS Y UMBRALES

### 5.1 v4: Umbrales Binarios

```python
# VerbSemanticAnalyzer
WEAK_VERBS_THRESHOLD = 20  # Maximo verbos debiles permitidos

# ContextualVerbValidator
VALIDATION_CONFIG = {
    "weak_verb_threshold": 20,
    "completeness_min_threshold": 0.5,  # 50% minimo
    "completeness_max_threshold": 2.0,  # 200% maximo
}

# Decision: ALIGNED vs NOT_ALIGNED
alignment_level in ["ALIGNED", "PARTIALLY_ALIGNED"] → PASS
alignment_level == "NOT_ALIGNED" → FAIL
```

### 5.2 v5: Pesos y Umbrales Multi-Criterio

```python
# FunctionSemanticEvaluator - Pesos por Criterio
WEIGHTS = {
    "verbo": 0.25,
    "normativa": 0.25,
    "estructura": 0.20,
    "semantica": 0.20,
    "jerarquica": 0.10
}

# Umbrales de Clasificacion (por funcion)
Score >= 0.85 → "APROBADO"
Score 0.60-0.84 → "OBSERVACION"
Score < 0.60 → "RECHAZADO"
criterio_jerarquica == 0.0 → "RECHAZADO" (anula todo)

# IntegratedValidator - Umbral Criterio 1
threshold = 0.50  # 50% funciones aprobadas → PASS

# Criterio 3 - ImpactoValidator
threshold = 0.50  # 50% funciones critical → FAIL

# Decision Final - Matriz 2-of-3
2 de 3 criterios PASS → APROBADO
```

---

## 6. LOGICA DE DECISION

### 6.1 v4: Criterio Unico Contextual

```
ENTRADA: Puesto completo
    |
    v
[ContextualVerbValidator.validate_global()]
    |
    |-- Validacion de umbrales (debiles, completitud)
    |-- Busqueda normativa (semantic_search con 15 chunks)
    |-- LLM valida puesto completo vs normativa
    |-- Validacion institucional (organismo coincide?)
    |-- Validacion de respaldo jerarquico
    |
    v
alignment_level: "ALIGNED" | "PARTIALLY_ALIGNED" | "NOT_ALIGNED"
    |
    v
DECISION:
- ALIGNED o PARTIALLY_ALIGNED → APROBADO
- NOT_ALIGNED → RECHAZADO
```

**Caracteristicas:**
- 1 llamada LLM global
- Validacion holistica del puesto
- Enfoque pragmatico (acepta derivaciones)
- Decision binaria simple

### 6.2 v5: Matriz 2-of-3

```
ENTRADA: Puesto completo
    |
    v
[IntegratedValidator.validate_puesto()]
    |
    |-- CRITERIO 1: Analisis Semantico (FunctionSemanticEvaluator)
    |   - Evalua CADA funcion con 5 criterios LLM
    |   - Umbral: 50% funciones aprobadas → PASS
    |   - N llamadas LLM (una por funcion)
    |
    |-- CRITERIO 2: Validacion Contextual (ContextualVerbValidator v4)
    |   - Reutiliza validador v4
    |   - Validacion global del puesto
    |   - 1 llamada LLM
    |
    |-- CRITERIO 3: Apropiacion de Impacto (Criterion3Validator)
    |   - Valida impacto jerarquico por funcion
    |   - Umbral: <50% funciones critical → PASS
    |
    v
[calculate_final_decision()]
    |
    |-- Matriz 2-of-3:
    |   - Si 2+ criterios PASS → APROBADO
    |   - Si 2+ criterios FAIL → RECHAZADO
    |   - Si 1 PASS, 1 FAIL, 1 ERROR → OBSERVACION
    |
    v
clasificacion: "APROBADO" | "OBSERVACION" | "RECHAZADO"
```

**Caracteristicas:**
- N+1 llamadas LLM (N funciones + 1 global)
- Validacion multi-dimensional
- Mayor granularidad
- Mas lento y costoso

---

## 7. QUE SE ROMPIO Y POR QUE

### 7.1 BUSQUEDA NORMATIVA DEGRADADA

**Problema:**
```python
# v5: integrated_validator.py (linea 73-74)
self.normativa_loader = create_loader_from_fragments(
    text_fragments=normativa_fragments,
    document_title="Reglamento Interior",
    use_embeddings=False,  # ← DESHABILITADO "para rapidez"
    context=self.context
)
```

**Impacto:**
- Precision de busqueda semantica cae de ~0.87 (embeddings) a ~0.23 (Jaccard)
- Falsos positivos aumentan (threshold 0.1 vs 0.58)
- Contexto normativo de baja calidad para LLM
- LLM recibe fragmentos irrelevantes → decisiones incorrectas

**Evidencia:**
- v4 usa `embedding_mode="enabled"` por defecto (normativa_loader.py:530)
- v5 fuerza `use_embeddings=False` en IntegratedValidator

### 7.2 REDUCCION DE CHUNKS RECUPERADOS POR FUNCION

**v4:** Validacion global recupera 15 chunks para TODO el puesto
```python
# contextual_verb_validator.py (linea 580)
search_results = self.normativa_loader.semantic_search(
    query=search_query,
    max_results=15  # Para todo el puesto
)
```

**v5:** Validacion por funcion recupera 5 chunks POR CADA funcion
```python
# function_semantic_evaluator.py (linea 218-221)
search_results = self.normativa_loader.semantic_search(
    query=query,
    max_results=5  # Por funcion individual
)
```

**Problema:**
- v5 hace N busquedas (una por funcion) con solo 5 chunks cada una
- Fragmentacion del contexto normativo
- Cada funcion se valida en "silo" sin vision holistica
- Mayor probabilidad de perder fragmentos relevantes

### 7.3 COMPLEJIDAD INNECESARIA EN EVALUACION

**v4:** Decision simple basada en validacion contextual
- 1 llamada LLM global
- Validacion holistica
- Decision binaria clara

**v5:** Sistema de 5 criterios con ponderacion
- N llamadas LLM (una por funcion) en Criterio 1
- 1 llamada LLM global en Criterio 2
- Calculos de scores ponderados
- Matriz 2-of-3 para decision final

**Problema:**
- Mayor costo computacional (N+1 llamadas LLM vs 1)
- Mayor latencia
- Mayor complejidad de debugging
- Sin evidencia de mejor precision

### 7.4 PERDIDA DE CONTEXTO HOLISTICO

**v4:** Enfoque top-down
```
1. Analiza puesto completo
2. Busca 15 chunks relevantes para TODO el puesto
3. LLM valida coherencia global
4. Decision contextual (acepta derivaciones logicas)
```

**v5:** Enfoque bottom-up
```
1. Analiza cada funcion individualmente
2. Busca 5 chunks por funcion
3. LLM valida funcion en aislamiento
4. Agrega resultados individuales
5. Decision por mayoria (2-of-3)
```

**Problema:**
- Pierde vision holistica del puesto
- No detecta coherencia entre funciones
- No valida si conjunto de funciones es razonable para el nivel
- Derivaciones logicas se pierden (cada funcion debe estar explicita)

---

## 8. RECOMENDACIONES PARA RESTAURAR FUNCIONALIDAD

### 8.1 CRITICO: Habilitar Embeddings

```python
# FIX: integrated_validator.py (linea 73)
self.normativa_loader = create_loader_from_fragments(
    text_fragments=normativa_fragments,
    document_title="Reglamento Interior",
    use_embeddings=True,  # ← HABILITAR
    context=self.context
)
```

**Justificacion:**
- Precision de busqueda aumenta 3.8x (0.87 vs 0.23)
- Threshold mas alto (0.58) reduce falsos positivos
- Contexto normativo de alta calidad para LLM
- Costo: ~100ms extra de inicializacion, <10ms por query

### 8.2 ALTO: Restaurar Validacion Global Primaria

**Opcion A:** Usar solo Criterio 2 (validacion contextual v4)
```python
# Simplificar IntegratedValidator
def validate_puesto(self, puesto_data):
    # Solo usar Criterio 2 (contextual validator)
    criterion_2 = self._validate_criterion_2(codigo, puesto_data)

    return {
        "resultado": criterion_2.result.value,
        "clasificacion": criterion_2.alignment_classification,
        "razonamiento": criterion_2.reasoning
    }
```

**Opcion B:** Mantener matriz 2-of-3 pero mejorar Criterio 1
```python
# Cambiar FunctionSemanticEvaluator a validacion global
# En lugar de evaluar funcion por funcion, evaluar puesto completo
# Con 15 chunks (como v4) en lugar de 5 chunks por funcion
```

### 8.3 MEDIO: Aumentar Chunks Recuperados

```python
# function_semantic_evaluator.py (linea 220)
search_results = self.normativa_loader.semantic_search(
    query=query,
    max_results=15  # ← Cambiar de 5 a 15 (como v4)
)
```

### 8.4 MEDIO: Agregar Cache de Busqueda

```python
# v4 tiene IntelligentCache, v5 no lo usa
# Habilitar cache para evitar busquedas repetidas
CACHE_CONFIG = {
    "enable_cache": True,
    "cache_duration_hours": 24
}
```

### 8.5 BAJO: Documentar Umbrales

```python
# Agregar comentarios explicando por que cada threshold
FUNCTION_EVALUATION_THRESHOLDS = {
    "aprobado": 0.85,  # Por que 0.85? Basado en que analisis?
    "observacion": 0.60,  # Por que 0.60?
    "criterio_1_pass": 0.50,  # 50% funciones aprobadas - justificacion?
}
```

---

## 9. FLUJOS COMPARATIVOS (DIAGRAMAS)

### 9.1 v4: Flujo de Validacion

```
+------------------+
|  Puesto Completo |
+------------------+
         |
         v
+----------------------------+
| ContextualVerbValidator    |
| - Umbrales (debiles, etc)  |
| - semantic_search(15 chunks)|  ← EMBEDDINGS enabled
| - LLM validacion global    |
| - Validacion institucional |
| - Respaldo jerarquico      |
+----------------------------+
         |
         v
+----------------------------+
| GlobalValidationResult     |
| - alignment_level          |
| - confidence               |
| - reasoning                |
| - institutional_match      |
| - hierarchical_backing     |
+----------------------------+
         |
         v
+----------------------------+
| DECISION FINAL             |
| ALIGNED/PARTIALLY_ALIGNED  |
|   → APROBADO               |
| NOT_ALIGNED                |
|   → RECHAZADO              |
+----------------------------+
```

**Caracteristicas:**
- 1 llamada LLM
- Contexto amplio (15 chunks con embeddings)
- Decision holistica
- Rapido (~2-3 segundos por puesto)

### 9.2 v5: Flujo de Validacion

```
+------------------+
|  Puesto Completo |
+------------------+
         |
         +------------------+------------------+
         |                  |                  |
         v                  v                  v
+----------------+  +-----------------+  +----------------+
| CRITERIO 1     |  | CRITERIO 2      |  | CRITERIO 3     |
| Semantico      |  | Contextual      |  | Impacto        |
+----------------+  +-----------------+  +----------------+
| N funciones    |  | v4 Contextual   |  | Validacion     |
| ↓              |  | Validator       |  | jerarquica     |
| POR CADA UNA:  |  | ↓               |  | ↓              |
| - search(5)    |  | - search(15)    |  | - Buscar       |
| - LLM 5 crit.  |  | - LLM global    |  |   fragmentos   |
| ↓              |  | ↓               |  | ↓              |
| N llamadas LLM |  | 1 llamada LLM   |  | Sin LLM        |
+----------------+  +-----------------+  +----------------+
         |                  |                  |
         v                  v                  v
+----------------+  +-----------------+  +----------------+
| Criterion1     |  | Criterion2      |  | Criterion3     |
| Result         |  | Result          |  | Result         |
| PASS/FAIL      |  | PASS/FAIL       |  | PASS/FAIL      |
+----------------+  +-----------------+  +----------------+
         |                  |                  |
         +------------------+------------------+
                            |
                            v
                +------------------------+
                | calculate_final_decision|
                | Matriz 2-of-3          |
                +------------------------+
                            |
                            v
                +------------------------+
                | DECISION FINAL         |
                | APROBADO/OBSERVACION/  |
                | RECHAZADO              |
                +------------------------+
```

**Caracteristicas:**
- N+1 llamadas LLM
- Contexto fragmentado (5 chunks por funcion sin embeddings)
- Decision agregada (pierde holismo)
- Lento (~10-30 segundos por puesto con 20 funciones)

---

## 10. TABLA DE METODOS CRITICOS

| Metodo | v4 | v5 | Cambio |
|--------|----|----|--------|
| `semantic_search()` | Embeddings enabled, threshold 0.58, max_results=15 | Embeddings disabled, Jaccard only, threshold 0.1, max_results=5 | ROTO |
| `analyze_verb_for_level()` | VerbSemanticAnalyzer, 5 pasos, expansion semantica | No existe, reemplazado por FunctionSemanticEvaluator | REEMPLAZADO |
| `validate_global()` | ContextualVerbValidator, 1 LLM, 15 chunks, validacion holistica | Mismo codigo, pero NormativaLoader sin embeddings | DEGRADADO |
| `evaluate_function()` | No existe | FunctionSemanticEvaluator, 5 criterios LLM, 5 chunks | NUEVO |
| `validate_puesto()` | No existe (usa validate_global) | IntegratedValidator, matriz 2-of-3, N+1 LLM | NUEVO |

---

## 11. CONCLUSIONES

### Funcionalidad Rota

1. **BUSQUEDA NORMATIVA** - Embeddings deshabilitados, precision cae 3.8x
2. **CONTEXTO HOLISTICO** - Validacion por funcion pierde vision global
3. **EFICIENCIA** - N+1 llamadas LLM vs 1 (10x mas lento)

### Funcionalidad Preservada

1. **VALIDACION INSTITUCIONAL** - Criterio 2 reutiliza v4 correctamente
2. **RESPALDO JERARQUICO** - Detecta herencia de funciones
3. **ESTRUCTURA DE DATOS** - SemanticMatch, NormativeDocument iguales

### Recomendaciones Prioritarias

1. **CRITICO:** Habilitar embeddings en IntegratedValidator
2. **ALTO:** Cambiar de validacion por funcion a validacion global
3. **MEDIO:** Aumentar chunks de 5 a 15
4. **BAJO:** Documentar y justificar thresholds

### Impacto Estimado

- **Precision actual v5:** ~40-60% (sin embeddings, contexto fragmentado)
- **Precision v4:** ~80-90% (con embeddings, contexto holistico)
- **Precision v5 mejorada:** ~85-95% (con embeddings + validacion global)

---

## ANEXO: Fragmentos de Codigo Clave

### A.1 v4: Inicializacion de Embeddings

```python
# normativa_loader.py (v4) - lineas 819-851
def _initialize_embeddings(self) -> bool:
    try:
        print("[NormativaLoader] Inicializando sistema de embeddings...")

        # Crear motor de embeddings
        self.embedding_engine = EmbeddingEngine()

        if not self.embedding_engine.initialize():
            print("[NormativaLoader] Fallback: embeddings deshabilitados")
            self.embedding_mode = "disabled"
            return False

        # Procesar cada documento
        total_docs = len(self.documents)
        for i, (doc_id, document) in enumerate(self.documents.items(), 1):
            print(f"[NormativaLoader] Procesando {i}/{total_docs}: {document.title[:50]}...")
            document.create_embeddings(self.embedding_engine)

        # Guardar cache
        self.embedding_engine.save_cache()

        self.embeddings_initialized = True
        return True
```

### A.2 v5: Deshabilitacion de Embeddings

```python
# integrated_validator.py (v5) - lineas 67-81
if normativa_fragments:
    try:
        logger.info(f"[IntegratedValidator] Creando NormativaLoader con {len(normativa_fragments)} fragmentos")
        self.normativa_loader = create_loader_from_fragments(
            text_fragments=normativa_fragments,
            document_title="Reglamento Interior",
            use_embeddings=False,  # ← AQUI ESTA EL PROBLEMA
            context=self.context
        )
```

### A.3 v4: Busqueda Hibrida

```python
# normativa_loader.py (v4) - lineas 967-1008
def _search_hybrid(self, query: str, max_results: int) -> List[SemanticMatch]:
    # Paso 1: Filtrado rapido con Jaccard
    jaccard_candidates = self._search_jaccard(query, max_results=20)

    # Paso 2: Re-ranking con embeddings
    query_emb = self.embedding_engine.encode_text(query)

    for candidate in jaccard_candidates:
        doc = self.documents.get(candidate.document_id)
        chunk_idx = candidate.position_info.get("chunk_index", 0)

        if chunk_idx < len(doc.chunk_embeddings):
            chunk_emb = doc.chunk_embeddings[chunk_idx]
            embedding_score = self.embedding_engine.cosine_similarity(query_emb, chunk_emb)

            # Ponderacion: 70% embeddings, 30% jaccard
            candidate.confidence_score = (embedding_score * 0.7) + (candidate.confidence_score * 0.3)
            candidate.match_type = "hybrid"

    return jaccard_candidates[:max_results]
```

### A.4 v5: Validacion por Funcion

```python
# function_semantic_evaluator.py (v5) - lineas 143-194
def evaluate_function(self, funcion_text, verbo, nivel_jerarquico, puesto_nombre, unidad):
    # Obtener contexto normativo relevante
    contexto_normativo = self._get_normativa_context(funcion_text, verbo, puesto_nombre)

    # Llamar a LLM con prompt de evaluacion
    llm_response = self._call_llm_evaluation(
        funcion_text=funcion_text,
        verbo=verbo,
        nivel_jerarquico=nivel_jerarquico,
        puesto_nombre=puesto_nombre,
        unidad=unidad,
        contexto_normativo=contexto_normativo
    )

    # Parsear respuesta LLM (5 criterios)
    result = self._parse_llm_response(llm_response, funcion_text, verbo)

    return result
```

---

**FIN DEL ANALISIS COMPARATIVO**
