# Próximos Pasos: Validación v4 vs v5

## 📋 Resumen de Herramientas Creadas

Ya tienes todo listo para validar v5 contra v4:

1. ✅ **Script de validación**: `scripts/validate_v4_vs_v5.py`
2. ✅ **Documento de estrategia**: `VALIDATION_STRATEGY.md`
3. ✅ **Sistema v5 completo y funcional**
4. ✅ **Datos de v4 disponibles** en `/home/alfred/HerramientaHomologaci-nDocker`

---

## 🎯 Paso 1: Preparar Casos de Test

### Opción A: Usar Puestos SABG Existentes

Los puestos SABG ya están en v4:

```bash
cd /home/alfred/HerramientaHomologaci-nDocker/data

# Puestos disponibles
ls "Secretaria Buen Gobierno/"
```

**Puestos sugeridos para test**:
1. `SECRETARIA(O) ANTICORRUPCION Y BUEN GOBIERNO.txt`
2. `DIRECTOR(A) GENERAL DE PREVENCION DE LA CORRUPCION Y MEJORA CO 3.txt`
3. `DIRECTOR(A) GENERAL DE COOPERACION TECNICA.txt`

### Opción B: Crear Nuevos Casos desde Cero

Si quieres empezar de cero con casos controlados:

1. Selecciona 3-5 archivos de puestos
2. Ejecuta extracción con v4 y guarda resultados
3. Ejecuta extracción con v5
4. Compara manualmente

---

## 🚀 Paso 2: Configurar el Script

### 2.1 Editar `scripts/validate_v4_vs_v5.py`

```python
# Línea ~380 aprox, buscar "test_cases"
test_cases = [
    {
        "name": "SABG - Secretario",
        "v4_result": "../HerramientaHomologaci-nDocker/data/resultados_v4/secretario_sabg_result.json",
        "puesto_file": "../HerramientaHomologaci-nDocker/data/Secretaria Buen Gobierno/SECRETARIA(O) ANTICORRUPCION Y BUEN GOBIERNO.txt"
    },
    {
        "name": "SABG - Director General",
        "v4_result": "../HerramientaHomologaci-nDocker/data/resultados_v4/director_sabg_result.json",
        "puesto_file": "../HerramientaHomologaci-nDocker/data/Secretaria Buen Gobierno/DIRECTOR(A) GENERAL DE COOPERACION TECNICA.txt"
    },
    # Agregar más casos...
]
```

### 2.2 Generar Resultados v4 (si no existen)

Si no tienes resultados v4 guardados, necesitas generarlos:

```bash
cd /home/alfred/HerramientaHomologaci-nDocker

# Ejecutar extracción con v4 para obtener resultados base
python notebooks/main_notebook.ipynb  # o el script que uses en v4
```

O **alternativamente**, puedes:

**Opción Simple**: Ejecutar solo v5 y validar manualmente los resultados mirando el archivo original.

---

## 🔧 Paso 3: Ejecutar Validación

### 3.1 Configurar Entorno

```bash
cd /home/alfred/herramienta-homologacion-v5

# Asegurar que API key está configurada
export OPENAI_API_KEY='tu-api-key-aqui'

# Verificar que está configurada
echo $OPENAI_API_KEY
```

### 3.2 Ejecutar Script

```bash
# Ejecutar validación
python scripts/validate_v4_vs_v5.py
```

**Salida esperada**:
```
================================================================================
🧪 Validación v4 vs v5 - Comparación de Resultados
================================================================================

Casos de test configurados: 3

[1/3] Procesando: SABG - Secretario
  ✅ Resultado v4 cargado
  🔄 Extrayendo con v5...
  ✅ Comparación completada: 92.5% similitud

[2/3] Procesando: SABG - Director General
  ✅ Resultado v4 cargado
  🔄 Extrayendo con v5...
  ✅ Comparación completada: 88.0% similitud

...

📊 REPORTE DE VALIDACIÓN v4 vs v5
================================================================================
Total de casos: 3
v5 exitosos: 3/3 (100.0%)
Similitud promedio: 90.2%

✅ EXCELENTE: v5 mantiene alta fidelidad con v4 (≥90%)
```

---

## 📊 Paso 4: Analizar Resultados

### 4.1 Revisar Reporte en Consola

El script muestra:
- ✅ Estado de cada caso
- ✅ Porcentaje de similitud
- ✅ Diferencias encontradas
- ✅ Notas sobre mejoras o regresiones

### 4.2 Revisar JSON Detallado

```bash
# Ver reporte JSON completo
cat validation_v4_vs_v5_report.json

# O con formato bonito
python -m json.tool validation_v4_vs_v5_report.json
```

