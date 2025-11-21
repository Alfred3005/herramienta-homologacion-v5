# 📄 Sistema de Reportes RH Net

## Descripción

Sistema de generación de reportes de puestos en formato RH Net para control y auditoría. Permite descargar la descripción del puesto en múltiples formatos para contrastar la información de entrada contra los resultados del análisis.

## Características

- ✅ Generación de reportes completos en formato RH Net
- ✅ Exportación a múltiples formatos: TXT, HTML, PDF, DOCX
- ✅ Integrado en página de resultados (Streamlit)
- ✅ Vista previa del reporte antes de descargar
- ✅ Manejo graceful de dependencias opcionales

## Formatos Soportados

### 📝 TXT (Texto Plano)
- **Dependencias:** Ninguna (nativo)
- **Uso:** Control de versiones, auditoría básica
- **Características:** UTF-8, header con metadata

### 🌐 HTML (Página Web)
- **Dependencias:** Ninguna (nativo)
- **Uso:** Visualización en navegador, compartir
- **Características:** Estilos CSS, responsive, colores

### 📕 PDF (Portable Document Format)
- **Dependencias:** `fpdf2`
- **Uso:** Documentación oficial, presentaciones
- **Características:** Formato profesional, headers coloreados
- **Instalación:** `pip install fpdf2`

### 📘 DOCX (Microsoft Word)
- **Dependencias:** `python-docx`
- **Uso:** Edición posterior, integración Office
- **Características:** Estilos, headings, formato completo
- **Instalación:** `pip install python-docx`

## Instalación de Dependencias Opcionales

Para habilitar todos los formatos de exportación:

```bash
# Instalar todas las dependencias opcionales
pip install fpdf2 python-docx

# O solo las que necesites
pip install fpdf2          # Para PDF
pip install python-docx    # Para DOCX
```

## Uso en Streamlit

1. Ejecuta un análisis desde "Nuevo Análisis"
2. Ve a la página "Resultados"
3. Selecciona un análisis de la lista
4. En "Explorar Puesto Individual", selecciona el puesto
5. Busca la sección "📄 Descargar Reporte RHNet"
6. Haz clic en el formato deseado: TXT, HTML, PDF, o DOCX
7. (Opcional) Usa "Vista Previa" para ver el reporte antes de descargar

## Estructura del Reporte

El reporte RH Net incluye las siguientes secciones:

### 1. Encabezado del Puesto
- Código del puesto
- Nombre/Denominación
- Carácter ocupacional
- Nivel salarial
- Persona en el puesto
- Puestos dependientes

### 2. Dirección (si está disponible)
- Edificio, calle, colonia
- País, estado, municipio
- Código postal
- Email y teléfono

### 3. Objetivo General y Funciones
- Objetivo general del puesto
- Lista numerada de funciones

### 4. Perfil
- **Entorno Operativo:** Tipo de relación, explicación
- **Escolaridad:** Nivel, grado, área, carrera
- **Experiencia Laboral:** Años requeridos, áreas
- **Condiciones de Trabajo:** Horario, viajes, etc.
- **Capacidades Profesionales:** Competencias requeridas
- **Observaciones:** Notas generales y de especialista

## Uso Programático

### Generar Reporte

```python
from src.adapters.rhnet_report_generator import RHNetReportGenerator

# Preparar datos del puesto
datos_puesto = {
    "identificacion_puesto": {
        "codigo_puesto": "27-100-1-M1C035P-0000661-E-X-V",
        "denominacion_puesto": "SECRETARIA(O) ANTICORRUPCION Y BUEN GOBIERNO",
        "nivel_salarial": {"codigo": "G11", "descripcion": "Secretario de Estado"},
        # ... más campos
    },
    "objetivo_general": {"descripcion_completa": "..."},
    "funciones": [{"descripcion_completa": "..."}, ...],
    # ... más secciones
}

# Generar reporte
generador = RHNetReportGenerator()
reporte_texto = generador.generar_reporte_completo(datos_puesto)
print(reporte_texto)
```

### Exportar a Formato Específico

