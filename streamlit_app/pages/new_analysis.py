"""
Página de Nuevo Análisis - Wizard de 4 Pasos
Permite configurar y ejecutar análisis de puestos
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import time
import json
from datetime import datetime

# Agregar path al sistema
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

def show():
    """Renderiza la página de nuevo análisis"""

    st.title("🆕 Nuevo Análisis")
    st.markdown("### Wizard de Configuración - 4 Pasos")

    # Inicializar estado si no existe
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1

    if 'uploaded_sidegor' not in st.session_state:
        st.session_state.uploaded_sidegor = None

    if 'uploaded_normativa' not in st.session_state:
        st.session_state.uploaded_normativa = None

    if 'filters_config' not in st.session_state:
        st.session_state.filters_config = {}

    if 'analysis_options' not in st.session_state:
        st.session_state.analysis_options = {
            'generate_pdf': True,
            'generate_excel': True,
            'save_json': True,
            'contextual_validation': False,
        }

    # Mostrar indicador de progreso
    steps = ["📂 Archivos", "🔍 Filtros", "⚙️ Opciones", "🚀 Ejecutar"]
    current_step = st.session_state.wizard_step

    cols = st.columns(4)
    for idx, (col, step_name) in enumerate(zip(cols, steps), 1):
        with col:
            if idx < current_step:
                st.success(f"✅ {step_name}")
            elif idx == current_step:
                st.info(f"▶️ {step_name}")
            else:
                st.markdown(f"⚪ {step_name}")

    st.markdown("---")

    # Renderizar paso correspondiente
    if current_step == 1:
        step_1_upload_files()
    elif current_step == 2:
        step_2_configure_filters()
    elif current_step == 3:
        step_3_analysis_options()
    elif current_step == 4:
        step_4_execute()


def step_1_upload_files():
    """Paso 1: Subir archivos necesarios"""

    st.subheader("📂 Paso 1: Subir Archivos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Base de Datos Sidegor (Requerido)")
        st.markdown("Formato: archivo Excel (.xlsx)")

        uploaded_sidegor = st.file_uploader(
            "Subir archivo Excel Sidegor",
            type=['xlsx'],
            key='sidegor_uploader',
            help="Archivo Excel con formato Sidegor (11 hojas: PUESTOS, OBJ_FUNCIONES, etc.)"
        )

        if uploaded_sidegor is not None:
            st.session_state.uploaded_sidegor = uploaded_sidegor

            # Validar archivo
            with st.spinner("Validando archivo..."):
                try:
                    # Leer hojas del Excel
                    excel_file = pd.ExcelFile(uploaded_sidegor)
                    sheets = excel_file.sheet_names

                    # Verificar hojas requeridas
                    required_sheets = ['PUESTOS', 'OBJ_FUNCIONES']
                    has_required = all(sheet in sheets for sheet in required_sheets)

                    if has_required:
                        # Contar puestos
                        df_puestos = pd.read_excel(uploaded_sidegor, sheet_name='PUESTOS')
                        num_puestos = len(df_puestos)

                        st.success(f"✅ Archivo válido")
                        st.info(f"""
                        **Información del archivo:**
                        - 📦 Tamaño: {uploaded_sidegor.size / 1024:.1f} KB
                        - 📋 Puestos detectados: **{num_puestos}**
                        - 📄 Hojas encontradas: {len(sheets)}
                        """)

                        # Guardar info en session state
                        st.session_state.sidegor_info = {
                            'num_puestos': num_puestos,
                            'sheets': sheets,
                            'df_puestos': df_puestos
                        }
                    else:
                        st.error(f"❌ Formato inválido. Faltan hojas requeridas: {', '.join(required_sheets)}")

                except Exception as e:
                    st.error(f"❌ Error al leer archivo: {str(e)}")

    with col2:
        st.markdown("#### 📜 Normativa / Reglamento (Requerido)")
        st.markdown("Formatos: .txt, .pdf, .docx")

        uploaded_normativa = st.file_uploader(
            "Subir normativa o reglamento",
            type=['txt', 'pdf', 'docx'],
            key='normativa_uploader',
            help="Documento normativo contra el cual se validarán los puestos"
        )

        if uploaded_normativa is not None:
            st.session_state.uploaded_normativa = uploaded_normativa

            st.success(f"✅ Archivo cargado")
            st.info(f"""
            **Información del archivo:**
            - 📦 Tamaño: {uploaded_normativa.size / 1024:.1f} KB
            - 📄 Tipo: {uploaded_normativa.type}
            - 📝 Nombre: {uploaded_normativa.name}
            """)

            # Si es TXT, mostrar preview
            if uploaded_normativa.name.endswith('.txt'):
                content = uploaded_normativa.getvalue().decode('utf-8')
                with st.expander("👁️ Preview del contenido"):
                    st.text(content[:500] + "..." if len(content) > 500 else content)

    st.markdown("---")

    # Botones de navegación
    col_left, col_right = st.columns([1, 1])

    with col_left:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    with col_right:
        can_proceed = (st.session_state.uploaded_sidegor is not None and
                       st.session_state.uploaded_normativa is not None)

        if st.button("Siguiente →", use_container_width=True,
                     type="primary", disabled=not can_proceed):
            st.session_state.wizard_step = 2
            st.rerun()

    if not can_proceed:
        st.warning("⚠️ Por favor sube ambos archivos para continuar")


def step_2_configure_filters():
    """Paso 2: Configurar filtros de selección"""

    st.subheader("🔍 Paso 2: Configurar Filtros")

    if 'sidegor_info' not in st.session_state:
        st.error("❌ No se ha cargado información del archivo Sidegor")
        return

    df_puestos = st.session_state.sidegor_info['df_puestos']

    # Filtro por Nivel Salarial
    st.markdown("### 🎯 Filtro por Nivel Salarial")

    enable_nivel_filter = st.checkbox("✓ Activar filtro por nivel salarial", value=True)

    if enable_nivel_filter:
        # Detectar tipo de niveles (alfabético o numérico)
        if 'GRUPO' in df_puestos.columns:
            grupos_unicos = df_puestos['GRUPO'].dropna().unique()
            tiene_alfabeticos = any(str(g).isalpha() for g in grupos_unicos)

            if tiene_alfabeticos:
                st.info("📊 Niveles detectados: **Alfabéticos** (G, H, I, J, K, M, N, O, P)")

                niveles_disponibles = sorted([str(g) for g in grupos_unicos if pd.notna(g)])

                selected_niveles = st.multiselect(
                    "Seleccionar niveles:",
                    options=niveles_disponibles,
                    default=[],
                    help="Puedes seleccionar múltiples niveles"
                )

                st.session_state.filters_config['niveles'] = selected_niveles
                st.session_state.filters_config['tipo_nivel'] = 'alfabetico'

        if 'GRADO' in df_puestos.columns and not tiene_alfabeticos:
            grados_unicos = sorted(df_puestos['GRADO'].dropna().unique())
            st.info("📊 Niveles detectados: **Numéricos** (1, 2, 3, ...)")

            selected_grados = st.multiselect(
                "Seleccionar grados:",
                options=[int(g) if not pd.isna(g) else g for g in grados_unicos],
                default=[],
            )

            st.session_state.filters_config['niveles'] = [str(g) for g in selected_grados]
            st.session_state.filters_config['tipo_nivel'] = 'numerico'

    else:
        st.session_state.filters_config['niveles'] = []

    st.markdown("---")

    # Filtro por UR
    st.markdown("### 🏢 Filtro por Unidad Responsable (UR)")

    enable_ur_filter = st.checkbox("✓ Activar filtro por UR", value=False)

    if enable_ur_filter:
        if 'UR' in df_puestos.columns:
            urs_disponibles = sorted(df_puestos['UR'].dropna().unique())

            # Contar puestos por UR
            ur_counts = df_puestos['UR'].value_counts()

            ur_options = [f"{ur} ({ur_counts[ur]} puestos)" for ur in urs_disponibles]

            selected_ur_with_count = st.selectbox(
                "Seleccionar UR:",
                options=ur_options,
                help="Unidad Responsable a filtrar"
            )

            # Extraer solo el código de UR
            selected_ur = selected_ur_with_count.split(' ')[0] if selected_ur_with_count else None

            st.session_state.filters_config['ur'] = selected_ur
        else:
            st.warning("⚠️ Columna 'UR' no encontrada en el archivo")
    else:
        st.session_state.filters_config['ur'] = None

    st.markdown("---")

    # Filtro por Código de Puesto
    st.markdown("### 🔢 Filtro por Código de Puesto (Opcional)")

    enable_codigo_filter = st.checkbox("✓ Activar filtro por código", value=False)

    if enable_codigo_filter:
        codigo_pattern = st.text_input(
            "Patrón de código:",
            placeholder="Ej: 21-410-*, 21-*-1-*, *-E-L-C",
            help="Usa * como wildcard para cualquier secuencia"
        )

        st.session_state.filters_config['codigo_pattern'] = codigo_pattern if codigo_pattern else None
    else:
        st.session_state.filters_config['codigo_pattern'] = None

    st.markdown("---")

    # Previsualización de resultados
    st.markdown("### 📊 Previsualización de Filtros")

    # Aplicar filtros para previsualizar
    filtered_df = df_puestos.copy()

    if enable_nivel_filter and st.session_state.filters_config.get('niveles'):
        if st.session_state.filters_config['tipo_nivel'] == 'alfabetico':
            filtered_df = filtered_df[filtered_df['GRUPO'].isin(st.session_state.filters_config['niveles'])]
        else:
            niveles_int = [int(float(n)) for n in st.session_state.filters_config['niveles']]
            filtered_df = filtered_df[filtered_df['GRADO'].isin(niveles_int)]

    if enable_ur_filter and st.session_state.filters_config.get('ur'):
        filtered_df = filtered_df[filtered_df['UR'] == int(st.session_state.filters_config['ur'])]

    num_filtered = len(filtered_df)

    if num_filtered > 0:
        st.success(f"✅ **{num_filtered} puestos** coinciden con los filtros aplicados")

        # Distribución por nivel
        if enable_nivel_filter and st.session_state.filters_config.get('niveles'):
            st.markdown("**Distribución por nivel:**")

            if st.session_state.filters_config['tipo_nivel'] == 'alfabetico':
                nivel_counts = filtered_df['GRUPO'].value_counts()
            else:
                nivel_counts = filtered_df['GRADO'].value_counts()

            for nivel, count in nivel_counts.items():
                st.markdown(f"- {nivel}: {count} puestos")

    else:
        st.error("❌ No se encontraron puestos con los filtros aplicados")

    st.session_state.filters_config['num_puestos_filtrados'] = num_filtered

    st.markdown("---")

    # Navegación
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.wizard_step = 1
            st.rerun()

    with col2:
        if st.button("🧹 Limpiar Filtros", use_container_width=True):
            st.session_state.filters_config = {}
            st.rerun()

    with col3:
        can_proceed = num_filtered > 0

        if st.button("Siguiente →", use_container_width=True,
                     type="primary", disabled=not can_proceed):
            st.session_state.wizard_step = 3
            st.rerun()

    if not can_proceed:
        st.warning("⚠️ Los filtros deben resultar en al menos 1 puesto")


def step_3_analysis_options():
    """Paso 3: Configurar opciones de análisis"""

    st.subheader("⚙️ Paso 3: Opciones de Análisis")

    # Nombre del análisis
    st.markdown("### 📝 Identificación del Análisis")

    default_name = f"Analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    analysis_name = st.text_input(
        "Nombre del análisis:",
        value=default_name,
        help="Identifica este análisis para encontrarlo después"
    )

    st.session_state.analysis_options['name'] = analysis_name

    st.markdown("---")

    # Opciones de salida
    st.markdown("### 📊 Opciones de Salida")

    col1, col2 = st.columns(2)

    with col1:
        generate_pdf = st.checkbox("📥 Generar reporte PDF", value=True)
        generate_excel = st.checkbox("📥 Generar reporte Excel", value=True)

    with col2:
        save_json = st.checkbox("📥 Guardar JSONs individuales", value=True)
        generate_charts = st.checkbox("📥 Generar gráficas PNG", value=False)

    st.session_state.analysis_options.update({
        'generate_pdf': generate_pdf,
        'generate_excel': generate_excel,
        'save_json': save_json,
        'generate_charts': generate_charts,
    })

    st.markdown("---")

    # Análisis avanzado
    st.markdown("### 🧠 Análisis Avanzado")

    contextual_validation = st.checkbox(
        "🔍 Ejecutar validación contextual (LLM)",
        value=False,
        help="Usa GPT-4o para validar funciones contra normativa (más lento pero más preciso)"
    )

    weak_verbs_analysis = st.checkbox(
        "⚠️ Análisis de verbos débiles",
        value=True,
        help="Detecta verbos sin potencia normativa"
    )

    st.session_state.analysis_options.update({
        'contextual_validation': contextual_validation,
        'weak_verbs_analysis': weak_verbs_analysis,
    })

    st.markdown("---")

    # Configuración técnica
    with st.expander("🔧 Configuración Técnica Avanzada"):
        model = st.selectbox(
            "Modelo LLM:",
            options=["openai/gpt-4o", "openai/gpt-4", "openai/gpt-3.5-turbo"],
            index=0
        )

        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="Menor = más determinista, Mayor = más creativo"
        )

        max_tokens = st.number_input(
            "Max tokens:",
            min_value=1000,
            max_value=8000,
            value=4000,
            step=500
        )

        st.session_state.analysis_options.update({
            'model': model,
            'temperature': temperature,
            'max_tokens': max_tokens,
        })

    st.markdown("---")

    # Navegación
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.wizard_step = 2
            st.rerun()

    with col2:
        if st.button("Siguiente →", use_container_width=True, type="primary"):
            st.session_state.wizard_step = 4
            st.rerun()


def step_4_execute():
    """Paso 4: Confirmar y ejecutar análisis"""

    st.subheader("🚀 Paso 4: Ejecutar Análisis")

    # Mostrar resumen de configuración
    st.markdown("### ✅ Resumen de Configuración")

    with st.container():
        st.markdown(f"""
        **📊 Archivo Sidegor:**
        - Nombre: {st.session_state.uploaded_sidegor.name}
        - Tamaño: {st.session_state.uploaded_sidegor.size / 1024:.1f} KB
        - Total puestos: {st.session_state.sidegor_info['num_puestos']}

        **📜 Normativa:**
        - Nombre: {st.session_state.uploaded_normativa.name}
        - Tamaño: {st.session_state.uploaded_normativa.size / 1024:.1f} KB

        **🔍 Filtros Aplicados:**
        - Niveles: {', '.join(st.session_state.filters_config.get('niveles', ['Ninguno']))}
        - UR: {st.session_state.filters_config.get('ur', 'Ninguna')}
        - Código: {st.session_state.filters_config.get('codigo_pattern', 'Ninguno')}

        **🎯 Puestos a Procesar:** {st.session_state.filters_config.get('num_puestos_filtrados', 0)}

        **⚙️ Opciones:**
        - Validación contextual: {'✅ Sí' if st.session_state.analysis_options.get('contextual_validation') else '❌ No'}
        - Análisis verbos débiles: {'✅ Sí' if st.session_state.analysis_options.get('weak_verbs_analysis') else '❌ No'}
        - Generar PDF: {'✅ Sí' if st.session_state.analysis_options.get('generate_pdf') else '❌ No'}
        - Generar Excel: {'✅ Sí' if st.session_state.analysis_options.get('generate_excel') else '❌ No'}

        **⏱️ Tiempo Estimado:** ~{st.session_state.filters_config.get('num_puestos_filtrados', 0) * 0.5:.1f} minutos
        """)

    st.markdown("---")

    # Botones de acción
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.wizard_step = 3
            st.rerun()

    with col2:
        if st.button("🚀 Ejecutar Análisis", use_container_width=True, type="primary"):
            # Guardar configuración y ejecutar
            execute_analysis()

def execute_analysis():
    """Ejecuta el análisis con la configuración guardada"""

    st.info("🔄 Iniciando análisis... Esta funcionalidad se implementará en la siguiente versión.")

    # TODO: Implementar integración con el sistema v5.0
    # Por ahora, mostramos un mensaje de progreso simulado

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"Procesando... {i+1}%")
        time.sleep(0.02)

    st.success("✅ Análisis completado (simulado)")
    st.balloons()

    if st.button("Ver Resultados"):
        st.session_state.page = 'results'
        st.rerun()


if __name__ == "__main__":
    show()
