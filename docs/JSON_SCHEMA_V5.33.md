# Esquema JSON v5.33 - Estructura Robusta de Validación

**Versión:** 5.33-new
**Fecha:** 2025-11-10
**Propósito:** Definir estructura JSON completa y robusta para evitar KeyErrors y soportar validaciones adicionales

---

## 📋 ESTRUCTURA COMPLETA

```json
{
  "puesto": {
    "codigo": "string (REQUERIDO)",
    "denominacion": "string (REQUERIDO)",
    "nivel": "string (REQUERIDO - ej: 'G11', 'H', 'J')",
    "nivel_salarial": "string (ALIAS de 'nivel' para compatibilidad)",
    "unidad_responsable": "string (OPCIONAL, default: '')"
  },
  "validacion": {
    "resultado": "string (REQUERIDO - 'APROBADO_PLENO'|'APROBADO_CON_OBSERVACIONES'|'RECHAZADO')",
    "clasificacion": "string (REQUERIDO - 'EXCELENTE'|'ACEPTABLE'|'DEFICIENTE'|'CRITICO')",
    "criterios_aprobados": "int (REQUERIDO - 0-3)",
    "total_criterios": "int (REQUERIDO - siempre 3)",
    "confianza": "float (REQUERIDO - 0.0-1.0)",
    "criterios": {
      "criterio_1_verbos": {
        "resultado": "string (PASS|FAIL)",
        "tasa_aprobadas": "float",
        "tasa_critica": "float",
        "threshold": "float (default 0.50)",
        "funciones_aprobadas": "int",
        "funciones_observadas": "int",
        "funciones_rechazadas": "int",
        "total_funciones": "int",
        "metodo": "string",
        "detalles": {
          "aprobadas": [...],
          "observadas": [...],
          "rechazadas": [...]
        },
        "validaciones_adicionales": {
          "duplicacion": {
            "tiene_duplicados": "bool",
            "total_duplicados": "int",
            "pares_duplicados": [
              {
                "funcion_1_id": "int",
                "funcion_2_id": "int",
                "similitud": "float",
                "descripcion": "string"
              }
            ]
          },
          "malformacion": {
            "tiene_malformadas": "bool",
            "total_malformadas": "int",
            "funciones_problemáticas": [
              {
                "funcion_id": "int",
                "problemas": [
                  {
                    "tipo": "string (VACIA|PLACEHOLDER|INCOMPLETA|SIN_VERBO|SIN_COMPLEMENTO|SIN_RESULTADO)",
                    "severidad": "string (CRITICAL|HIGH|MODERATE|LOW)",
                    "descripcion": "string"
                  }
                ]
              }
            ]
          }
        }
      },
      "criterio_2_contextual": {
        "resultado": "string (PASS|FAIL)",
        "referencias_institucionales": {
          "coinciden": "bool",
          "explicacion": "string"
        },
        "alineacion": {
          "clasificacion": "string (ALIGNED|PARTIALLY_ALIGNED|NOT_ALIGNED)",
          "confianza": "float",
          "respaldo_jerarquico": "bool",
          "explicacion_respaldo": "string"
        },
        "razonamiento": "string",
        "evidencias": ["string"],
        "flags": [],
        "validaciones_adicionales": {
          "marco_legal": {
            "tiene_problemas": "bool",
            "total_problemas": "int",
            "problemas": [
              {
                "tipo": "string (ORGANISMO_EXTINTO|LEY_OBSOLETA|REFERENCIA_INVALIDA)",
                "severidad": "string (CRITICAL|HIGH|MODERATE|LOW)",
                "descripcion": "string",
                "sugerencia": "string"
              }
            ]
          },
          "objetivo_general": {
            "es_adecuado": "bool",
            "calificacion": "float (0.0-1.0)",
            "problemas": [
              {
                "tipo": "string (MUY_CORTO|MUY_LARGO|SIN_VERBO|SIN_FINALIDAD|GENERICO)",
                "severidad": "string",
                "descripcion": "string"
              }
            ]
          }
        }
      },
      "criterio_3_impacto": {
        "resultado": "string (PASS|FAIL)",
        "metricas": {
          "total_funciones": "int",
          "funciones_critical": "int",
          "funciones_moderate": "int",
          "funciones_low": "int",
          "tasa_critica": "float"
        },
        "detalles": {
          "critical_discrepancies": [...],
          "moderate_discrepancies": [...]
        }
      }
    },
    "accion_requerida": "string",
    "razonamiento": "string"
  },
  "metadata": {
    "version_sistema": "string (5.33)",
    "timestamp": "string (ISO 8601)",
    "duracion_segundos": "float"
  }
}
```

