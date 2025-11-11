# Cotización de Costos LLM - Sistema de Homologación APF v5.34

**Fecha:** Noviembre 2025
**Sistema:** Herramienta de Homologación v5.34
**Versión:** Con Criterio 3 usando LLM (sistema completo)
**Moneda Principal:** Pesos Mexicanos (MXN)
**Tipo de Cambio:** $20.00 MXN = $1.00 USD
**Análisis:** Costos por puesto validado con diferentes proveedores LLM

---

## 📋 RESUMEN EJECUTIVO

### Sistema v5.34: Validación Completa con 4 Componentes LLM

El sistema de homologación v5.34 utiliza **inteligencia artificial (LLM)** en todos sus componentes de validación:

1. **AdvancedQualityValidator** - Detecta duplicados, funciones malformadas, problemas legales
2. **Criterio 1: Análisis Semántico** - Evalúa la fortaleza de cada función (Protocolo SABG)
3. **Criterio 2: Validación Contextual** - Verifica respaldo normativo institucional
4. **Criterio 3: Impacto Jerárquico** - Valida coherencia con nivel del puesto ✅ **NUEVO en v5.34**

### Proveedores Analizados

- **OpenAI** (GPT-4o, GPT-4o-mini, GPT-3.5-turbo)
- **DeepSeek** (V3, V3.2-Exp)
- **Google Gemini** (2.5 Flash, 2.5 Pro)

### Caso de Uso Real

✅ **25 puestos de Turismo** analizados exitosamente
✅ **66,000 tokens promedio** por puesto (12 funciones)
✅ **26 llamadas LLM** por puesto validado

---

## 💰 PRECIOS ACTUALES (Noviembre 2025)

### 1. OpenAI

| Modelo | Input (MXN/1M tokens) | Output (MXN/1M tokens) | Input (USD/1M) | Output (USD/1M) | Uso Recomendado |
|--------|----------------------|------------------------|----------------|-----------------|-----------------|
| **GPT-4o** | $60.00 | $200.00 | $3.00 | $10.00 | Producción anterior |
| **GPT-4o-mini** | $3.00 | $12.00 | $0.15 | $0.60 | **Producción actual** ⭐ |
| **GPT-3.5-turbo** | $10.00 | $30.00 | $0.50 | $1.50 | Volumen alto |

**Ventajas:**
- GPT-4o-mini ofrece 90% de capacidad de GPT-4o a 95% menos costo
- Alta confiabilidad y disponibilidad
- Documentación extensa

### 2. DeepSeek

| Modelo | Cache Hit (MXN/1M) | Cache Miss (MXN/1M) | Output (MXN/1M) | Uso Recomendado |
|--------|-------------------|---------------------|-----------------|-----------------|
| **DeepSeek V3** | $1.40 | $11.20 | $33.60 | Volumen muy alto |
| **DeepSeek V3.2-Exp** | $0.60 | $5.60 | $8.40 | **Máxima economía** 🏆 |

**Ventajas:**
- Precio más bajo del mercado
- Cache hits con 75% descuento
- Ideal para procesos repetitivos

**Nota:** Precios finales (no promocionales) vigentes desde septiembre 2025.

### 3. Google Gemini

| Modelo | Input (MXN/1M tokens) | Output (MXN/1M tokens) | Input (USD/1M) | Output (USD/1M) | Uso Recomendado |
|--------|----------------------|------------------------|----------------|-----------------|-----------------|
| **Gemini 2.5 Flash** | $3.00 | $12.00 | $0.15 | $0.60 | Velocidad + economía |
| **Gemini 2.5 Flash (reasoning)** | $3.00 | $70.00 | $0.15 | $3.50 | Razonamiento complejo |
| **Gemini 2.5 Pro** | $25.00 | $200.00 | $1.25 | $10.00 | Máxima capacidad |

**Ventajas:**
- **Free tier:** 1,500 requests/día (45,000/mes) **GRATIS**
- Batch processing: 50% descuento
- Context caching: 75% ahorro en tokens repetidos

