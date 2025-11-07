"""
Página de Resultados Detallados
Muestra análisis guardados con métricas y descarga de reportes
"""
import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import sys

# Añadir directorio src al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.report_humanizer import humanize_report

def show():
    st.title("📊 Resultados Detallados de Análisis")

    # Obtener análisis guardados
    output_dir = Path("output/analisis")
    if not output_dir.exists():
        st.warning("📁 No se encontraron análisis guardados")
        return

    json_files = sorted(output_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

    if not json_files:
        st.info("🔍 No hay análisis disponibles. Realiza un análisis en la página 'Nuevo Análisis'")
        return

    # Selector de análisis
    st.markdown("### 🗂️ Seleccionar Análisis")

    file_options = {}
    for f in json_files[:10]:  # Mostrar últimos 10
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                timestamp = datetime.fromisoformat(data.get('timestamp', ''))
                fecha_str = timestamp.strftime('%d/%m/%Y %H:%M:%S')
                total = data.get('total_puestos', 0)
                label = f"{fecha_str} - {total} puestos"
                file_options[label] = f
        except:
            continue

    if not file_options:
        st.error("❌ No se pudieron cargar los análisis")
        return

    selected_label = st.selectbox(
        "Análisis disponibles:",
        options=list(file_options.keys())
    )

    selected_file = file_options[selected_label]

    # Cargar datos
    with open(selected_file, 'r') as f:
        data = json.load(f)

    # Separador
    st.markdown("---")

    # SECCIÓN 1: Resumen General
    st.markdown("## 📈 Resumen General")

    total_puestos = data['total_puestos']
    resultados = data['resultados']

    aprobados = [r for r in resultados if r['validacion']['resultado'] in ['APROBADO_CON_OBSERVACIONES', 'APROBADO_PLENO']]
    rechazados = [r for r in resultados if r['validacion']['resultado'] == 'RECHAZADO']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📋 Total Analizado",
            value=total_puestos
        )

    with col2:
        st.metric(
            label="✅ Aprobados",
            value=len(aprobados),
            delta=f"{len(aprobados)/total_puestos*100:.0f}%"
        )

    with col3:
        st.metric(
            label="❌ Rechazados",
            value=len(rechazados),
            delta=f"-{len(rechazados)/total_puestos*100:.0f}%",
            delta_color="inverse"
        )

    with col4:
        confianza_prom = sum(r['validacion']['confianza'] for r in resultados) / len(resultados)
        st.metric(
            label="🎯 Confianza Promedio",
            value=f"{confianza_prom:.2f}"
        )

    # SECCIÓN 2: Gráficos
    st.markdown("---")
    st.markdown("## 📊 Visualizaciones")

    tab1, tab2, tab3 = st.tabs(["Distribución", "Por Criterio", "Detalle Puestos"])

    with tab1:
        # Gráfico de pastel
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Aprobados', 'Rechazados'],
            values=[len(aprobados), len(rechazados)],
            marker=dict(colors=['#4CAF50', '#F44336']),
            hole=0.4
        )])
        fig_pie.update_layout(
            title="Distribución de Resultados",
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        # Análisis por criterio
        criterios_data = {
            'Criterio': [],
            'PASS': [],
            'FAIL': []
        }

        for criterio_key, criterio_name in [
            ('criterio_1_verbos', 'Verbos Débiles'),
            ('criterio_2_contextual', 'Contextual'),
            ('criterio_3_impacto', 'Impacto Jerárquico')
        ]:
            pass_count = sum(1 for r in resultados if r['validacion']['criterios'][criterio_key]['resultado'] == 'PASS')
            fail_count = sum(1 for r in resultados if r['validacion']['criterios'][criterio_key]['resultado'] == 'FAIL')

            criterios_data['Criterio'].append(criterio_name)
            criterios_data['PASS'].append(pass_count)
            criterios_data['FAIL'].append(fail_count)

        df_criterios = pd.DataFrame(criterios_data)

        fig_criterios = go.Figure(data=[
            go.Bar(name='PASS', x=df_criterios['Criterio'], y=df_criterios['PASS'], marker_color='#4CAF50'),
            go.Bar(name='FAIL', x=df_criterios['Criterio'], y=df_criterios['FAIL'], marker_color='#F44336')
        ])
        fig_criterios.update_layout(
            title="Resultados por Criterio",
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig_criterios, use_container_width=True)

        # Estadísticas de criterios
        col1, col2, col3 = st.columns(3)

        with col1:
            c1_tasas = [r['validacion']['criterios']['criterio_1_verbos']['tasa_critica'] for r in resultados]
            st.metric("Criterio 1 - Tasa Crítica Prom.", f"{sum(c1_tasas)/len(c1_tasas):.0%}")

        with col2:
            c2_confianzas = [r['validacion']['criterios']['criterio_2_contextual']['alineacion']['confianza'] for r in resultados]
            st.metric("Criterio 2 - Confianza Prom.", f"{sum(c2_confianzas)/len(c2_confianzas):.2f}")

        with col3:
            c3_tasas = [r['validacion']['criterios']['criterio_3_impacto']['metricas']['tasa_critica'] for r in resultados]
            st.metric("Criterio 3 - Tasa Crítica Prom.", f"{sum(c3_tasas)/len(c3_tasas):.0%}")

    with tab3:
        # Tabla detallada de puestos
        st.markdown("### 📋 Detalle de Todos los Puestos")

        tabla_data = []
        for r in resultados:
            puesto = r['puesto']
            val = r['validacion']
            c1 = val['criterios']['criterio_1_verbos']
            c2 = val['criterios']['criterio_2_contextual']
            c3 = val['criterios']['criterio_3_impacto']

            tabla_data.append({
                'Código': puesto['codigo'],
                'Denominación': puesto['denominacion'],
                'Nivel': puesto['nivel'],
                'Resultado': val['resultado'],
                'Confianza': f"{val['confianza']:.2f}",
                'C1 (Verbos)': c1['resultado'],
                'C1 Tasa': f"{c1['tasa_critica']:.0%}",
                'C2 (Context)': c2['resultado'],
                'C2 Conf': f"{c2['alineacion']['confianza']:.2f}",
                'C3 (Impacto)': c3['resultado'],
                'C3 Tasa': f"{c3['metricas']['tasa_critica']:.0%}"
            })

        df_detalle = pd.DataFrame(tabla_data)

        # Aplicar estilo
        def color_resultado(val):
            if 'APROBADO' in val:
                return 'background-color: #C8E6C9'
            elif 'RECHAZADO' in val:
                return 'background-color: #FFCDD2'
            return ''

        def color_criterio(val):
            if val == 'PASS':
                return 'background-color: #C8E6C9'
            elif val == 'FAIL':
                return 'background-color: #FFCDD2'
            return ''

        styled_df = df_detalle.style.applymap(
            color_resultado, subset=['Resultado']
        ).applymap(
            color_criterio, subset=['C1 (Verbos)', 'C2 (Context)', 'C3 (Impacto)']
        )

        st.dataframe(styled_df, use_container_width=True, height=600)

    # SECCIÓN 3: Descargas
    st.markdown("---")
    st.markdown("## 💾 Descargar Reportes")

    col1, col2 = st.columns(2)

    with col1:
        # Descargar JSON completo
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📄 Descargar JSON Completo",
            data=json_str,
            file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    with col2:
        # Descargar Excel con resultados
        excel_data = df_detalle.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Descargar CSV",
            data=excel_data,
            file_name=f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    # SECCIÓN 3.5: Humanización de Reportes con LLM
    st.markdown("---")
    st.markdown("## 🤖 Generar Reporte Humanizado")
    st.markdown("Convierte el análisis técnico a lenguaje natural comprensible para auditoría y revisión humana.")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        modo_reporte = st.selectbox(
            "Selecciona el tipo de reporte:",
            options=["simplificado", "detallado"],
            format_func=lambda x: "📋 Resumen Ejecutivo (1-2 páginas)" if x == "simplificado" else "📊 Análisis Completo para Auditoría",
            help="Simplificado: Resumen breve para decisiones rápidas. Detallado: Análisis exhaustivo con evidencias."
        )

    with col2:
        generar_btn = st.button("🚀 Generar Reporte", type="primary", use_container_width=True)

    with col3:
        if 'reporte_humanizado' in st.session_state:
            st.download_button(
                label="💾 Descargar MD",
                data=st.session_state['reporte_humanizado'],
                file_name=f"reporte_{modo_reporte}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )

    if generar_btn:
        with st.spinner(f"🤖 Generando reporte {modo_reporte}... (esto puede tomar 10-30 segundos)"):
            try:
                # Generar reporte usando LLM
                reporte = humanize_report(str(selected_file), modo_reporte)

                # Guardar en session_state para descargar
                st.session_state['reporte_humanizado'] = reporte

                # Mostrar reporte
                st.success(f"✅ Reporte {modo_reporte} generado exitosamente!")
                st.markdown("### 📄 Vista Previa del Reporte")

                # Mostrar en expander para no ocupar mucho espacio
                with st.expander("📖 Ver reporte completo", expanded=True):
                    st.markdown(reporte)

            except Exception as e:
                st.error(f"❌ Error al generar reporte: {str(e)}")
                st.exception(e)

    # Mostrar reporte previo si existe
    elif 'reporte_humanizado' in st.session_state:
        st.info("💡 Hay un reporte generado previamente. Usa el botón 'Descargar MD' o genera uno nuevo.")

    # SECCIÓN 4: Análisis Detallado de Puestos
    st.markdown("---")
    st.markdown("## 🔍 Explorar Puesto Individual")

    puestos_dict = {f"{r['puesto']['codigo']} - {r['puesto']['denominacion']}": r for r in resultados}
    selected_puesto = st.selectbox(
        "Selecciona un puesto para ver detalles:",
        options=list(puestos_dict.keys())
    )

    if selected_puesto:
        puesto_data = puestos_dict[selected_puesto]
        puesto = puesto_data['puesto']
        val = puesto_data['validacion']

        st.markdown(f"### {puesto['denominacion']}")
        st.markdown(f"**Código:** {puesto['codigo']} | **Nivel:** {puesto['nivel']}")

        # Resultado general
        if val['resultado'] in ['APROBADO_CON_OBSERVACIONES', 'APROBADO_PLENO']:
            st.success(f"✅ {val['resultado']}")
        else:
            st.error(f"❌ {val['resultado']}")

        st.markdown(f"**Confianza Global:** {val['confianza']:.2f}")
        st.markdown(f"**Criterios Aprobados:** {val['criterios_aprobados']}/3")

        # Detalles por criterio
        st.markdown("#### 📊 Detalles por Criterio")

        c1, c2, c3 = st.columns(3)

        with c1:
            c1_data = val['criterios']['criterio_1_verbos']
            with st.container():
                st.markdown("**Criterio 1: Verbos Débiles**")
                if c1_data['resultado'] == 'PASS':
                    st.success("✅ PASS")
                else:
                    st.error("❌ FAIL")
                st.metric("Tasa Crítica", f"{c1_data['tasa_critica']:.0%}")
                st.caption(f"Rechazadas: {c1_data['funciones_rechazadas']}/{c1_data['total_funciones']}")

        with c2:
            c2_data = val['criterios']['criterio_2_contextual']
            with st.container():
                st.markdown("**Criterio 2: Contextual**")
                if c2_data['resultado'] == 'PASS':
                    st.success("✅ PASS")
                else:
                    st.error("❌ FAIL")
                st.metric("Confianza", f"{c2_data['alineacion']['confianza']:.2f}")
                st.caption(f"Alineación: {c2_data['alineacion']['clasificacion']}")

        with c3:
            c3_data = val['criterios']['criterio_3_impacto']
            with st.container():
                st.markdown("**Criterio 3: Impacto**")
                if c3_data['resultado'] == 'PASS':
                    st.success("✅ PASS")
                else:
                    st.error("❌ FAIL")
                st.metric("Tasa Crítica", f"{c3_data['metricas']['tasa_critica']:.0%}")
                st.caption(f"Critical: {c3_data['metricas'].get('funciones_critical', 0)}")

        # Razonamiento
        with st.expander("📝 Ver Razonamiento Detallado"):
            st.markdown(val['razonamiento'])
            st.markdown(f"**Acción Requerida:** {val['accion_requerida']}")

if __name__ == "__main__":
    show()
