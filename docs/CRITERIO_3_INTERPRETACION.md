# Interpretación del Criterio 3: Impacto Jerárquico

**Versión:** v5.33-new
**Fecha:** 2025-11-10
**Autor:** Claude Code

---

## 📊 ¿Qué es el Criterio 3?

El **Criterio 3: Impacto Jerárquico** evalúa si el impacto declarado en las funciones de un puesto es **coherente** con su nivel jerárquico dentro de la Administración Pública Federal.

### Qué Evalúa

1. **Apropiación de Verbos:** ¿El verbo usado está autorizado para el nivel del puesto?
2. **Alcance de Decisiones:** ¿El alcance de las decisiones es coherente con el nivel?
3. **Consecuencias de Errores:** ¿Las consecuencias de errores son apropiadas para el nivel?
4. **Complejidad:** ¿La complejidad de las tareas es adecuada para el nivel?

### Sistema de Clasificación

El sistema clasifica las discrepancias (incoherencias) en dos niveles:

- **CRITICAL (Crítico):** Discrepancia **SIN** respaldo normativo
  - El impacto no es coherente con el nivel
  - NO hay justificación normativa para esta función
  - **Ejemplo:** Director usando verbo "Apoyar" (nivel operativo) sin respaldo normativo

- **MODERATE (Moderado):** Discrepancia **CON** respaldo normativo
  - El impacto no es coherente con el nivel
  - PERO existe justificación normativa específica
  - **Ejemplo:** Director usando verbo "Apoyar" porque la normativa lo establece explícitamente

---

## 📈 Interpretación de la Tasa Crítica

### Fórmula

```
Tasa Crítica = (Funciones CRITICAL / Total Funciones) × 100%
```

### Decisión del Criterio

- **PASS (Aprobado):** Tasa Crítica ≤ 50%
- **FAIL (Rechazado):** Tasa Crítica > 50%

### ⚠️ IMPORTANTE: ¿Qué significa una Tasa de 0%?

**Tasa Crítica 0% = EXCELENTE RESULTADO** ✅

Una tasa de **0%** significa que:

1. **NO se detectaron funciones con discrepancias críticas**
   - No hay funciones con impacto incoherente sin justificación normativa
   - Todas las funciones tienen impacto apropiado para el nivel

2. **Todas las funciones son coherentes jerárquicamente**
   - Los verbos son apropiados para el nivel
   - El alcance de decisiones es adecuado
   - Las consecuencias de errores son proporcionales
   - La complejidad es coherente con el nivel

3. **El puesto está bien diseñado** en términos de impacto jerárquico
   - No hay "inflación" de funciones (asignar funciones de niveles superiores)
   - No hay "deflación" de funciones (asignar funciones de niveles inferiores)

---

## 📋 Ejemplos de Interpretación

### Ejemplo 1: Tasa Crítica 0% (PASS)

```
Puesto: SECRETARIO DE TURISMO (Nivel G11)
Total Funciones: 15
Funciones CRITICAL: 0
Funciones MODERATE: 0
Tasa Crítica: 0%
Decisión: PASS ✅
```

**Interpretación:**
- **Excelente.** Todas las 15 funciones tienen impacto coherente con el nivel G11.
- No se detectaron discrepancias críticas ni moderadas.
- El puesto está correctamente diseñado en términos de impacto jerárquico.

### Ejemplo 2: Tasa Crítica 20% (PASS)

```
Puesto: DIRECTOR GENERAL DE PLANEACIÓN (Nivel K12)
Total Funciones: 10
Funciones CRITICAL: 2
Funciones MODERATE: 1
Tasa Crítica: 20%
Decisión: PASS ✅
```

**Interpretación:**
- **Aceptable.** 2 de 10 funciones (20%) tienen discrepancias sin respaldo normativo.
- La tasa está por debajo del umbral de 50%, por lo que el criterio aprueba.
- **Recomendación:** Revisar las 2 funciones críticas para alinearlas con el nivel.

### Ejemplo 3: Tasa Crítica 60% (FAIL)

```
Puesto: SUBDIRECTOR DE ÁREA (Nivel M31)
Total Funciones: 8
Funciones CRITICAL: 5
Funciones MODERATE: 0
Tasa Crítica: 62.5%
Decisión: FAIL ❌
```