---

## 📈 USO ACTUAL DEL SISTEMA v5.34

### Llamadas LLM por Puesto Validado

| Componente | Llamadas | Model | Tokens Input | Tokens Output | Total Tokens |
|------------|----------|-------|--------------|---------------|--------------|
| **AdvancedQualityValidator** | 1 | gpt-4o-mini | ~2,500 | ~1,500 | 4,000 |
| **Criterio 1 (por función)** | N* | gpt-4o-mini | ~1,200 | ~800 | 2,000 |
| **Criterio 2 (contextual)** | 1 | gpt-4o-mini | ~1,000 | ~500 | 1,500 |
| **Criterio 3 (Impacto Jerárquico)** | N* | gpt-4o-mini | ~600 | ~400 | 1,000 |
| **TOTAL POR PUESTO** | **2N+2** | - | **~4,900N+7,000** | - | **~66,000** |

*N = número de funciones por puesto (promedio: 12)

### Ejemplo Real: Puesto con 12 Funciones

```
Llamadas LLM:
- AdvancedQualityValidator: 1 llamada
- Criterio 1: 12 llamadas (1 por función)
- Criterio 2: 1 llamada
- Criterio 3: 12 llamadas (1 por función)
- TOTAL: 26 llamadas

Tokens consumidos:
- Input:  3,700 × 12 + 4,500 = 48,900 tokens (~49K)
- Output: 1,200 × 12 + 2,500 = 16,900 tokens (~17K)
- TOTAL: 65,800 tokens (~66K por puesto)
```

### Análisis de 25 Puestos de Turismo (Real)

```
Funciones promedio: 12 por puesto
Total tokens input: 25 × 49K = 1,225,000 tokens (1.23M)
Total tokens output: 25 × 17K = 425,000 tokens (0.43M)
TOTAL: 1,650,000 tokens (1.65M)
```

---

## 💵 COSTO POR PUESTO - COMPARATIVA

### Escenario Base: Puesto con 12 Funciones (66K tokens)

| Proveedor | Modelo | Costo MXN | Costo USD | Ahorro vs GPT-4o |
|-----------|--------|-----------|-----------|------------------|
| **OpenAI** | GPT-4o | **$6.32** | $0.316 | - (base) |
| **OpenAI** | GPT-4o-mini | **$0.35** | $0.017 | **94.6%** ⭐ |
| **OpenAI** | GPT-3.5-turbo | **$0.99** | $0.049 | 84.5% |
| **DeepSeek** | V3 (cache miss) | **$1.10** | $0.055 | 82.6% |
| **DeepSeek** | V3 (cache 50%) | **$0.84** | $0.042 | 86.7% |
| **DeepSeek** | V3.2-Exp | **$0.42** | $0.021 | **93.4%** 🏆 |
| **Gemini** | 2.5 Flash | **$0.35** | $0.017 | **94.6%** ⭐ |
| **Gemini** | 2.5 Flash (reasoning) | **$1.33** | $0.066 | 79.1% |
| **Gemini** | 2.5 Pro | **$4.60** | $0.230 | 27.2% |
| **Gemini** | Free Tier | **$0.00** | $0.00 | **100%** 🎁 |

### Cálculos Detallados

#### OpenAI GPT-4o (Anterior)
```
Input:  48,900 tokens × $60.00/1M = $2.93 MXN ($0.147 USD)
Output: 16,900 tokens × $200.00/1M = $3.38 MXN ($0.169 USD)
TOTAL: $6.32 MXN ($0.316 USD) por puesto
```

#### OpenAI GPT-4o-mini (Actual - RECOMENDADO)
```
Input:  48,900 tokens × $3.00/1M = $0.15 MXN ($0.007 USD)
Output: 16,900 tokens × $12.00/1M = $0.20 MXN ($0.010 USD)
TOTAL: $0.35 MXN ($0.017 USD) por puesto

AHORRO: $5.97 MXN ($0.299 USD) por puesto = 94.6%
```

