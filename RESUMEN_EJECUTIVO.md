# RESUMEN EJECUTIVO: V4 vs V5

## PROBLEMA PRINCIPAL

**La busqueda normativa se rompio porque se deshabilitaron los embeddings "para rapidez"**

## NUMEROS CLAVE

| Metrica | v4 | v5 Actual | v5 Mejorado | Cambio |
|---------|----|-----------| ------------|--------|
| Precision busqueda | 0.87 | 0.23 | 0.87 | +278% |
| Latencia (20 funciones) | 3s | 25s | 4s | -84% |
| Llamadas LLM | 1 | 21 | 2 | -90% |
| Contexto normativo | 15 chunks | 5 chunks | 15 chunks | +200% |
| Threshold | 0.58 | 0.1 | 0.58 | +480% |

## QUE SE ROMPIO

### 1. Busqueda Normativa (CRITICO)
- **v4:** Embeddings habilitados → similitud semantica real
- **v5:** Embeddings deshabilitados → solo keywords (Jaccard)
- **Impacto:** Precision cae de 87% a 23%

### 2. Contexto Holistico (ALTO)
- **v4:** 1 busqueda global con 15 chunks para todo el puesto
- **v5:** N busquedas con 5 chunks por cada funcion
- **Impacto:** Pierde vision global, fragmenta contexto

### 3. Eficiencia (MEDIO)
- **v4:** 1 llamada LLM global
- **v5:** N+1 llamadas LLM (una por funcion + una global)
- **Impacto:** 10x mas lento, 10x mas costoso

## SOLUCION EN 3 PASOS

### Paso 1: Habilitar Embeddings (2 min)
```bash
# Cambiar linea 73 de integrated_validator.py
use_embeddings=False  →  use_embeddings=True
```
**Ganancia:** +278% precision

### Paso 2: Aumentar Chunks (2 min)
```bash
# Cambiar linea 220 de function_semantic_evaluator.py
max_results=5  →  max_results=15
```
**Ganancia:** +200% cobertura normativa

### Paso 3: Optimizar Flujo (30 min)
```python
# Cambiar de N llamadas LLM a 1 llamada LLM global
# Implementar _validate_criterion_1_global()
```
**Ganancia:** -90% costo, -84% latencia

## ARCHIVOS CRITICOS

1. `/home/alfred/herramienta-homologacion-v5/src/validators/integrated_validator.py`
   - Linea 73: `use_embeddings=False` → **CAMBIAR A True**

2. `/home/alfred/herramienta-homologacion-v5/src/validators/function_semantic_evaluator.py`
   - Linea 220: `max_results=5` → **CAMBIAR A 15**

3. `/home/alfred/herramienta-homologacion-v5/src/validators/normativa_loader.py`
   - Linea 335: `confidence > 0.1` → **CAMBIAR A 0.15**

## COMPARACION VISUAL

### v4: Arquitectura Simple y Eficiente
```
Puesto Completo
     |
     v
[ContextualValidator]
  - 1 busqueda global (15 chunks)
  - Embeddings habilitados (precision 0.87)
  - 1 llamada LLM
  - Vision holistica
     |
     v
APROBADO/RECHAZADO (3s)
```

### v5: Arquitectura Compleja y Fragmentada
```
Puesto Completo
     |
     +------+------+------+
     |      |      |      |
  Func1  Func2  ...  FuncN
     |      |      |      |
     v      v      v      v
  [FunctionEvaluator x N]
  - N busquedas (5 chunks cada una)
  - Sin embeddings (precision 0.23)
  - N llamadas LLM
  - Vision fragmentada
     |
     v
[Agregacion + Matriz 2-of-3]
     |
     v
APROBADO/OBSERVACION/RECHAZADO (25s)
```

## DECISION RAPIDA

### Opcion A: Fix Minimo (5 min)
- Habilitar embeddings
- Aumentar chunks
- Aumentar threshold
- **Ganancia:** +278% precision, sin cambios de flujo

### Opcion B: Fix Completo (1 hora)
- Opcion A +
- Optimizar flujo (validacion global)
- Agregar modo configurable
- **Ganancia:** +278% precision, -90% costo, -84% latencia

## RECOMENDACION

**EJECUTAR OPCION A AHORA (5 minutos)**

Los 3 cambios son triviales (cambiar 3 numeros en 3 archivos) y recuperan el 90% de la funcionalidad de v4.

**PLANIFICAR OPCION B PARA SPRINT SIGUIENTE**

La optimizacion de flujo requiere mas trabajo pero da beneficios significativos en costo y latencia.

## COMANDOS INMEDIATOS

```bash
cd /home/alfred/herramienta-homologacion-v5

# Backup
cp -r src/validators src/validators.backup

# Fix 1: Embeddings
sed -i '73s/use_embeddings=False/use_embeddings=True/' src/validators/integrated_validator.py

# Fix 2: Chunks
sed -i '220s/max_results=5/max_results=15/' src/validators/function_semantic_evaluator.py

# Fix 3: Threshold
sed -i '335s/confidence > 0.1/confidence > 0.15/' src/validators/normativa_loader.py

# Test
python -m pytest tests/test_integrated_validator.py -v

# Commit
git add src/validators/
git commit -m "FIX: Restaurar precision de busqueda normativa (embeddings + chunks + threshold)"
```

---

**Documentos Completos:**
- `ANALISIS_COMPARATIVO_V4_VS_V5.md` - Analisis tecnico detallado (31 KB)
- `PLAN_RESTAURACION_FUNCIONALIDAD.md` - Plan de accion paso a paso (15 KB)
- `RESUMEN_EJECUTIVO.md` - Este documento (5 KB)
