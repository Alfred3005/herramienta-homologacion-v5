# Guía de Procesamiento en Lote - Sistema Sidegor

**Fecha**: 2025-11-04
**Versión**: 1.0
**Estado**: Implementado y probado ✅

---

## 📋 Resumen

Sistema completo para procesar masivamente puestos desde archivos Excel Sidegor, generar documentos virtuales en formato RHNet y crear reportes consolidados.

### Funcionalidades Implementadas

✅ **Sistema de filtros modular** (niveles, UR, códigos con wildcards)
✅ **Adaptador Sidegor** (Excel → Formato APF)
✅ **Generador de documentos RHNet** (APF → TXT compatible con pipeline)
✅ **Procesador en lote** (procesamiento secuencial masivo)
✅ **Reportes consolidados** (JSON, Excel, TXT)
✅ **Estadísticas por nivel** (agregación y análisis)

---

## 🚀 Quick Start

### Ejemplo Básico

```bash
cd /home/alfred/herramienta-homologacion-v5

# Procesar TURISMO niveles 1-2
python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx" \
  "1,2"
```

### Resultado

```
📊 Puestos encontrados: 169
✅ Procesados: 169 (100.0% éxito)
⏱️  Duración: 0.8 segundos

📁 Archivos generados:
   • 169 documentos RHNet
   • 169 archivos JSON APF
   • Reporte consolidado (JSON + Excel)
   • Estadísticas por nivel
```

---

## 📚 Archivos Disponibles

Actualmente en `validación comparativa con otras URs/`:

| Archivo | Tamaño | Puestos | Descripción |
|---------|---------|---------|-------------|
| `Reporte_DPP_06_000_03-11-2025 HACIENDA SC.xlsx` | 8.0 MB | ~? | Secretaría de Hacienda |
| `Reporte_DPP_08_000_03-11-2025 SADER SC.xlsx` | 5.9 MB | ~? | Secretaría de Agricultura |
| `Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx` | 791 KB | 1,439 | Secretaría de Turismo ✅ |
| `Reporte_DPP_48_000_03-11-2025 CULTURA SC.xlsx` | 2.4 MB | ~? | Secretaría de Cultura |

**Para SABG**: Se requiere archivo `Reporte_DPP_27_000_SABG.xlsx` (no disponible actualmente)

---

## 🔧 Uso Detallado

### Sintaxis Completa

```bash
python scripts/procesar_lote_sidegor.py <archivo_excel> "<niveles>" [ur]
```

**Parámetros**:
- `<archivo_excel>`: Ruta al archivo Excel de Sidegor
- `"<niveles>"`: Lista de niveles separados por comas (ej: "1,2,3" o "G,H,I,J,K")
- `[ur]` (opcional): Código de Unidad Responsable

### Ejemplos de Uso

#### 1. Procesar niveles específicos

```bash
# Turismo - niveles 1 y 2
python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx" \
  "1,2"
```

#### 2. Procesar con filtro de UR

```bash
# Hacienda - niveles 1,2,3 con UR=06
python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_06_000_03-11-2025 HACIENDA SC.xlsx" \
  "1,2,3" \
  "06"
```

#### 3. Procesar múltiples niveles

```bash
# Cultura - niveles 1 a 4
python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_48_000_03-11-2025 CULTURA SC.xlsx" \
  "1,2,3,4"
```

---

## 📊 Estructura de Salida

### Directorio Generado

```
output/<nombre_archivo>_niveles_<niveles>/
├── documentos/                      # Documentos RHNet (.txt)
│   ├── 21-510-1-M1C014P-..._rhnet.txt
│   ├── 21-410-1-M1C015P-..._rhnet.txt
│   └── ...
├── datos_apf/                       # Datos APF en JSON
│   ├── 21-510-1-M1C014P-..._apf.json
│   ├── 21-410-1-M1C015P-..._apf.json
│   └── ...
├── reporte_consolidado.json         # Reporte completo (JSON)
├── reporte_consolidado.xlsx         # Reporte Excel (4 hojas)
└── resumen.txt                      # Resumen ejecutivo
```

### Formato de Documento RHNet

```
Puesto: 21-510-1-M1C014P-0000283-E-U-S
Nombre	JEFATURA DE DEPARTAMENTO	Caracter ocupacional	CUMPLIMIENTO A UN LAUDO
Nivel salarial	2.0	Estatus	No especificado
Ramo	21	Unidad Responsable	0

Objetivo General y Funciones.
Objetivo General
APOYAR LAS ACTIVIDADES DEL TITULAR...

Función 1
ESTABLECER COMUNICACIÓN PERMANENTE...
Función 2
DAR SEGUIMIENTO A LA AGENDA...

Perfil.
Escolaridad
Nivel de Estudios:	LICENCIATURA O PROFESIONAL
Grado de Avance:	TITULADO
...
```

### Reporte Excel (4 Hojas)