#### DeepSeek V3.2-Exp (Máxima Economía)
```
Input:  48,900 tokens × $5.60/1M = $0.27 MXN ($0.014 USD)
Output: 16,900 tokens × $8.40/1M = $0.14 MXN ($0.007 USD)
TOTAL: $0.42 MXN ($0.021 USD) por puesto

AHORRO: $5.90 MXN ($0.295 USD) por puesto = 93.4%
```

#### Gemini 2.5 Flash (Equilibrio)
```
Input:  48,900 tokens × $3.00/1M = $0.15 MXN ($0.007 USD)
Output: 16,900 tokens × $12.00/1M = $0.20 MXN ($0.010 USD)
TOTAL: $0.35 MXN ($0.017 USD) por puesto

AHORRO: $5.97 MXN ($0.299 USD) por puesto = 94.6%
```

---

## 📊 PROYECCIÓN DE COSTOS MENSUALES Y ANUALES

### Por Volumen de Puestos (Pesos Mexicanos)

| Volumen | Escenario | GPT-4o | GPT-4o-mini | DeepSeek V3.2 | Gemini Flash |
|---------|-----------|--------|-------------|---------------|--------------|
| **50** | Piloto | $316 | **$17** | $21 | $17 |
| **100** | Pequeño | $632 | **$35** | $42 | $35 |
| **500** | Mediano | $3,160 | **$175** | $210 | $175 |
| **1,000** | Grande | $6,320 | **$350** | $420 | $350 |
| **5,000** | Secretaría completa | $31,600 | **$1,750** | $2,100 | $1,750 |
| **50,000** | Gobierno Federal | $316,000 | **$17,500** | $21,000 | $17,500 |

### Ahorro Anual: Secretaría Típica (5,000 puestos/año)

| Comparación | Costo Anual MXN | Costo Anual USD | Ahorro MXN | Ahorro USD |
|-------------|-----------------|-----------------|------------|------------|
| GPT-4o (anterior) | $31,600 | $1,580 | - | - |
| **GPT-4o-mini** ⭐ | **$1,750** | **$88** | **$29,850** | **$1,492** |
| **DeepSeek V3.2** | **$2,100** | **$105** | **$29,500** | **$1,475** |
| **Gemini Flash** | **$1,750** | **$88** | **$29,850** | **$1,492** |

### Proyección Mensual (Diferentes Volúmenes)

| Puestos/Mes | GPT-4o MXN/mes | GPT-4o-mini MXN/mes | Ahorro MXN/mes |
|-------------|----------------|---------------------|----------------|
| 100 | $632 | $35 | $597 (94.6%) |
| 250 | $1,580 | $88 | $1,493 (94.5%) |
| 500 | $3,160 | $175 | $2,985 (94.5%) |
| 1,000 | $6,320 | $350 | $5,970 (94.5%) |
| 2,000 | $12,640 | $700 | $11,940 (94.5%) |

---

## 🎯 PLANES Y OPCIONES DISPONIBLES

### OpenAI

**Modalidad:** Pay-as-you-go (pago por uso)

- Sin planes mensuales fijos
- Créditos prepagados disponibles
- Límites de rate configurables por organización
- Facturación mensual en USD (convertir a MXN al tipo de cambio del día)

**Cómo contratar:**
1. Crear cuenta en https://platform.openai.com
2. Agregar método de pago (tarjeta de crédito internacional)
3. Configurar límites de gasto mensuales
4. Obtener API key para el sistema

**Recomendación:** Configurar límite de $100 USD/mes para pruebas, luego ajustar según necesidad.

### DeepSeek

**Modalidad:** Pay-as-you-go

- Precio más bajo del mercado
- Cache hits con 75% descuento automático
- No hay planes mensuales oficiales
- Facturación en USD

**Cómo contratar:**
1. Registrarse en https://platform.deepseek.com
2. Verificar cuenta
3. Agregar créditos (mínimo $5 USD)
4. Obtener API key

