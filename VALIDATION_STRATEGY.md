# Estrategia de Validación v4 vs v5

**Objetivo**: Asegurar que la migración a v5.0 mantiene (o mejora) la funcionalidad y calibración de v4.

---

## 🎯 Métodos de Validación

### **Método 1: Comparación de Extracción Directa**

**Descripción**: Ejecutar ambas versiones con los mismos archivos y comparar resultados campo por campo.

**Pasos**:
1. Seleccionar casos de test representativos
2. Ejecutar extracción en v4 (usar resultados guardados si existen)
3. Ejecutar extracción en v5
4. Comparar resultados automáticamente

**Script**: `scripts/validate_v4_vs_v5.py`

**Métricas**:
- ✅ Porcentaje de similitud global
- ✅ Campos críticos coincidentes (denominación, nivel, funciones)
- ✅ Número de funciones extraídas
- ✅ Verbos de acción identificados
- ✅ Tasa de éxito de extracción

**Criterios de Éxito**:
- ≥90%: Excelente fidelidad
- ≥75%: Compatible
- ≥60%: Aceptable con diferencias
- <60%: Requiere revisión

---

### **Método 2: Validación con Golden Dataset**

**Descripción**: Usar resultados históricos de v4 como "golden standard" para regresión testing.

**Pasos**:
1. Identificar 10-15 casos ya validados en v4
2. Usar sus resultados guardados como referencia
3. Ejecutar v5 con mismos inputs
4. Calcular métricas de regresión

**Casos Sugeridos**:
- ✅ 5 puestos SABG validados (positivos)
- ❌ 3 puestos CONAPESCA vs SABG (negativos esperados)
- ✅ 2 puestos formato convencional
- ✅ 2 puestos formato no convencional
- ✅ 1 puesto con caracteres especiales

**Métricas de Regresión**:
```
Completitud = campos_extraidos_v5 / campos_extraidos_v4
Precisión = campos_correctos_v5 / total_campos_v5
Recall = campos_correctos_v5 / campos_en_v4
F1-Score = 2 * (Precisión * Recall) / (Precisión + Recall)
```

---

### **Método 3: Validación de Calibración**

**Descripción**: Verificar que los criterios de validación (verbos débiles, umbrales) funcionan igual.

**Aspectos a Validar**:

1. **Detección de Verbos Débiles**:
   - Verificar que v5 detecta mismos verbos que v4
   - Validar clasificación CRITICAL vs MODERATE

2. **Umbrales de Tolerancia**:
   - Verificar umbral 50% para verbos débiles
   - Confirmar lógica de FAIL vs PASS

3. **Validación Contextual** (si se migra):
   - Referencias institucionales
   - Herencia jerárquica
   - Alineación con normativa

**Casos de Test Específicos**:
- Puesto con 1/19 verbos débiles (debe PASAR)
- Puesto con 6/10 verbos débiles (debe FALLAR)
- Puesto SABG vs normativa SABG (debe PASAR)
- Puesto CONAPESCA vs normativa SABG (debe FALLAR)

---

## 📋 Casos de Test Recomendados

### **Set Mínimo (5 casos)**:
1. ✅ Puesto 1 SABG (positivo conocido)
2. ✅ Puesto formato PDF estándar
3. ❌ Puesto CONAPESCA vs SABG (negativo)
4. ✅ Puesto con formato no convencional
5. ✅ Puesto con nivel salarial complejo (G11, M33, etc.)

### **Set Completo (15 casos)**:
- Todo lo del set mínimo
- 3 puestos SABG adicionales validados
- 2 puestos con verbos débiles (diferentes tasas)
- 2 puestos diferentes organismos
- 3 puestos con formatos diversos

---

## 🔧 Herramientas Creadas

### 1. `validate_v4_vs_v5.py`

**Funcionalidad**:
- Carga resultados de v4 (JSON guardados)
- Ejecuta extracción con v5
- Compara campo por campo
- Genera reporte detallado
- Calcula métricas de similitud

**Uso**:
```bash
# Editar script para agregar tus casos
nano scripts/validate_v4_vs_v5.py

# Configurar casos de test en el array test_cases
# Ejecutar
python scripts/validate_v4_vs_v5.py
```

**Output**:
- Reporte en consola con estadísticas
- JSON detallado: `validation_v4_vs_v5_report.json`

---

## 📊 Formato de Reporte