### 4.3 Interpretar Resultados

**Si similitud ≥90%**: ✅ Excelente, v5 funciona correctamente

**Si similitud 75-90%**: ⚠️ Revisar diferencias específicas
- ¿Son mejoras de v5?
- ¿Son variaciones semánticas aceptables?

**Si similitud <75%**: ❌ Requiere investigación
- Revisar prompts
- Verificar lógica de validación
- Ajustar según sea necesario

---

## 🔍 Paso 5: Validación Manual (Alternativa Simple)

Si no tienes resultados v4 guardados, puedes hacer **validación manual**:

### 5.1 Ejecutar Extracción Simple

```bash
cd /home/alfred/herramienta-homologacion-v5

# Ejecutar con un puesto de prueba
python scripts/run_extraction.py \
  ../HerramientaHomologaci-nDocker/data/"Secretaria Buen Gobierno/SECRETARIA(O) ANTICORRUPCION Y BUEN GOBIERNO.txt" \
  intelligent
```

### 5.2 Verificar Manualmente

Abre el archivo original y verifica:

- ✅ **Denominación**: ¿Se extrajo correctamente?
- ✅ **Nivel salarial**: ¿Coincide?
- ✅ **Funciones**: ¿Se extrajeron todas?
- ✅ **Verbos**: ¿Los verbos de acción son correctos?

### 5.3 Guardar Resultado

```bash
# El script pregunta si quieres guardar
# Responder: s

# Resultado guardado como: SECRETARIA_O_ANTICORRUPCION_Y_BUEN_GOBIERNO_extracted.json
```

---

## 📈 Criterios de Éxito

### ✅ Validación Exitosa si:

1. **Extracción funciona**: v5 puede procesar todos los archivos
2. **Campos críticos**: denominación, nivel, funciones se extraen
3. **Cantidad razonable**: número de funciones similar a v4 (±2)
4. **Verbos identificados**: verbos de acción correctos
5. **Sin errores fatales**: no crashes ni timeouts

### ⚠️ Requiere Ajuste si:

1. **Funciones faltantes**: v5 extrae significativamente menos
2. **Campos null**: campos críticos quedan vacíos
3. **Errores frecuentes**: múltiples archivos fallan
4. **Parsing incorrecto**: JSON malformado

---

## 🎯 Recomendación para Empezar

### Plan Mínimo (30 minutos):

1. **Elegir 2-3 archivos** de `Secretaria Buen Gobierno/`
2. **Ejecutar v5** con `scripts/run_extraction.py`
3. **Revisar manualmente** comparando con archivo original
4. **Verificar** que información crítica se extrae correctamente

### Plan Completo (2-3 horas):

1. **Generar resultados v4** para 5-10 casos
2. **Configurar script** `validate_v4_vs_v5.py`
3. **Ejecutar validación** automatizada
4. **Analizar reporte** y ajustar si necesario
5. **Documentar resultados** para referencia

---

## 💡 Tips

### Para Debugging:

```python
# Si quieres ver más detalles durante extracción
# Editar scripts/run_extraction.py línea 63:
extractor = PipelineFactory.create_simple_pipeline(
    model="openai/gpt-4o",
    enable_logging=True  # <-- Cambiar a True para más info
)
```

### Para Diferentes Modos:

```bash
# Probar con modo fast (más rápido)
python scripts/run_extraction.py archivo.txt fast

# Probar con modo thorough (más detallado)
python scripts/run_extraction.py archivo.txt thorough
```

### Para Ver Estructura JSON:

```bash
# Ver estructura de un resultado guardado
python -c "import json; print(json.dumps(json.load(open('resultado.json')), indent=2))" | head -50
```

---

## 📞 Siguientes Pasos

1. **Ahora mismo**: Ejecuta una prueba simple con `run_extraction.py`
2. **Hoy**: Valida 2-3 casos manualmente
3. **Esta semana**: Configura y ejecuta validación automatizada
4. **Siguiente**: Documenta resultados y define próximos pasos

---

## 🚀 Comando Rápido para Empezar

```bash
cd /home/alfred/herramienta-homologacion-v5

export OPENAI_API_KEY='tu-api-key'

# Ejecutar primera prueba
python scripts/run_extraction.py \
  ../HerramientaHomologaci-nDocker/data/"Secretaria Buen Gobierno/SECRETARIA(O) ANTICORRUPCION Y BUEN GOBIERNO.txt" \
  intelligent

# Ver resultado
ls -lh *.json
```

---

¡Éxito con las pruebas! 🎉
