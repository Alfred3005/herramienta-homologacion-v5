# PLAN DE RESTAURACION DE FUNCIONALIDAD V5
## Acciones Concretas para Restaurar lo que se Rompio

**Fecha:** 2025-11-07
**Referencia:** ANALISIS_COMPARATIVO_V4_VS_V5.md

---

## RESUMEN DE PROBLEMAS CRITICOS

| # | Problema | Impacto | Prioridad | Tiempo Est. |
|---|----------|---------|-----------|-------------|
| 1 | Embeddings deshabilitados en IntegratedValidator | CRITICO - Precision cae 3.8x | P0 | 5 min |
| 2 | Contexto fragmentado (5 chunks vs 15) | ALTO - Pierde vision holistica | P1 | 10 min |
| 3 | N+1 llamadas LLM innecesarias | MEDIO - 10x mas lento | P2 | 30 min |
| 4 | Threshold Jaccard muy bajo (0.1) | MEDIO - Falsos positivos | P1 | 2 min |

---

## ACCION 1: HABILITAR EMBEDDINGS (P0 - CRITICO)

### Problema
```python
# integrated_validator.py (linea 73)
self.normativa_loader = create_loader_from_fragments(
    use_embeddings=False,  # ← DESHABILITADO "para rapidez"
)
```

### Solucion
```python
# integrated_validator.py (linea 73)
self.normativa_loader = create_loader_from_fragments(
    text_fragments=normativa_fragments,
    document_title="Reglamento Interior",
    use_embeddings=True,  # ← HABILITAR
    context=self.context
)
```

### Archivo a Modificar
- `/home/alfred/herramienta-homologacion-v5/src/validators/integrated_validator.py`
- Linea: 73

### Impacto Esperado
- Precision de busqueda: 0.23 → 0.87 (+278%)
- Threshold: 0.1 → 0.58 (menos falsos positivos)
- Costo: +100ms inicializacion, <10ms por query
- Contexto normativo LLM: BAJA calidad → ALTA calidad

### Validacion
```bash
# Test antes del cambio
cd /home/alfred/herramienta-homologacion-v5
python -c "
from src.validators.integrated_validator import IntegratedValidator
validator = IntegratedValidator(normativa_fragments=['test'])
print(f'Embedding mode: {validator.normativa_loader.embedding_mode}')
# Esperado ANTES: 'disabled'
"

# Test despues del cambio
python -c "
from src.validators.integrated_validator import IntegratedValidator
validator = IntegratedValidator(normativa_fragments=['test'])
print(f'Embedding mode: {validator.normativa_loader.embedding_mode}')
# Esperado DESPUES: 'enabled' o 'hybrid'
"
```

---

## ACCION 2: AUMENTAR CHUNKS RECUPERADOS (P1 - ALTO)

### Problema
```python
# function_semantic_evaluator.py (linea 218-221)
search_results = self.normativa_loader.semantic_search(
    query=query,
    max_results=5  # ← SOLO 5 chunks por funcion
)
```

### Solucion
```python
# function_semantic_evaluator.py (linea 218-221)
search_results = self.normativa_loader.semantic_search(
    query=query,
    max_results=15  # ← Aumentar a 15 (como v4)
)
```

### Archivo a Modificar
- `/home/alfred/herramienta-homologacion-v5/src/validators/function_semantic_evaluator.py`
- Linea: 220

### Impacto Esperado
- Cobertura normativa: +200% (5 → 15 fragmentos)
- Mayor probabilidad de encontrar fragmento relevante
- Mejor contexto para LLM en evaluacion de 5 criterios
- Costo: +50ms por busqueda (despreciable)

### Validacion
```python
# Test
from src.validators.function_semantic_evaluator import FunctionSemanticEvaluator

evaluator = FunctionSemanticEvaluator(normativa_loader, context)
result = evaluator._get_normativa_context(
    funcion_text="Coordinar actividades de transparencia",
    verbo="coordinar",
    puesto_nombre="Director"
)

# Contar fragmentos en resultado
num_fragments = result.count("[Fragmento")
print(f"Fragmentos recuperados: {num_fragments}")
# Esperado DESPUES: 15 (vs 5 antes)
```