```
📊 REPORTE DE VALIDACIÓN v4 vs v5
================================================================================

Total de casos: 5
v5 exitosos: 5/5 (100.0%)
Similitud promedio: 92.3%

================================================================================
Resultados por Caso
================================================================================

1. Puesto SABG 1
   Estado v5: ✅ Success
   Similitud: 95.0%
   Funciones: v4=19, v5=19
   Campos diferentes: 1/5
   Diferencias:
     - funciones[3].verbo_accion: v4='coordinar' vs v5='conducir'
   Notas:
     ✅ v5 extrajo exitosamente

...

================================================================================
Conclusiones
================================================================================
✅ EXCELENTE: v5 mantiene alta fidelidad con v4 (≥90%)
```

---

## 🚀 Cómo Ejecutar Validación

### **Paso 1: Preparar Casos de Test**

```bash
# Navegar a v4
cd /home/alfred/HerramientaHomologaci-nDocker

# Identificar resultados guardados
ls data/resultados_validacion_sabg/

# Anotar rutas de:
# - Resultados v4 (JSON)
# - Archivos de puestos originales
```

### **Paso 2: Configurar Script**

```python
# Editar scripts/validate_v4_vs_v5.py
test_cases = [
    {
        "name": "Puesto SABG 1",
        "v4_result": "ruta/a/resultado_v4.json",
        "puesto_file": "ruta/a/puesto.txt"
    },
    # ... más casos
]
```

### **Paso 3: Ejecutar Validación**

```bash
cd /home/alfred/herramienta-homologacion-v5

# Configurar API key
export OPENAI_API_KEY='tu-api-key'

# Ejecutar validación
python scripts/validate_v4_vs_v5.py
```

### **Paso 4: Analizar Resultados**

```bash
# Ver reporte detallado
cat validation_v4_vs_v5_report.json

# Analizar diferencias
# Si similitud <90%, investigar causas
```

---

## ⚠️ Posibles Causas de Diferencias

### **Diferencias Esperadas (Normales)**:
1. **Mejoras en extracción**: v5 puede extraer más información
2. **Verbos sinónimos**: "coordinar" vs "conducir" (semánticamente equivalentes)
3. **Formato de salida**: Campos adicionales o metadata
4. **Limpieza de texto**: v5 puede limpiar mejor caracteres especiales

### **Diferencias Problemáticas (Requieren Atención)**:
1. **Funciones faltantes**: v5 extrae significativamente menos
2. **Campos críticos null**: denominación, nivel salarial vacíos
3. **Errores de parsing**: JSON malformado o incompleto
4. **Cambio en calibración**: Puestos que deberían pasar/fallar cambian

---

## 📈 Métricas de Éxito del Proyecto

**Objetivo Global**: Mantener o superar funcionalidad de v4

**KPIs**:
- ✅ Similitud promedio ≥ 85%
- ✅ Tasa de éxito extracción ≥ 95%
- ✅ Campos críticos coincidentes ≥ 90%
- ✅ Sin regresiones en casos positivos conocidos
- ✅ Validación negativa mantiene criterios

**Si se cumplen estos KPIs**: ✅ Migración exitosa, v5 listo para producción

---

## 🔄 Iteración y Mejora

Si se encuentran divergencias:

1. **Analizar causa raíz**:
   - ¿Es mejora o regresión?
   - ¿Afecta funcionalidad crítica?

2. **Ajustar si necesario**:
   - Refinar prompts
   - Ajustar umbrales
   - Mejorar validación

3. **Re-validar**:
   - Ejecutar nuevamente casos afectados
   - Confirmar corrección

4. **Documentar**:
   - Registrar cambios
   - Actualizar expectativas

---

## 📝 Próximos Pasos

1. **Inmediato**:
   - [ ] Identificar 5 casos de test mínimos
   - [ ] Localizar resultados v4 guardados
   - [ ] Configurar `validate_v4_vs_v5.py`
   - [ ] Ejecutar primera validación

2. **Corto Plazo**:
   - [ ] Ampliar a 15 casos completos
   - [ ] Validar calibración específica
   - [ ] Documentar cualquier diferencia
   - [ ] Ajustar si es necesario

3. **Mediano Plazo**:
   - [ ] Crear suite automatizada de tests
   - [ ] Integrar en CI/CD
   - [ ] Establecer como regresión testing

---

**Documento creado**: 2025-11-01
**Versión**: 1.0