1. **Resumen**: Estadísticas globales
   - Total puestos, procesados, exitosos, fallidos
   - Tasa de éxito, duración
   - Filtros aplicados

2. **Detalle**: Fila por cada puesto
   - Código, denominación, nivel, UR
   - Status de conversión
   - Número de funciones
   - Ruta al documento generado

3. **Errores**: Puestos fallidos (si los hay)
   - Código, status, mensaje de error

4. **Por Nivel**: Estadísticas agregadas por nivel salarial
   - Total, exitosos, fallidos por nivel
   - Tasa de éxito por nivel

---

## 🎯 Casos de Uso Prácticos

### Caso 1: Validar Puestos SABG G-K (Cuando esté disponible)

**Objetivo**: Procesar todos los puestos SABG de niveles G a K para validación posterior

```bash
# Prerequisito: Tener archivo Reporte_DPP_27_000_SABG.xlsx

python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_27_000_SABG.xlsx" \
  "G,H,I,J,K" \
  "27"
```

**Salida esperada**:
- ~50-150 puestos procesados (depende del archivo)
- Documentos RHNet listos para validación
- Reporte consolidado con estadísticas

**Siguiente paso**:
- Usar documentos RHNet generados con el pipeline de validación APF
- Validar contra normativa SABG

### Caso 2: Análisis Comparativo de Niveles entre URs

**Objetivo**: Comparar puestos de nivel 1 y 2 entre diferentes secretarías

```bash
# Procesar TURISMO
python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx" \
  "1,2"

# Procesar CULTURA
python scripts/procesar_lote_sidegor.py \
  "validación comparativa con otras URs/Reporte_DPP_48_000_03-11-2025 CULTURA SC.xlsx" \
  "1,2"

# Comparar reportes Excel manualmente
```

### Caso 3: Extracción Masiva para Análisis

**Objetivo**: Extraer todos los puestos de niveles bajos (1-3) para análisis estadístico

```bash
# Procesar todos los archivos disponibles
for archivo in "validación comparativa con otras URs"/*.xlsx; do
    nombre=$(basename "$archivo" .xlsx)
    echo "Procesando: $nombre"

    python scripts/procesar_lote_sidegor.py \
      "$archivo" \
      "1,2,3" \
      > "logs/${nombre}_procesamiento.log" 2>&1
done
```

---

## 🔍 Sistema de Filtros

### Filtros Disponibles

#### 1. Filtro por Nivel Salarial

```python
from src.filters import NivelSalarialFilter

# Niveles numéricos
filtro = NivelSalarialFilter(["1", "2", "3"])

# Niveles alfabéticos (para archivos que los usen)
filtro = NivelSalarialFilter(["G", "H", "I", "J", "K"])

# Mixto
filtro = NivelSalarialFilter(["K", "L", "M1", "M2", "M3"])
```

#### 2. Filtro por Unidad Responsable (UR)

```python
from src.filters import URFilter

# UR única
filtro = URFilter(["27"])  # SABG

# Múltiples URs
filtro = URFilter(["21", "06", "48"])  # TURISMO, HACIENDA, CULTURA
```

#### 3. Filtro por Código de Puesto

```python
from src.filters import CodigoPuestoFilter

# Código exacto
filtro = CodigoPuestoFilter(["21-510-1-M1C014P-0000283-E-U-S"])

# Wildcards
filtro = CodigoPuestoFilter([
    "21-510-*",    # Todos los puestos de 21-510
    "27-100-*",    # Todos los puestos de 27-100
    "06-*"         # Todos los puestos de UR 06
])
```

#### 4. Filtros Compuestos (AND/OR)

```python
from src.filters import CompositeFilter, NivelSalarialFilter, URFilter

# AND: Nivel G-K Y UR=27
filtro_nivel = NivelSalarialFilter(["G", "H", "I", "J", "K"])
filtro_ur = URFilter(["27"])
filtro_compuesto = CompositeFilter([filtro_nivel, filtro_ur], logic="AND")

# OR: Nivel K O Nivel L
filtro_k = NivelSalarialFilter(["K"])
filtro_l = NivelSalarialFilter(["L"])
filtro_compuesto = CompositeFilter([filtro_k, filtro_l], logic="OR")
```

---

## 💻 Uso Programático

### Ejemplo Completo

```python
from src.adapters import (
    SidegorAdapter,
    RHNetDocumentGenerator,
    SidegorBatchProcessor
)
from src.filters import NivelSalarialFilter, URFilter
from src.reporting import BatchReporter

# 1. Cargar archivo
adapter = SidegorAdapter()
adapter.cargar_archivo("validación comparativa con otras URs/Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx")

# 2. Configurar generador
generator = RHNetDocumentGenerator(template="default")

# 3. Crear procesador
processor = SidegorBatchProcessor(
    adapter=adapter,
    document_generator=generator,
    validation_pipeline=None  # Opcional
)

# 4. Agregar filtros
processor.add_filter(NivelSalarialFilter(["1", "2"]))
processor.add_filter(URFilter(["0"]))  # UR de TURISMO

# 5. Procesar lote
resultado = processor.procesar_lote(
    validar=False,
    generar_documentos=True,
    output_dir="output/mi_proceso",
    guardar_intermedios=True
)

# 6. Generar reportes
reporter = BatchReporter(resultado)
reporter.generar_reporte_excel("output/mi_reporte.xlsx")
reporter.generar_reporte_json("output/mi_reporte.json")
reporter.imprimir_estadisticas_por_nivel()

# 7. Ver resultados
print(resultado.get_summary())
```