**Ventaja:** Ideal para volúmenes muy altos (>10,000 puestos/mes).

### Google Gemini

**Modalidad:** Free tier + Pay-as-you-go

**Free Tier (GRATIS):**
- ✅ 1,500 requests/día
- ✅ 45,000 requests/mes
- ✅ Suficiente para ~45,000 puestos/mes
- ✅ Sin tarjeta de crédito requerida

**API Pagada:**
- Batch processing: 50% descuento
- Context caching: 75% ahorro en tokens repetidos
- Vertex AI: Facturación empresarial con descuentos por volumen

**Cómo contratar Free Tier:**
1. Crear proyecto en https://aistudio.google.com
2. Activar Gemini API (gratis)
3. Obtener API key
4. Usar hasta 1,500 puestos/día sin costo

**Proyección con Free Tier:**
```
45,000 puestos/mes × $0 = $0 MXN/mes
Ahorro vs GPT-4o: $284,400 MXN/mes (100%)
```

**Recomendación:** Iniciar con Free Tier, migrar a API pagada solo si se excede el límite.

---

## 💡 RECOMENDACIONES POR ESCENARIO

### Escenario 1: Secretaría Pequeña (<500 puestos/mes)

**Recomendación:** 🎁 **Gemini Free Tier**

```
Costo: $0 MXN/mes
Límite: 1,500 puestos/día (suficiente)
Calidad: Equivalente a GPT-4o-mini
```

**Ventajas:**
- Costo cero
- Sin tarjeta de crédito
- Perfecto para volúmenes bajos

### Escenario 2: Secretaría Mediana (500-2,000 puestos/mes)

**Recomendación:** ⭐ **GPT-4o-mini**

```
Costo: $175-700 MXN/mes
Ahorro vs GPT-4o: $2,985-5,970 MXN/mes
ROI: Excelente relación calidad/precio
```

**Ventajas:**
- Alta confiabilidad de OpenAI
- 90% de capacidad de GPT-4o
- Documentación extensa
- Soporte empresarial

### Escenario 3: Secretaría Grande (2,000-10,000 puestos/mes)

**Recomendación:** 🏆 **DeepSeek V3.2-Exp**

```
Costo: $840-4,200 MXN/mes
Ahorro vs GPT-4o: 93.4%
Cache hits: 75% descuento adicional
```

**Ventajas:**
- Precio más bajo del mercado
- Ahorro significativo en volumen alto
- Cache optimizado para uso repetitivo

### Escenario 4: Gobierno Federal (>10,000 puestos/mes)

**Recomendación:** 🔄 **Modelo Híbrido**

```
85% de casos: GPT-4o-mini ($0.35 MXN)
10% casos complejos: GPT-4o ($6.32 MXN)
5% casos simples: Gemini Free ($0 MXN)
Costo promedio: ~$0.66 MXN/puesto
```

**Proyección anual (50,000 puestos):**
```
Costo: $33,000 MXN/año
Ahorro vs GPT-4o puro: $283,000 MXN/año (89.6%)
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN RECOMENDADO

### Fase 1: Migración Inmediata (Semana 1)

**Acción:** Cambiar de GPT-4o a GPT-4o-mini

**Pasos:**
1. ✅ Ya completado - Sistema migrado a GPT-4o-mini
2. Ejecutar análisis de 10-20 puestos de prueba
3. Comparar calidad vs análisis anteriores
4. Confirmar ahorro en dashboard de OpenAI

**Ahorro inmediato:**
```
De $6.32 → $0.35 MXN por puesto
Ahorro: $5.97 MXN por puesto (94.6%)
```

**ROI:** Con solo 100 puestos recuperas cualquier costo de configuración.

### Fase 2: Evaluación de Free Tier (Semana 2-3)

**Acción:** Probar Gemini Free Tier en paralelo

**Pasos:**
1. Crear cuenta en Google AI Studio
2. Obtener API key gratuita
3. Configurar como proveedor alternativo
4. Ejecutar 100 puestos de prueba
5. Comparar calidad vs GPT-4o-mini

**Potencial:**
```
Si calidad es equivalente: $0 MXN/mes indefinidamente
Hasta 45,000 puestos/mes gratis
```

### Fase 3: Optimización Avanzada (Mes 2-3)

**Acción:** Implementar modelo híbrido inteligente

**Lógica de selección:**
```python
if num_funciones > 20 or nivel in ['G11', 'H21']:
    model = "gpt-4o"  # Casos muy complejos (5%)