---

## 🔑 CAMPOS CRÍTICOS PARA EVITAR KeyErrors

### En `puesto`:
- ✅ **SIEMPRE incluir**: `codigo`, `denominacion`, `nivel`
- ✅ **ALIAS**: `nivel_salarial` = `nivel` (para compatibilidad)
- ✅ **DEFAULT**: `unidad_responsable = ""`

### En `validacion`:
- ✅ **SIEMPRE incluir**: `resultado`, `clasificacion`, `criterios_aprobados`, `confianza`
- ✅ **NUEVO**: `total_criterios = 3` (para evitar hardcoding)

### En cada criterio:
- ✅ **SIEMPRE incluir**: `resultado` (PASS|FAIL)
- ✅ **SIEMPRE incluir**: métricas básicas (totales, tasas)
- ✅ **NUEVO**: `validaciones_adicionales` (anidado, opcional pero estructurado)

---

## 🎯 INTEGRACIÓN CON VALIDACIONES ADICIONALES

### Criterio 1 - `validaciones_adicionales`:
```python
{
  "duplicacion": {
    "tiene_duplicados": bool,
    "total_duplicados": int,
    "pares_duplicados": [...]  # Lista de pares similares
  },
  "malformacion": {
    "tiene_malformadas": bool,
    "total_malformadas": int,
    "funciones_problemáticas": [...]  # Lista de funciones con problemas
  }
}
```

### Criterio 2 - `validaciones_adicionales`:
```python
{
  "marco_legal": {
    "tiene_problemas": bool,
    "total_problemas": int,
    "problemas": [...]  # Lista de problemas detectados
  },
  "objetivo_general": {
    "es_adecuado": bool,
    "calificacion": float,
    "problemas": [...]  # Lista de deficiencias
  }
}
```

---

## 🛡️ ESTRATEGIA DE ROBUSTEZ

1. **Campos REQUERIDOS siempre presentes** (con defaults si falla)
2. **Estructura anidada predecible** (no mezclar listas y diccionarios)
3. **Nombres consistentes** (nivel = nivel_salarial, nunca cambiar)
4. **Validaciones adicionales OPCIONALES** (si no hay, dict vacío)
5. **Tipos explícitos** (int, float, bool, string - nunca None en campos críticos)

---

## 📊 EJEMPLO REAL (CASO NEGATIVO - CONACYT)

```json
{
  "puesto": {
    "codigo": "38-100-1-M1C035P-0000002-E-X-V",
    "denominacion": "SECRETARIA DE CIENCIA, HUMANIDADES, TECNOLOGÍA E INNOVACIÓN",
    "nivel": "G11",
    "nivel_salarial": "G11",
    "unidad_responsable": "0"
  },
  "validacion": {
    "resultado": "RECHAZADO",
    "clasificacion": "DEFICIENTE",
    "criterios_aprobados": 1,
    "total_criterios": 3,
    "confianza": 0.85,
    "criterios": {
      "criterio_1_verbos": {
        "resultado": "FAIL",
        "tasa_critica": 0.87,
        "funciones_aprobadas": 1,
        "funciones_rechazadas": 40,
        "total_funciones": 46,
        "validaciones_adicionales": {
          "duplicacion": {
            "tiene_duplicados": true,
            "total_duplicados": 2,
            "pares_duplicados": [...]
          },
          "malformacion": {
            "tiene_malformadas": true,
            "total_malformadas": 5,
            "funciones_problemáticas": [...]
          }
        }
      },
      "criterio_2_contextual": {
        "resultado": "FAIL",
        "alineacion": {
          "clasificacion": "NOT_ALIGNED",
          "confianza": 0.95
        },
        "validaciones_adicionales": {
          "marco_legal": {
            "tiene_problemas": true,
            "total_problemas": 1,
            "problemas": [
              {
                "tipo": "ORGANISMO_EXTINTO",
                "descripcion": "Referencias a CONACYT que ya no existe"
              }
            ]
          }
        }
      },
      "criterio_3_impacto": {
        "resultado": "PASS",
        "tasa_critica": 0.02
      }
    }
  }
}
```

---

## ✅ COMPATIBILIDAD

- ✅ **report_humanizer.py**: Accede a `puesto['nivel']` ✓
- ✅ **results.py**: Accede a `puesto['nivel']` ✓
- ✅ **Estructura existente**: Mantiene todos los campos actuales ✓
- ✅ **Validaciones nuevas**: En campo anidado separado ✓