---

## 📈 Métricas y Estadísticas

### Reporte JSON Generado

```json
{
  "resumen": {
    "total_puestos": 169,
    "procesados": 169,
    "exitosos": 169,
    "fallidos": 0,
    "tasa_exito": 100.0,
    "tiempo_inicio": "2025-11-04 00:29:13",
    "tiempo_fin": "2025-11-04 00:29:14",
    "duracion_segundos": 0.8
  },
  "filtros_aplicados": [
    "Nivel salarial: 1, 2"
  ],
  "resultados": [
    {
      "codigo": "21-510-1-M1C014P-0000283-E-U-S",
      "denominacion": "JEFATURA DE DEPARTAMENTO",
      "nivel": "2.0",
      "ur": "0",
      "status": "success",
      "conversion_status": "completa",
      "num_funciones": 5,
      "documento_path": "output/.../21-510-1-M1C014P-..._rhnet.txt",
      "validacion": null
    },
    ...
  ]
}
```

### Estadísticas por Nivel

```
Nivel 1.0:
  Total: 82
  Exitosos: 82 (100.0%)
  Fallidos: 0

Nivel 2.0:
  Total: 87
  Exitosos: 87 (100.0%)
  Fallidos: 0
```

---

## ⚠️ Notas Importantes

### Formato de Niveles

**Los archivos actuales usan niveles NUMÉRICOS (1, 2, 3, 4) no alfabéticos (G, H, I, J, K)**.

Si se requiere procesar archivos con niveles alfabéticos (como sería SABG), usar:
```bash
python scripts/procesar_lote_sidegor.py archivo.xlsx "G,H,I,J,K"
```

### Unidad Responsable (UR)

- **TURISMO**: UR = 0
- **SABG**: UR = 27 (cuando esté disponible)
- **HACIENDA**: UR = 06
- **SADER**: UR = 08
- **CULTURA**: UR = 48

Verificar valor correcto de UR en cada archivo antes de filtrar.

### Validación con Pipeline APF

Actualmente el sistema **NO ejecuta validación** (parámetro `validar=False`).

Para habilitar validación en el futuro:
1. Configurar `validation_pipeline` con un `APFExtractor`
2. Pasar `validar=True` al procesar lote
3. Los resultados incluirán campo `validacion` con resultado de cada puesto

---

## 🔮 Próximos Pasos

### Implementación Pendiente

- [ ] Integrar con `ContextualValidator` para validación automática
- [ ] Implementar procesamiento paralelo para mayor velocidad
- [ ] Agregar soporte para múltiples archivos en un solo comando
- [ ] Crear comparador de reportes entre diferentes URs
- [ ] Implementar exportación a otros formatos (CSV, PDF)

### Para SABG Niveles G-K

1. **Obtener archivo**: `Reporte_DPP_27_000_SABG.xlsx`
2. **Ejecutar procesamiento**:
   ```bash
   python scripts/procesar_lote_sidegor.py \
     "validación comparativa con otras URs/Reporte_DPP_27_000_SABG.xlsx" \
     "G,H,I,J,K" \
     "27"
   ```
3. **Validar documentos generados** contra normativa SABG
4. **Generar informe** de puestos alineados/no alineados

---

## 📞 Soporte y Troubleshooting

### Errores Comunes

**Error: "No se encontraron puestos con los filtros especificados"**
- Verificar que los niveles existen en el archivo
- Revisar formato de niveles (numérico vs alfabético)
- Comprobar valor correcto de UR

**Error: "Archivo no encontrado"**
- Verificar ruta completa del archivo
- Usar comillas si el nombre tiene espacios
- Ejecutar desde directorio raíz del proyecto

**Error: "pandas no disponible"**
```bash
pip install pandas openpyxl
```

### Logs y Debugging

Para ver más detalles durante procesamiento:
```bash
python scripts/procesar_lote_sidegor.py archivo.xlsx "1,2" 2>&1 | tee procesamiento.log
```

---

**Documento creado**: 2025-11-04
**Última actualización**: 2025-11-04
**Versión**: 1.0
**Estado**: ✅ Sistema completo y probado

**Prueba realizada**:
- ✅ TURISMO niveles 1-2: 169 puestos (100% éxito, 0.8s)
- ✅ Generación de documentos RHNet
- ✅ Reportes consolidados (JSON + Excel)
- ✅ Estadísticas por nivel