---

## ACCION 3: AUMENTAR THRESHOLD JACCARD (P1 - ALTO)

### Problema
```python
# normativa_loader.py (linea 335)
if confidence > 0.1:  # ← Threshold muy bajo
    results.append(match)
```

### Solucion
```python
# normativa_loader.py (linea 335)
if confidence > 0.15:  # ← Aumentar threshold
    results.append(match)
```

### Archivo a Modificar
- `/home/alfred/herramienta-homologacion-v5/src/validators/normativa_loader.py`
- Linea: 335

### Justificacion
- Threshold 0.1 (10%) es muy permisivo
- Genera muchos falsos positivos
- v4 usa 0.58 con embeddings (mucho mas estricto)
- 0.15 (15%) es un compromiso razonable para Jaccard

### Impacto Esperado
- Reduccion de falsos positivos: ~30%
- Mejores resultados en top-5/top-15
- Sin perdida significativa de recall

### Validacion
```python
# Test comparativo
from src.validators.normativa_loader import NormativaLoader

loader = NormativaLoader()
loader.initialize(use_embeddings=False)  # Forzar Jaccard

results = loader.semantic_search("coordinar transparencia", max_results=15)

# Analizar confianza minima
min_confidence = min(r.confidence_score for r in results)
print(f"Confianza minima: {min_confidence}")
# Esperado DESPUES: >= 0.15 (vs >= 0.1 antes)
```

---

## ACCION 4: OPTIMIZAR FLUJO DE VALIDACION (P2 - MEDIO)

### Problema
```python
# integrated_validator.py - _validate_criterion_1
# Hace N llamadas LLM (una por funcion)
for idx, func in enumerate(funciones):
    evaluation = self.function_evaluator.evaluate_function(...)
    # ← N llamadas LLM
```

### Solucion A: Validacion Global Primaria (RECOMENDADO)

```python
# integrated_validator.py - NUEVO metodo
def _validate_criterion_1_global(self, codigo, puesto_data):
    """
    Criterio 1 GLOBAL: Validacion holistica del puesto completo.
    Similar a ContextualVerbValidator pero enfocado en verbos.
    """
    # 1 sola llamada LLM para todo el puesto
    search_query = f"{puesto_nombre} {objetivo_general} {funciones_summary}"
    normativa_context = self.normativa_loader.semantic_search(
        query=search_query,
        max_results=15  # Contexto amplio
    )

    llm_result = self._validate_verbs_with_llm_global(
        puesto_nombre, funciones, nivel_jerarquico, normativa_context
    )

    return Criterion1Result(...)
```

### Solucion B: Batch LLM (ALTERNATIVA)

```python
# function_semantic_evaluator.py - NUEVO metodo
def evaluate_functions_batch(self, funciones_list):
    """
    Evalua multiples funciones en 1 llamada LLM.
    Usa prompt con array de funciones.
    """
    # Construir contexto con TODAS las funciones
    all_functions_text = "\n".join([
        f"{i}. {f['verbo_accion']} - {f['descripcion_completa'][:100]}"
        for i, f in enumerate(funciones_list, 1)
    ])

    # 1 llamada LLM para N funciones
    llm_response = self._call_llm_batch_evaluation(all_functions_text)

    return [parse_result(r) for r in llm_response["evaluations"]]
```

### Impacto Esperado
- Latencia: 10-30s → 2-5s (6x mas rapido)
- Costo LLM: N+1 llamadas → 2 llamadas (-83% para N=20)
- Vision holistica restaurada
- Mejor deteccion de coherencia entre funciones

### Archivo a Modificar
- Solucion A: `/home/alfred/herramienta-homologacion-v5/src/validators/integrated_validator.py`
- Solucion B: `/home/alfred/herramienta-homologacion-v5/src/validators/function_semantic_evaluator.py`

---

## ACCION 5: AGREGAR MODO HIBRIDO CONFIGURABLE (P2 - MEDIO)

### Problema
- v5 no permite configurar modo de busqueda
- v4 tiene 3 modos: "enabled", "hybrid", "disabled"

