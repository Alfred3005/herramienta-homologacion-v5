# Diseño: Sistema de Procesamiento en Lote Sidegor → RHNet → Validación

**Fecha**: 2025-11-03
**Objetivo**: Procesar masivamente puestos desde bases de datos Excel Sidegor, generar documentos virtuales RHNet y validarlos secuencialmente
**Versión**: 1.0

---

## 🎯 Requisitos del Sistema

### Funcionalidad Principal
Tomar bases de datos Excel de Sidegor y:
1. **Filtrar** puestos por criterios específicos (nivel salarial, UR, código, etc.)
2. **Convertir** datos tabulares a formato RHNet (texto simulado)
3. **Validar** secuencialmente cada puesto contra normativa
4. **Generar reportes** consolidados de validación masiva

### Casos de Uso

**Caso 1**: Validar todos los puestos de SABG de nivel G a K
```python
processor.procesar_lote(
    archivo="Reporte_DPP_27_SABG.xlsx",
    filtros={
        "niveles": ["G", "H", "I", "J", "K"],
        "ur": "27"
    },
    normativa="reglamento_sabg.txt"
)
```

**Caso 2**: Validar puestos específicos de HACIENDA
```python
processor.procesar_lote(
    archivo="Reporte_DPP_06_HACIENDA.xlsx",
    filtros={
        "codigos": ["06-100-1-M1C035P-*"],  # Wildcard
        "grupo_personal": "Mando"
    }
)
```

**Caso 3**: Comparar múltiples URs
```python
processor.procesar_multiples_urs(
    archivos=[
        "Reporte_DPP_27_SABG.xlsx",
        "Reporte_DPP_06_HACIENDA.xlsx",
        "Reporte_DPP_21_TURISMO.xlsx"
    ],
    filtros_comunes={"niveles": ["K", "L", "M"]},
    comparar=True
)
```

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
src/
├── adapters/
│   ├── sidegor_adapter.py         # Adaptador base (ya existe en script)
│   ├── sidegor_batch_processor.py # NUEVO: Procesamiento en lote
│   └── rhnet_document_generator.py # NUEVO: Generador documentos RHNet
│
├── filters/
│   ├── base_filter.py             # NUEVO: Clase base para filtros
│   ├── nivel_filter.py            # NUEVO: Filtro por nivel salarial
│   ├── ur_filter.py               # NUEVO: Filtro por UR
│   └── codigo_filter.py           # NUEVO: Filtro por código (wildcards)
│
├── pipeline/
│   ├── batch_validation_pipeline.py # NUEVO: Pipeline validación masiva
│   └── apf_pipeline.py             # Existente: Pipeline individual
│
└── reporting/
    ├── batch_reporter.py           # NUEVO: Reportes consolidados
    └── comparison_reporter.py      # NUEVO: Comparaciones entre URs
```

### Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│  1. CARGA Y FILTRADO                                        │
├─────────────────────────────────────────────────────────────┤
│  Excel Sidegor → SidegorAdapter → Filtros → Lista Puestos  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. CONVERSIÓN A RHNET                                      │
├─────────────────────────────────────────────────────────────┤
│  Datos Tabular → RHNetGenerator → Documento TXT Virtual    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. VALIDACIÓN SECUENCIAL                                   │
├─────────────────────────────────────────────────────────────┤
│  Doc RHNet → APFExtractor → ContextualValidator → Resultado│
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. AGREGACIÓN Y REPORTE                                    │
├─────────────────────────────────────────────────────────────┤
│  Resultados → BatchReporter → Reporte Consolidado + Stats  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Diseño Detallado de Componentes

### 1. Sistema de Filtros (Filter Pattern)

**Principio SOLID**: Open/Closed Principle - extensible sin modificar código

```python
# filters/base_filter.py
class PuestoFilter(Protocol):
    """Interface para filtros de puestos"""

    def match(self, puesto_data: Dict[str, Any]) -> bool:
        """Retorna True si el puesto cumple el criterio"""
        ...

    def get_description(self) -> str:
        """Descripción del filtro para logs"""
        ...

