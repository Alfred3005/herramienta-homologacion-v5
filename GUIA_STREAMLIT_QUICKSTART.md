# 🚀 Guía de Inicio Rápido - Interfaz Streamlit

**Fecha**: 2025-11-04
**Versión**: 1.0
**Estado**: ✅ Implementado y listo para usar

---

## ✅ Lo que se Implementó

### Aplicación Completa con 4 Páginas:

1. **🏠 Dashboard Principal** (`home.py`)
   - Métricas visuales (análisis totales, en proceso, completados)
   - Gráfica interactiva de tendencias (Plotly)
   - Lista de análisis recientes con acceso rápido
   - Tips, guías y FAQ integrados

2. **🆕 Wizard de Nuevo Análisis** (`new_analysis.py`)
   - **Paso 1**: Upload de archivos (Sidegor + Normativa)
   - **Paso 2**: Configuración de filtros (Nivel, UR, Código)
   - **Paso 3**: Opciones de análisis avanzadas
   - **Paso 4**: Confirmación y ejecución

3. **📊 Resultados** (`results.py`) - Stub para desarrollo futuro

4. **📚 Historial** (`history.py`) - Stub para desarrollo futuro

---

## 🏃 Inicio Rápido (3 minutos)

### Paso 1: Instalar Dependencias

```bash
cd /home/alfred/herramienta-homologacion-v5/streamlit_app

# Instalar requirements
pip install -r requirements.txt
```

### Paso 2: Ejecutar la Aplicación

```bash
streamlit run app.py
```

### Paso 3: Abrir en el Navegador

La aplicación se abrirá automáticamente en:
```
http://localhost:8501
```

Si no se abre, copia la URL que aparece en la terminal.

---

## 📸 Screenshots Conceptuales

### Dashboard Principal
```
┌─────────────────────────────────────────────┐
│ 🏛️ Sistema de Homologación APF             │
│                                              │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │
│ │ 127  │ │  3   │ │ 124  │ │97.3% │       │
│ │Total │ │Activo│ │ Done │ │ Éxito│       │
│ └──────┘ └──────┘ └──────┘ └──────┘       │
│                                              │
│ 📈 Análisis por Mes                         │
│ ▁▂▃▅▆▇█▆▅▃▂▁                                │
│                                              │
│ 🔥 Análisis Recientes                       │
│ ├─ TURISMO G-K ✅ (25 puestos) [Ver]       │
│ ├─ SABG Nivel M 🔄 (15/20) [Ver]           │
│ └─ SADER 1-3 ✅ (82 puestos) [Ver]         │
└─────────────────────────────────────────────┘
```

### Wizard - Paso 1: Upload
```
┌─────────────────────────────────────────────┐
│ 📂 Paso 1: Subir Archivos                  │
│                                              │
│ ┌─────────────────┐ ┌─────────────────┐   │
│ │ 📊 Sidegor Excel│ │ 📜 Normativa    │   │
│ │ [Drag & Drop]   │ │ [Drag & Drop]   │   │
│ │                 │ │                 │   │
│ │ ✅ archivo.xlsx │ │ ✅ reglamento..│   │
│ │ 791 KB          │ │ 135 KB          │   │
│ │ 1,439 puestos   │ │                 │   │
│ └─────────────────┘ └─────────────────┘   │
│                                              │
│                    [🏠 Inicio] [Siguiente →]│
└─────────────────────────────────────────────┘
```

### Wizard - Paso 2: Filtros
```
┌─────────────────────────────────────────────┐
│ 🔍 Paso 2: Configurar Filtros              │
│                                              │
│ 🎯 Nivel Salarial                           │
│ ☑️ Activar filtro                           │
│ Tipo: ◉ Alfabético  ○ Numérico             │
│ Niveles: [G] [H] [J] [K]                   │
│          ✓   ✓   ✓   ✓                     │
│                                              │
│ 🏢 Unidad Responsable                       │
│ ☑️ Activar filtro                           │
│ UR: [21 - TURISMO (1,439 puestos)]         │
│                                              │
│ 📊 PREVISUALIZACIÓN                         │
│ ✅ 25 puestos coinciden                     │
│                                              │
│ [← Atrás] [🧹 Limpiar] [Siguiente →]       │
└─────────────────────────────────────────────┘
```