### Solucion
```python
# integrated_validator.py - __init__
def __init__(
    self,
    normativa_fragments: Optional[List[str]] = None,
    openai_api_key: Optional[str] = None,
    embedding_mode: str = "hybrid"  # ← NUEVO parametro
):
    # ...
    if normativa_fragments:
        self.normativa_loader = create_loader_from_fragments(
            text_fragments=normativa_fragments,
            document_title="Reglamento Interior",
            use_embeddings=(embedding_mode != "disabled"),
            context=self.context
        )

        # Configurar modo
        if hasattr(self.normativa_loader, 'embedding_mode'):
            self.normativa_loader.embedding_mode = embedding_mode
```

### Modos Disponibles
- `"enabled"`: Solo embeddings (maximo precision, mas lento)
- `"hybrid"`: Jaccard + embeddings (balance, RECOMENDADO)
- `"disabled"`: Solo Jaccard (rapido, baja precision)

### Impacto Esperado
- Flexibilidad para casos de uso
- Modo hybrid: Precision ~0.85, velocidad intermedia
- Facil testing de modos

---

## PLAN DE IMPLEMENTACION SECUENCIAL

### Fase 1: Fixes Rapidos (15 minutos)

```bash
# 1. Habilitar embeddings
sed -i 's/use_embeddings=False/use_embeddings=True/' \
  /home/alfred/herramienta-homologacion-v5/src/validators/integrated_validator.py

# 2. Aumentar chunks de 5 a 15
sed -i 's/max_results=5/max_results=15/' \
  /home/alfred/herramienta-homologacion-v5/src/validators/function_semantic_evaluator.py

# 3. Aumentar threshold Jaccard
sed -i 's/confidence > 0.1/confidence > 0.15/' \
  /home/alfred/herramienta-homologacion-v5/src/validators/normativa_loader.py

# 4. Validar
cd /home/alfred/herramienta-homologacion-v5
python -m pytest tests/test_integrated_validator.py -v
```

### Fase 2: Optimizacion de Flujo (1 hora)

1. Implementar `_validate_criterion_1_global()` en `integrated_validator.py`
2. Agregar parametro `embedding_mode` configurable
3. Tests unitarios para nuevos metodos
4. Benchmarking de latencia y precision

### Fase 3: Validacion End-to-End (30 minutos)

1. Test con dataset real de puestos SABG
2. Comparacion v5 mejorado vs v4
3. Metricas: precision, recall, latencia
4. Documentacion de resultados

---

## METRICAS DE EXITO

### Antes (v5 actual)

| Metrica | Valor Actual |
|---------|--------------|
| Precision busqueda | ~0.23 (Jaccard) |
| Latencia por puesto | 10-30s (20 funciones) |
| Llamadas LLM | N+1 (21 para 20 funciones) |
| Threshold | 0.1 (muy bajo) |
| Contexto por funcion | 5 chunks |

### Despues (v5 mejorado)

| Metrica | Valor Esperado |
|---------|----------------|
| Precision busqueda | ~0.87 (embeddings) |
| Latencia por puesto | 2-5s |
| Llamadas LLM | 2 (global) |
| Threshold | 0.58 (embeddings) o 0.15 (Jaccard) |
| Contexto global | 15 chunks |

### Ganancia

| Metrica | Mejora |
|---------|--------|
| Precision | +278% |
| Latencia | -70% |
| Costo LLM | -90% |
| Calidad contexto | +200% |

---

## RIESGOS Y MITIGACIONES

### Riesgo 1: Embeddings no disponibles

**Problema:** EmbeddingEngine falla al inicializar

**Mitigacion:**
```python
# Fallback automatico a Jaccard con threshold mejorado
try:
    self.normativa_loader = create_loader_from_fragments(
        use_embeddings=True
    )
except Exception as e:
    logger.warning(f"Embeddings fallaron: {e}, usando Jaccard")
    self.normativa_loader = create_loader_from_fragments(
        use_embeddings=False
    )
    # Aumentar threshold Jaccard compensatoriamente
    self.normativa_loader.jaccard_threshold = 0.20
```

### Riesgo 2: Cambio de API LLM

**Problema:** Prompt global no parsea correctamente