# filters/nivel_filter.py
class NivelSalarialFilter:
    """Filtra por rango de niveles salariales (G-K, M1-M5, etc.)"""

    def __init__(self, niveles: List[str]):
        self.niveles = niveles

    def match(self, puesto_data: Dict[str, Any]) -> bool:
        nivel = puesto_data.get('GRADO', '')
        return nivel in self.niveles

# filters/ur_filter.py
class URFilter:
    """Filtra por Unidad Responsable"""

    def __init__(self, ur_codes: List[str]):
        self.ur_codes = ur_codes

    def match(self, puesto_data: Dict[str, Any]) -> bool:
        ur = str(puesto_data.get('UR', ''))
        return ur in self.ur_codes

# filters/codigo_filter.py
class CodigoPuestoFilter:
    """Filtra por patrón de código (soporta wildcards)"""

    def __init__(self, patrones: List[str]):
        self.patrones = patrones  # Ej: ["27-100-*", "27-244-*"]

    def match(self, puesto_data: Dict[str, Any]) -> bool:
        codigo = puesto_data.get('CÓDIGO_DE_PUESTO', '')
        return any(self._match_pattern(codigo, p) for p in self.patrones)

    def _match_pattern(self, codigo: str, pattern: str) -> bool:
        # Lógica de wildcard matching
        import re
        regex = pattern.replace('*', '.*')
        return bool(re.match(regex, codigo))

# filters/composite_filter.py
class CompositeFilter:
    """Combina múltiples filtros con lógica AND/OR"""

    def __init__(self, filters: List[PuestoFilter], logic: str = "AND"):
        self.filters = filters
        self.logic = logic

    def match(self, puesto_data: Dict[str, Any]) -> bool:
        if self.logic == "AND":
            return all(f.match(puesto_data) for f in self.filters)
        elif self.logic == "OR":
            return any(f.match(puesto_data) for f in self.filters)
        else:
            raise ValueError(f"Logic inválida: {self.logic}")