**Interpretación:**
- **Problemático.** 5 de 8 funciones (62.5%) tienen impacto incoherente sin justificación.
- La tasa supera el umbral de 50%, por lo que el criterio falla.
- **Acción requerida:** Revisar y rediseñar las funciones del puesto.

---

## 🔍 Diferencia con Criterio 1

Es importante NO confundir el Criterio 3 con el Criterio 1:

| Aspecto | Criterio 1: Análisis Semántico | Criterio 3: Impacto Jerárquico |
|---------|-------------------------------|-------------------------------|
| **Qué evalúa** | Calidad de las funciones (estructura, verbo, normativa) | Coherencia del impacto con el nivel |
| **Enfoque** | ¿Están bien escritas las funciones? | ¿Son apropiadas para este nivel? |
| **Métrica principal** | Tasa Crítica de funciones rechazadas | Tasa Crítica de discrepancias sin respaldo |
| **Umbral** | ≤50% funciones rechazadas | ≤50% funciones con discrepancia crítica |
| **Tasa Alta** | Funciones mal escritas | Impacto no coherente con el nivel |
| **Tasa 0%** | Todas las funciones bien escritas | Todas coherentes jerárquicamente |

---

## 📊 Tabla de Referencia Rápida

| Tasa Crítica | Decisión | Interpretación | Acción Recomendada |
|--------------|----------|----------------|-------------------|
| **0%** | PASS ✅ | **Excelente** - Coherencia total | Ninguna |
| **1-25%** | PASS ✅ | **Bueno** - Pocas discrepancias menores | Revisar funciones críticas identificadas |
| **26-50%** | PASS ✅ | **Aceptable** - Varias discrepancias | Revisar y ajustar funciones críticas |
| **51-75%** | FAIL ❌ | **Problemático** - Mayoría con discrepancias | Rediseño significativo requerido |
| **76-100%** | FAIL ❌ | **Crítico** - Diseño incorrecto del puesto | Rediseño completo del puesto |

---

## ❓ Preguntas Frecuentes

### 1. ¿Por qué TODOS mis puestos tienen Tasa 0%?

**Respuesta:** Esto es **normal y positivo** si:
- Los puestos están correctamente diseñados
- Las funciones son apropiadas para sus niveles
- Hay buen respaldo normativo

**No es un bug**, es un indicador de **calidad en el diseño de puestos**.

### 2. ¿Una Tasa de 0% significa que no se evaluó nada?

**Respuesta:** NO. El sistema evaluó:
- Apropiación de verbos (verificado contra tabla de autorización)
- Coherencia de alcance de decisiones
- Coherencia de consecuencias de errores
- Coherencia de complejidad

Una tasa de 0% significa que **todas las evaluaciones pasaron**.

### 3. ¿Es mejor 0% que 10% o 20%?

**Respuesta:** SÍ. Una tasa de 0% indica **coherencia perfecta**. Mientras más baja la tasa, mejor.

### 4. ¿Qué pasa si tengo Tasa 0% pero el Criterio 3 marca FAIL?

**Respuesta:** Esto **NO debería pasar**. Si la Tasa Crítica es 0%, el Criterio 3 SIEMPRE debe ser PASS.
Si esto ocurre, reporta un bug en el sistema.

### 5. ¿Puedo tener Tasa 0% pero aún tener funciones MODERATE?

**Respuesta:** SÍ. La Tasa Crítica solo cuenta funciones **CRITICAL** (sin respaldo).
Puedes tener funciones MODERATE (con respaldo) y aún así tener Tasa 0%.

**Ejemplo:**
```
Total Funciones: 10
CRITICAL: 0
MODERATE: 3
Tasa Crítica: 0% (solo cuenta CRITICAL)
Decisión: PASS ✅
```

---

## 🎯 Conclusión

**La Tasa Crítica de 0% en el Criterio 3 es un RESULTADO POSITIVO que indica:**

✅ Coherencia jerárquica perfecta
✅ Funciones apropiadas para el nivel del puesto
✅ Diseño correcto del puesto
✅ No se requieren ajustes de impacto

**NO es un bug, es un indicador de calidad.**

---

**Documento creado:** 2025-11-10
**Sistema:** Herramienta de Homologación APF v5.33-new
**Para más información:** Consultar `criterion_3_validator.py`