```python
from src.adapters.report_exporters import exportar_reporte

# Metadata opcional
metadata = {
    "codigo_puesto": "27-100-1-M1C035P-0000661-E-X-V",
    "fecha_generacion": "2025-11-20 10:30:00"
}

# Exportar a PDF
pdf_bytes = exportar_reporte(reporte_texto, 'pdf', metadata)
with open('reporte.pdf', 'wb') as f:
    f.write(pdf_bytes)

# Exportar a DOCX
docx_bytes = exportar_reporte(reporte_texto, 'docx', metadata)
with open('reporte.docx', 'wb') as f:
    f.write(docx_bytes)

# Exportar a HTML
html_bytes = exportar_reporte(reporte_texto, 'html', metadata)
with open('reporte.html', 'wb') as f:
    f.write(html_bytes)

# Exportar a TXT
txt_bytes = exportar_reporte(reporte_texto, 'txt', metadata)
with open('reporte.txt', 'wb') as f:
    f.write(txt_bytes)
```

### Factory Pattern

```python
from src.adapters.report_exporters import ReportExporterFactory

# Obtener exportador específico
exporter = ReportExporterFactory.get_exporter('pdf')
pdf_bytes = exporter.exportar(reporte_texto, metadata)

# Ver formatos disponibles
formatos = ReportExporterFactory.formatos_disponibles()
print(formatos)  # ['txt', 'html', 'pdf', 'docx']
```

## Arquitectura

### Módulos Principales

1. **`rhnet_report_generator.py`**
   - Clase: `RHNetReportGenerator`
   - Responsabilidad: Generar reporte en formato texto
   - Métodos: `generar_reporte_completo()`, `generar_reporte_desde_excel()`

2. **`report_exporters.py`**
   - Clases: `TXTExporter`, `HTMLExporter`, `PDFExporter`, `DOCXExporter`
   - Patrón: Factory + Strategy
   - Responsabilidad: Exportar reportes a diferentes formatos

3. **`results.py` (Streamlit)**
   - Integración en UI
   - Botones de descarga
   - Vista previa

### Flujo de Datos

```
Datos Puesto (JSON)
    ↓
RHNetReportGenerator
    ↓
Reporte Texto (String)
    ↓
ReportExporter (Factory)
    ↓
Bytes (TXT/HTML/PDF/DOCX)
    ↓
Download Button (Streamlit)
```

## Manejo de Errores

### Dependencias Faltantes

Si `fpdf2` o `python-docx` no están instaladas, los botones correspondientes se mostrarán deshabilitados con un tooltip indicando cómo instalar la dependencia.

### Datos Incompletos

El generador maneja gracefully datos faltantes usando valores por defecto:
- "N/A" para campos de identificación
- "No disponible" para descripciones
- "NO APLICA" para campos de perfil
- Listas vacías para funciones/competencias

### Excepciones

```python
try:
    reporte = generador.generar_reporte_completo(datos)
    pdf_bytes = exportar_reporte(reporte, 'pdf')
except ImportError as e:
    print(f"Dependencia faltante: {e}")
except Exception as e:
    print(f"Error generando reporte: {e}")
```

## Caso de Uso: Control y Auditoría

1. **Problema:** Necesidad de contrastar información original del puesto vs resultados del análisis
2. **Solución:** Generar reporte RH Net con datos de entrada
3. **Beneficio:** Documento oficial para auditorías, control de cambios, y revisión

### Workflow de Auditoría

```
1. Cargar Excel con puestos → 2. Ejecutar análisis → 3. Revisar resultados
                                                              ↓
                                                    4. Descargar reporte RHNet
                                                              ↓
                                            5. Contrastar entrada vs análisis
                                                              ↓
                                            6. Documentar hallazgos y decisiones
```

## Mejoras Futuras

- [ ] Exportación a Excel con formato
- [ ] Generación de reportes por lote (múltiples puestos)
- [ ] Templates personalizables
- [ ] Integración con sistema de versiones
- [ ] Firma digital de reportes
- [ ] Comparación lado a lado (entrada vs análisis)

## Referencias

- Formato RH Net oficial
- Sistema de Homologación APF v5.41
- Documentación Streamlit: https://docs.streamlit.io

---

**Versión:** 1.0
**Fecha:** 2025-11-20
**Autor:** Sistema de Homologación APF