elif puestos_hoy < 1500:
    model = "gemini-2.5-flash"  # Free tier (5%)
else:
    model = "gpt-4o-mini"  # Default (90%)
```

**Resultado esperado:**
```
Ahorro adicional: 10-15%
Costo promedio: $0.30 MXN/puesto
```

---

## 📊 COMPARATIVA FINAL: CUADRO RESUMEN

### Por Costo Total/Puesto (Pesos Mexicanos)

| Ranking | Modelo | MXN/Puesto | USD/Puesto | Ahorro | Disponibilidad |
|---------|--------|------------|------------|--------|----------------|
| 🥇 | **Gemini Free Tier** | **$0.00** | $0.00 | 100% | 1,500/día |
| 🥈 | **GPT-4o-mini** | **$0.35** | $0.017 | 94.6% | Ilimitado |
| 🥉 | **Gemini 2.5 Flash** | **$0.35** | $0.017 | 94.6% | Ilimitado |
| 4 | DeepSeek V3.2-Exp | $0.42 | $0.021 | 93.4% | Ilimitado |
| 5 | DeepSeek V3 (cache) | $0.84 | $0.042 | 86.7% | Ilimitado |
| 6 | GPT-3.5-turbo | $0.99 | $0.049 | 84.5% | Ilimitado |
| 7 | DeepSeek V3 | $1.10 | $0.055 | 82.6% | Ilimitado |
| 8 | Gemini Flash (reasoning) | $1.33 | $0.066 | 79.1% | Ilimitado |
| 9 | Gemini 2.5 Pro | $4.60 | $0.230 | 27.2% | Ilimitado |
| 10 | GPT-4o (anterior) | $6.32 | $0.316 | - | Ilimitado |

### Por Volumen Anual: 5,000 Puestos (Secretaría Típica)

| Modelo | Costo Anual MXN | Costo Mensual MXN | Ahorro Anual MXN | ROI |
|--------|-----------------|-------------------|------------------|-----|
| GPT-4o (anterior) | $31,600 | $2,633 | - | - |
| **GPT-4o-mini** ⭐ | **$1,750** | **$146** | **$29,850** | **1,706%** |
| **DeepSeek V3.2** | **$2,100** | **$175** | **$29,500** | **1,405%** |
| **Gemini Flash** | **$1,750** | **$146** | **$29,850** | **1,706%** |
| **Gemini Free** 🎁 | **$0** | **$0** | **$31,600** | **∞** |

---

## 🔍 ANÁLISIS DE ROI

### Inversión Inicial

**Costo de implementación/migración:** ~$5,000 MXN (1 semana de trabajo)

### Recuperación de Inversión

Con GPT-4o-mini ahorrando $5.97 MXN por puesto:

```
Punto de equilibrio: 838 puestos
Tiempo estimado: 1-2 meses (secretaría típica)
```

### Ahorro Proyectado a 3 Años (5,000 puestos/año)

```
Año 1: $29,850 MXN de ahorro
Año 2: $29,850 MXN de ahorro
Año 3: $29,850 MXN de ahorro
TOTAL 3 AÑOS: $89,550 MXN de ahorro