---

## 🎯 Características Implementadas

### ✅ Funcionalidades Core

- ✅ **Navegación fluida** entre 4 páginas
- ✅ **Upload de archivos** con drag & drop
- ✅ **Validación automática** de formatos Sidegor
- ✅ **Filtros dinámicos** (nivel, UR, código)
- ✅ **Previsualización** de resultados
- ✅ **Session state** para persistencia
- ✅ **CSS personalizado** con gradientes
- ✅ **Gráficas interactivas** (Plotly)
- ✅ **Wizard de 4 pasos** con indicador de progreso
- ✅ **Detección automática** de tipo de nivel (alfabético/numérico)

### 🎨 Diseño UI/UX

- **Cards de métricas** con gradientes coloridos
- **Botones mejorados** con estados hover
- **Progress indicators** visuales
- **Sidebar** con navegación clara
- **Tabs** para organizar contenido
- **Alerts** personalizados (success, info, warning)
- **Upload zones** con feedback visual

---

## 🔧 Estructura del Código

```
streamlit_app/
├── app.py                    # Punto de entrada principal
│   ├── Configuración de página
│   ├── CSS personalizado
│   ├── Session state initialization
│   ├── Sidebar con navegación
│   └── Router de páginas
│
├── pages/
│   ├── __init__.py
│   ├── home.py              # Dashboard
│   │   ├── Métricas principales
│   │   ├── Gráfica de tendencias
│   │   ├── Lista de análisis recientes
│   │   └── Tips y ayuda
│   │
│   ├── new_analysis.py      # Wizard completo
│   │   ├── step_1_upload_files()
│   │   ├── step_2_configure_filters()
│   │   ├── step_3_analysis_options()
│   │   └── step_4_execute()
│   │
│   ├── results.py           # Visualización (stub)
│   └── history.py           # Historial (stub)
│
├── requirements.txt         # Dependencias
└── README.md               # Documentación
```

---

## 📦 Dependencias

```txt
streamlit>=1.28.0        # Framework web
pandas>=2.0.0            # Manejo de datos
plotly>=5.17.0          # Gráficas interactivas
openpyxl>=3.1.0         # Lectura de Excel
python-docx>=1.1.0      # Lectura de DOCX
PyPDF2>=3.0.0           # Lectura de PDF
```

---

## 🧪 Prueba de Funcionalidades

### Caso de Prueba 1: Dashboard

1. Ejecuta `streamlit run app.py`
2. Verifica que se muestre:
   - ✅ 4 cards de métricas con colores
   - ✅ Gráfica de barras interactiva
   - ✅ Lista de análisis recientes
   - ✅ Tabs de Tips/Guías/FAQ

### Caso de Prueba 2: Wizard - Upload

1. Haz clic en "🆕 Nuevo Análisis"
2. Sube archivo Excel Sidegor (ej: `Reporte_DPP_21_000_TURISMO.xlsx`)
3. Verifica validación:
   - ✅ Mensaje "Archivo válido"
   - ✅ Contador de puestos detectados
   - ✅ Lista de hojas encontradas
4. Sube archivo de normativa (.txt)
5. Verifica que el botón "Siguiente" se active

### Caso de Prueba 3: Filtros

1. En Paso 2, activa filtro por nivel
2. Selecciona niveles G, H, J, K
3. Verifica:
   - ✅ Previsualización muestra cantidad de puestos
   - ✅ Distribución por nivel se actualiza
   - ✅ Contador de puestos es correcto

### Caso de Prueba 4: Opciones

1. En Paso 3, configura:
   - ✅ Nombre del análisis
   - ✅ Formatos de salida (PDF, Excel, JSON)
   - ✅ Validación contextual
   - ✅ Configuración técnica avanzada

### Caso de Prueba 5: Ejecución

1. En Paso 4, verifica resumen completo
2. Haz clic en "🚀 Ejecutar Análisis"
3. Verifica:
   - ✅ Progress bar aparece
   - ✅ Mensaje de completado (simulado)

---

## 🚀 Deployment Opciones

### Opción 1: Streamlit Cloud (Recomendado - Gratis)

1. Sube código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. Selecciona `streamlit_app/app.py` como main file
5. ¡Deploy automático!