```

### 2. Procesador en Lote

**Principio SOLID**: Single Responsibility - solo coordina procesamiento en lote

```python
# adapters/sidegor_batch_processor.py
class SidegorBatchProcessor:
    """
    Procesador en lote de puestos desde Excel Sidegor.
    Coordina filtrado, conversión y validación masiva.
    """

    def __init__(self,
                 adapter: SidegorAdapter,
                 document_generator: RHNetDocumentGenerator,
                 validation_pipeline: Optional[APFExtractor] = None):
        self.adapter = adapter
        self.generator = document_generator
        self.pipeline = validation_pipeline
        self.filtros = []

    def add_filter(self, filtro: PuestoFilter):
        """Agrega filtro al procesador"""
        self.filtros.append(filtro)

    def clear_filters(self):
        """Limpia todos los filtros"""
        self.filtros.clear()

    def obtener_puestos_filtrados(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los puestos que cumplen los filtros.

        Returns:
            Lista de códigos de puesto que pasan filtros
        """
        if 'PUESTOS' not in self.adapter.extractor.hojas:
            raise ValueError("Hoja PUESTOS no cargada")

        df_puestos = self.adapter.extractor.hojas['PUESTOS']
        puestos_filtrados = []

        for idx, row in df_puestos.iterrows():
            puesto_dict = row.to_dict()

            # Aplicar todos los filtros
            if all(f.match(puesto_dict) for f in self.filtros):
                puestos_filtrados.append(puesto_dict)

        return puestos_filtrados

    def procesar_lote(self,
                     validar: bool = True,
                     generar_documentos: bool = True,
                     output_dir: str = "output/batch") -> BatchProcessingResult:
        """
        Procesa lote completo de puestos filtrados.

        Args:
            validar: Si ejecutar validación con pipeline
            generar_documentos: Si generar documentos RHNet
            output_dir: Directorio de salida

        Returns:
            BatchProcessingResult con estadísticas y resultados
        """
        # Obtener puestos filtrados
        puestos = self.obtener_puestos_filtrados()

        print(f"🔍 Filtros aplicados: {len(self.filtros)}")
        print(f"📋 Puestos encontrados: {len(puestos)}")

        if len(puestos) == 0:
            print("⚠️ No se encontraron puestos con los filtros especificados")
            return BatchProcessingResult(
                total_puestos=0,
                procesados=0,
                exitosos=0,
                fallidos=0,
                resultados=[]
            )

        # Crear directorio de salida
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Procesar cada puesto
        resultados = []

        for i, puesto_data in enumerate(puestos, 1):
            codigo = puesto_data.get('CÓDIGO_DE_PUESTO', 'UNKNOWN')

            print(f"\n[{i}/{len(puestos)}] Procesando: {codigo}")

            try:
                # 1. Convertir a formato APF
                datos_apf = self.adapter.convertir_puesto(codigo)

                if "error" in datos_apf:
                    print(f"  ❌ Error en conversión: {datos_apf['error']}")
                    resultados.append({
                        "codigo": codigo,
                        "status": "error_conversion",
                        "error": datos_apf["error"]
                    })
                    continue

                # 2. Generar documento RHNet virtual
                doc_rhnet = None
                if generar_documentos:
                    doc_rhnet = self.generator.generar_documento(datos_apf)

                    # Guardar documento
                    doc_path = Path(output_dir) / f"{codigo.replace('/', '_')}_rhnet.txt"
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(doc_rhnet)
                    print(f"  📄 Documento guardado: {doc_path.name}")

                # 3. Validar (si está habilitado)
                resultado_validacion = None
                if validar and self.pipeline:
                    # Escribir documento temporal para validación
                    temp_doc = Path(output_dir) / f"temp_{codigo.replace('/', '_')}.txt"
                    with open(temp_doc, 'w', encoding='utf-8') as f:
                        f.write(doc_rhnet)

                    # Ejecutar validación
                    resultado_validacion = self.pipeline.extract_from_file(str(temp_doc))

                    # Limpiar temporal
                    temp_doc.unlink()

                    print(f"  ✅ Validación: {resultado_validacion.get('status', 'unknown')}")

                # Consolidar resultado
                resultados.append({
                    "codigo": codigo,
                    "denominacion": datos_apf.get("identificacion_puesto", {}).get("denominacion_puesto"),
                    "nivel": puesto_data.get('GRADO'),
                    "ur": puesto_data.get('UR'),
                    "status": "success",
                    "datos_apf": datos_apf,
                    "validacion": resultado_validacion
                })

            except Exception as e:
                print(f"  ❌ Error procesando: {str(e)}")
                resultados.append({
                    "codigo": codigo,
                    "status": "error",
                    "error": str(e)
                })

        # Generar resultado consolidado
        return self._consolidar_resultados(resultados, puestos)

    def _consolidar_resultados(self,
                               resultados: List[Dict],
                               puestos_originales: List[Dict]) -> BatchProcessingResult:
        """Consolida resultados de procesamiento en lote"""
        exitosos = sum(1 for r in resultados if r["status"] == "success")
        fallidos = len(resultados) - exitosos

        return BatchProcessingResult(
            total_puestos=len(puestos_originales),
            procesados=len(resultados),
            exitosos=exitosos,
            fallidos=fallidos,
            resultados=resultados,
            filtros_aplicados=[f.get_description() for f in self.filtros]
        )

@dataclass
class BatchProcessingResult:
    """Resultado de procesamiento en lote"""
    total_puestos: int
    procesados: int
    exitosos: int
    fallidos: int
    resultados: List[Dict[str, Any]]
    filtros_aplicados: List[str] = field(default_factory=list)

    def get_summary(self) -> str:
        """Genera resumen textual"""
        return f"""
📊 RESUMEN DE PROCESAMIENTO EN LOTE
{'='*60}
Total de puestos: {self.total_puestos}
Procesados: {self.procesados}
Exitosos: {self.exitosos} ({self.exitosos/self.procesados*100:.1f}%)
Fallidos: {self.fallidos}

Filtros aplicados: {len(self.filtros_aplicados)}
{chr(10).join(f'  - {f}' for f in self.filtros_aplicados)}
"""
```

### 3. Generador de Documentos RHNet

**Principio SOLID**: Single Responsibility - solo genera documentos texto

```python
# adapters/rhnet_document_generator.py
class RHNetDocumentGenerator:
    """
    Genera documentos de texto simulando formato RHNet.
    Toma datos en formato APF y produce texto estructurado.
    """

    def __init__(self, template: str = "default"):
        self.template = template

    def generar_documento(self, datos_apf: Dict[str, Any]) -> str:
        """
        Genera documento RHNet desde datos APF.

        Args:
            datos_apf: Datos en formato APF (output de SidegorAdapter)

        Returns:
            String con documento formateado estilo RHNet
        """
        if self.template == "default":
            return self._generar_formato_default(datos_apf)
        elif self.template == "extended":
            return self._generar_formato_extendido(datos_apf)
        else:
            raise ValueError(f"Template desconocido: {self.template}")

    def _generar_formato_default(self, datos_apf: Dict[str, Any]) -> str:
        """Formato RHNet estándar (compatible con pipeline actual)"""
        ident = datos_apf.get("identificacion_puesto", {})
        obj = datos_apf.get("objetivo_general", {})
        funciones = datos_apf.get("funciones", [])
        escolaridad = datos_apf.get("escolaridad", {})
        experiencia = datos_apf.get("experiencia", {})

        doc = f"""Puesto: {ident.get('codigo_puesto', 'N/A')}
Nombre\t{ident.get('denominacion_puesto', 'N/A')}\tCaracter ocupacional\t{ident.get('caracter_ocupacional', 'N/A')}
Nivel salarial\t{ident.get('nivel_salarial', {}).get('codigo', 'N/A')}\tEstatus\t{ident.get('estatus', 'N/A')}
Ramo\t{ident.get('ramo', 'N/A')}\tUnidad Responsable\t{ident.get('unidad_responsable', 'N/A')}

Objetivo General y Funciones.
Objetivo General
{obj.get('descripcion_completa', 'No disponible')}

"""

        # Agregar funciones
        for i, func in enumerate(funciones, 1):
            doc += f"Función {i}\n"
            doc += f"{func.get('descripcion_completa', 'No disponible')}\n"

        # Agregar perfil
        doc += f"""
Perfil.
Escolaridad
Nivel de Estudios:\t{escolaridad.get('nivel_estudios', 'NO APLICA')}
Grado de Avance:\t{escolaridad.get('grado_avance', 'NO APLICA')}
Área General:\t{escolaridad.get('area_general', 'NO APLICA')}
Carrera Genérica:\t{escolaridad.get('carrera_generica', 'NO APLICA')}

Experiencia Laboral
Años requeridos:\t{experiencia.get('anos_experiencia', 'NO APLICA')}
Área de Experiencia:\t{experiencia.get('area_experiencia', 'NO APLICA')}
"""

        return doc

    def _generar_formato_extendido(self, datos_apf: Dict[str, Any]) -> str:
        """Formato extendido con información adicional"""
        doc_base = self._generar_formato_default(datos_apf)

        # Agregar información adicional si existe
        info_adicional = datos_apf.get("informacion_adicional", {})

        if info_adicional:
            doc_base += "\n\nInformación Adicional.\n"

            # Competencias
            competencias = datos_apf.get("competencias", [])
            if competencias:
                doc_base += "\nCompetencias:\n"
                for comp in competencias:
                    doc_base += f"  - {comp.get('competencia', 'N/A')}: {comp.get('nivel_requerido', 'N/A')}\n"

            # Condiciones de trabajo
            if "condiciones_trabajo" in info_adicional:
                cond = info_adicional["condiciones_trabajo"]
                doc_base += f"\nCondiciones de Trabajo:\n"
                doc_base += f"  Horario: {cond.get('horario', 'N/A')}\n"
                doc_base += f"  Disponibilidad para viajar: {cond.get('disponibilidad_viajar', 'N/A')}\n"

        return doc_base
```

---

## 🔧 API de Uso

### Caso de Uso 1: Procesar SABG niveles G-K

```python
from src.adapters import SidegorAdapter, SidegorBatchProcessor, RHNetDocumentGenerator
from src.filters import NivelSalarialFilter, URFilter, CompositeFilter
from src.pipeline import PipelineFactory

# 1. Cargar archivo Excel
adapter = SidegorAdapter()
adapter.cargar_archivo("validación comparativa con otras URs/Reporte_DPP_27_SABG.xlsx")

# 2. Crear generador de documentos
generator = RHNetDocumentGenerator(template="default")

# 3. Crear pipeline de validación (opcional)
validation_pipeline = PipelineFactory.create_simple_pipeline(
    model="openai/gpt-4o"
)

# 4. Crear procesador en lote
processor = SidegorBatchProcessor(
    adapter=adapter,
    document_generator=generator,
    validation_pipeline=validation_pipeline
)

# 5. Configurar filtros
filtro_niveles = NivelSalarialFilter(niveles=["G", "H", "I", "J", "K"])
filtro_ur = URFilter(ur_codes=["27"])

processor.add_filter(filtro_niveles)
processor.add_filter(filtro_ur)

# 6. Procesar lote
resultado = processor.procesar_lote(
    validar=True,
    generar_documentos=True,
    output_dir="output/sabg_niveles_g_k"
)

# 7. Ver resultados
print(resultado.get_summary())

# 8. Exportar reporte
resultado.exportar_json("output/sabg_niveles_g_k/reporte_consolidado.json")
```

### Caso de Uso 2: Comparar múltiples URs

```python
from src.adapters import MultiURProcessor

# Procesar múltiples archivos
processor = MultiURProcessor()

archivos = [
    ("SABG", "Reporte_DPP_27_SABG.xlsx"),
    ("HACIENDA", "Reporte_DPP_06_HACIENDA.xlsx"),
    ("TURISMO", "Reporte_DPP_21_TURISMO.xlsx")
]

# Filtros comunes
filtro_niveles = NivelSalarialFilter(niveles=["K", "L", "M"])

resultados = processor.procesar_multiples_urs(
    archivos=archivos,
    filtros=[filtro_niveles],
    validar=True
)

# Generar comparación
comparacion = processor.generar_comparacion(resultados)
comparacion.exportar_excel("output/comparacion_urs.xlsx")
```

---

## 📊 Reportes y Métricas

### Métricas por Lote

```python
{
    "resumen": {
        "total_puestos": 150,
        "procesados": 150,
        "exitosos": 142,
        "fallidos": 8,
        "tasa_exito": 94.7
    },
    "por_nivel": {
        "G": {"total": 30, "exitosos": 28},
        "H": {"total": 40, "exitosos": 39},
        "I": {"total": 35, "exitosos": 34},
        "J": {"total": 25, "exitosos": 23},
        "K": {"total": 20, "exitosos": 18}
    },
    "validacion": {
        "aligned": 85,
        "partially_aligned": 42,
        "not_aligned": 15
    },
    "tiempos": {
        "total_segundos": 450,
        "promedio_por_puesto": 3.0
    }
}
```

### Reporte Consolidado Excel

Hojas generadas:
1. **Resumen**: Estadísticas globales
2. **Detalle**: Fila por cada puesto con status
3. **Errores**: Puestos fallidos con detalles
4. **Validación**: Resultados de validación contextual
5. **Comparación**: (si múltiples URs) Comparativa

---

## 🚀 Plan de Implementación

### Fase 1: Core (2-3 horas)
1. ✅ Diseño completo (este documento)
2. Implementar sistema de filtros (`filters/`)
3. Implementar `SidegorBatchProcessor`
4. Implementar `RHNetDocumentGenerator`

### Fase 2: Validación (1-2 horas)
5. Integrar con `APFExtractor` existente
6. Crear `BatchValidationPipeline`
7. Implementar agregación de resultados

### Fase 3: Reportes (1 hora)
8. Implementar `BatchReporter`
9. Implementar exportación a Excel
10. Crear visualizaciones de métricas

### Fase 4: Testing (1 hora)
11. Probar con SABG niveles G-K
12. Probar con múltiples URs
13. Validar reportes generados

**Tiempo total estimado**: 5-7 horas

---

## 🎯 Siguientes Pasos Inmediatos

1. **Revisar y aprobar diseño**
2. **Implementar Fase 1**: Sistema de filtros + BatchProcessor
3. **Probar con datos reales**: TURISMO (archivo pequeño)
4. **Iterar según resultados**

---

**Documento creado**: 2025-11-03
**Autor**: Sistema APF v5.0
**Status**: Propuesta de diseño - Pendiente de aprobación