Menos inversión inicial: -$5,000 MXN
AHORRO NETO: $84,550 MXN en 3 años
```

---

## 📝 NOTAS IMPORTANTES

### Tipo de Cambio

- **Actual:** $20.00 MXN = $1.00 USD
- Los precios en MXN son aproximados y sujetos a variación del tipo de cambio
- Revisar tipo de cambio mensualmente en facturación

### Facturación

- **OpenAI y DeepSeek:** Facturan en USD, se convierte a MXN al pagar
- **Gemini:** Puede facturar en MXN si se usa Vertex AI con cuenta mexicana
- Usar tarjeta de crédito internacional para pagos en USD

### Impuestos

- Precios NO incluyen IVA (16% en México)
- Agregar IVA al calcular costo final para presupuesto gubernamental

**Ejemplo con IVA:**
```
GPT-4o-mini: $0.35 MXN + 16% IVA = $0.41 MXN por puesto
5,000 puestos/año: $1,750 + 16% = $2,030 MXN/año
```

### Actualizaciones de Precios

- Precios válidos: Noviembre 2025
- Revisar pricing pages cada trimestre
- OpenAI tiende a bajar precios periódicamente
- DeepSeek y Gemini son más estables

---

## 🎯 RECOMENDACIÓN FINAL

### Para Implementación Inmediata

**Opción 1: Presupuesto Sin Restricciones**
- Usar **GPT-4o-mini** de OpenAI
- Costo: **$1,750 MXN/año** (5,000 puestos)
- Confiabilidad máxima
- Soporte empresarial

**Opción 2: Presupuesto Limitado**
- Usar **Gemini Free Tier**
- Costo: **$0 MXN/año** (hasta 45,000 puestos/mes)
- Calidad equivalente
- Gratis indefinidamente

**Opción 3: Máxima Economía con Volumen Alto**
- Usar **DeepSeek V3.2-Exp**
- Costo: **$2,100 MXN/año** (5,000 puestos)
- Precio más bajo del mercado
- Cache optimizado

### Plan Recomendado: Híbrido Inteligente

```
Mes 1-3: GPT-4o-mini (estabilizar sistema)
Mes 4-6: Probar Gemini Free Tier en paralelo
Mes 7+: Modelo híbrido optimizado (90% GPT-4o-mini, 5% GPT-4o, 5% Gemini)

Ahorro proyectado: $28,000-30,000 MXN/año
Calidad: Mantenida o mejorada
Riesgo: Mínimo
```

---

## 📞 INFORMACIÓN DE CONTACTO

### Proveedores

**OpenAI:**
- Web: https://openai.com/api/pricing/
- Docs: https://platform.openai.com/docs/pricing
- Soporte: platform.openai.com/docs

**DeepSeek:**
- Web: https://api-docs.deepseek.com/
- Pricing: https://api-docs.deepseek.com/quick_start/pricing
- API: api.deepseek.com

**Google Gemini:**
- Web: https://ai.google.dev/
- Pricing: https://ai.google.dev/gemini-api/docs/pricing
- Free tier: https://ai.google.dev/pricing

### Calculadoras de Costos Online

- OpenAI: https://docsbot.ai/tools/gpt-openai-api-pricing-calculator
- Gemini: https://invertedstone.com/calculators/gemini-pricing
- Comparador: https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025

---

## 🔄 HISTORIAL DE VERSIONES

**v5.34 (Noviembre 2025):**
- Criterio 3 ahora usa LLM (antes era solo reglas)
- Incremento: 45K → 66K tokens por puesto (+47%)
- Costo actualizado: $0.012 → $0.017 USD ($0.24 → $0.35 MXN)
- Beneficio: Mayor precisión en validación de impacto jerárquico

**v5.33 (Noviembre 2025):**
- Sistema completo con validaciones adicionales de calidad
- AdvancedQualityValidator agregado
- Costo: ~45K tokens por puesto

---

**Documento creado:** Noviembre 2025
**Sistema:** Herramienta de Homologación APF v5.34
**Próxima revisión:** Diciembre 2025 (actualizar tipo de cambio y precios)

**FIN DEL DOCUMENTO**