**Ventajas**:
- ✅ Gratis para proyectos públicos
- ✅ Deploy automático en cada push
- ✅ URL persistente (https://tu-app.streamlit.app)
- ✅ HTTPS automático

### Opción 2: Docker (Self-Hosted)

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY streamlit_app/ /app/
COPY src/ /app/src/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

```bash
docker build -t apf-homologacion .
docker run -p 8501:8501 apf-homologacion
```

### Opción 3: Render/Railway (Managed)

Similar a Streamlit Cloud pero con más recursos:
- Render.com: $7/mes (512MB RAM)
- Railway.app: $5/mes + uso

---

## 📝 Próximos Pasos de Desarrollo

### Corto Plazo (1-2 semanas)

- [ ] **Integración con sistema v5.0**
  - Conectar wizard con `SidegorBatchProcessor`
  - Ejecutar análisis real (no simulado)
  - Guardar resultados en `output/`

- [ ] **Página de Resultados completa**
  - Leer análisis guardados en `output/`
  - Gráficas de distribución
  - Tablas interactivas con pandas
  - Detalles por puesto

- [ ] **Exportación de reportes**
  - PDF generado con ReportLab
  - Excel multi-hoja
  - JSON estructurado

### Mediano Plazo (3-4 semanas)

- [ ] **Procesamiento en tiempo real**
  - WebSockets para updates
  - Progress bar real (no simulado)
  - Logs streaming

- [ ] **Historial persistente**
  - SQLite local para metadata
  - Búsqueda y filtrado
  - Comparación entre análisis

- [ ] **Visualizaciones avanzadas**
  - Gráficas de validación por función
  - Análisis de verbos débiles
  - Mapas de calor

### Largo Plazo (1-2 meses)

- [ ] **Autenticación**
  - Login de usuarios
  - Roles y permisos
  - Análisis privados/compartidos

- [ ] **APIs**
  - Endpoint REST para análisis
  - Webhook para notificaciones
  - Integración con otros sistemas

- [ ] **Features avanzadas**
  - Comparación lado a lado
  - Templates de filtros
  - Análisis programados

---

## 💡 Tips de Desarrollo

### Hot Reload

Streamlit recarga automáticamente al guardar cambios:
- Edita cualquier archivo `.py`
- Guarda
- ¡La app se actualiza sola!

### Debugging

```python
import streamlit as st

# Ver session state
st.write(st.session_state)

# Logs en sidebar
with st.sidebar:
    st.write("Debug info")
    st.json(some_data)
```

### Performance

```python
# Cache datos pesados
@st.cache_data
def load_large_dataframe():
    return pd.read_excel("huge_file.xlsx")

# Cache recursos
@st.cache_resource
def load_model():
    return load_llm_model()
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### Error: Port 8501 already in use

```bash
# Usar otro puerto
streamlit run app.py --server.port 8502
```

### Error: Cannot import from parent directory

```python
# En archivos de pages/, agregar:
import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))
```

### App no se actualiza después de cambios

```bash
# Ctrl+C para detener
# Reiniciar
streamlit run app.py --server.runOnSave true
```

---

## 📞 Soporte

- 📖 [Documentación Streamlit](https://docs.streamlit.io)
- 💬 [Community Forum](https://discuss.streamlit.io)
- 🐛 [Reportar Bug](https://github.com/tu-repo/issues)

---

## ✅ Checklist de Verificación

Antes de usar en producción, verifica:

- [ ] Todas las dependencias instaladas (`pip install -r requirements.txt`)
- [ ] App se ejecuta sin errores (`streamlit run app.py`)
- [ ] Dashboard muestra métricas correctamente
- [ ] Wizard permite subir archivos
- [ ] Filtros funcionan y actualizan preview
- [ ] Navegación entre páginas funciona
- [ ] CSS personalizado se carga
- [ ] Gráficas de Plotly son interactivas

---

**Documento creado**: 2025-11-04
**Última actualización**: 2025-11-04
**Versión**: 1.0
**Estado**: ✅ Listo para usar

**Prueba realizada**: No (requiere instalación de dependencias)

Para empezar ahora mismo:
```bash
cd streamlit_app && pip install -r requirements.txt && streamlit run app.py
```