**Mitigacion:**
- Mantener modo por funcion como fallback
- Tests end-to-end con validacion de respuesta JSON
- Schema validation con Pydantic

### Riesgo 3: Regression en precision

**Problema:** Cambios degradan precision

**Mitigacion:**
- Dataset de gold standard (puestos validados manualmente)
- Tests A/B (v5 actual vs v5 mejorado)
- Metricas automatizadas en CI/CD

---

## CHECKLIST DE IMPLEMENTACION

### Pre-requisitos
- [ ] Backup de `/home/alfred/herramienta-homologacion-v5/src/validators/`
- [ ] Tests unitarios existentes pasan
- [ ] Dataset de prueba preparado

### Fase 1: Fixes Rapidos
- [ ] Habilitar embeddings en integrated_validator.py (linea 73)
- [ ] Aumentar max_results en function_semantic_evaluator.py (linea 220)
- [ ] Aumentar threshold en normativa_loader.py (linea 335)
- [ ] Tests unitarios pasan
- [ ] Benchmarking basico (10 puestos)

### Fase 2: Optimizacion
- [ ] Implementar _validate_criterion_1_global()
- [ ] Agregar parametro embedding_mode configurable
- [ ] Tests unitarios para nuevos metodos
- [ ] Benchmarking completo (100 puestos)

### Fase 3: Validacion
- [ ] Tests end-to-end con dataset real
- [ ] Comparacion metricas v5 vs v5 mejorado
- [ ] Documentacion actualizada
- [ ] Code review y merge

---

## COMANDOS DE VALIDACION

### Test 1: Embeddings Habilitados
```python
from src.validators.integrated_validator import IntegratedValidator

validator = IntegratedValidator(normativa_fragments=["test fragment"])
assert validator.normativa_loader.embedding_mode != "disabled", "Embeddings deben estar habilitados"
print("✓ Test 1: Embeddings habilitados")
```

### Test 2: Busqueda con Mayor Precision
```python
from src.validators.normativa_loader import NormativaLoader

loader = NormativaLoader()
loader.initialize(use_embeddings=True)

results = loader.semantic_search("coordinar transparencia", max_results=15)
avg_confidence = sum(r.confidence_score for r in results) / len(results)

assert avg_confidence > 0.50, f"Confianza promedio baja: {avg_confidence}"
print(f"✓ Test 2: Confianza promedio = {avg_confidence:.2f}")
```

### Test 3: Latencia Mejorada
```python
import time
from src.validators.integrated_validator import IntegratedValidator

validator = IntegratedValidator(normativa_fragments=["test"])
puesto_data = {
    "codigo": "TEST",
    "denominacion": "Director de Transparencia",
    "nivel_salarial": "M1",
    "funciones": [{"descripcion_completa": f"Funcion {i}"} for i in range(20)]
}

start = time.time()
result = validator.validate_puesto(puesto_data)
latencia = time.time() - start

assert latencia < 10, f"Latencia muy alta: {latencia}s"
print(f"✓ Test 3: Latencia = {latencia:.2f}s")
```

---

## SIGUIENTE PASO INMEDIATO

**EJECUTAR AHORA:**

```bash
cd /home/alfred/herramienta-homologacion-v5

# 1. Backup
cp -r src/validators src/validators.backup

# 2. Fix critico: Habilitar embeddings
sed -i '73s/use_embeddings=False/use_embeddings=True/' \
  src/validators/integrated_validator.py

# 3. Validar cambio
grep -n "use_embeddings" src/validators/integrated_validator.py | head -5

# 4. Test rapido
python -c "
from src.validators.integrated_validator import IntegratedValidator
v = IntegratedValidator(normativa_fragments=['test'])
print(f'Embedding mode: {v.normativa_loader.embedding_mode if v.normativa_loader else \"No loader\"}')
"

# 5. Commit
git add src/validators/integrated_validator.py
git commit -m "FIX: Habilitar embeddings en IntegratedValidator para restaurar precision de busqueda normativa"
```

**Tiempo estimado:** 2 minutos
**Impacto esperado:** +278% precision en busqueda normativa

---

**FIN DEL PLAN DE RESTAURACION**
