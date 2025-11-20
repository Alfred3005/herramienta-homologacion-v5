"""
Sistema de Homologación APF - Aplicación Principal Streamlit
Interfaz web para análisis de puestos y validación contra normativas
"""

import streamlit as st
from pathlib import Path
import sys

# Agregar el directorio raíz al path para importar módulos
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Leer versión del sistema
def get_version():
    """Lee la versión del archivo VERSION"""
    version_file = root_dir / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "5.0"

VERSION = get_version()

# Configuración de página
st.set_page_config(
    page_title="Sistema de Homologación APF",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Alfred3005/herramienta-homologacion-v5',
        'Report a bug': 'https://github.com/Alfred3005/herramienta-homologacion-v5/issues',
        'About': """
        # Sistema de Homologación APF v5.41

        Herramienta para análisis y validación de puestos de la
        Administración Pública Federal contra normativas oficiales.

        ## ✨ Nuevas Características v5.41

        **Sistema Jerárquico de Herencia Normativa:**
        - Identificación inteligente de instituciones (sin hardcoding)
        - 4 niveles de alineación jerárquica con scores granulares
        - Análisis función por función con distancia jerárquica
        - Diferenciación entre herencia directa, del jefe directo, y lejana

        **Niveles de Alineación:**
        - 🟢 Nivel 1: Alineación Directa (Score: 0.9)
        - 🔵 Nivel 2: Herencia del Jefe Directo (Score: 0.75)
        - 🟡 Nivel 3: Herencia Lejana en Organismo (Score: 0.55)
        - 🔴 Nivel 4: No Alineado (Score: 0.0)

        **Desarrollado con**: Python 3.12, Streamlit, OpenAI GPT-4o-mini

        **Modelo de IA**: GPT-4o-mini (94.6% más económico que GPT-4o)
        """
    }
)

# CSS personalizado con soporte para tema oscuro
st.markdown("""
<style>
    /* Mejoras visuales */
    .main > div {
        padding-top: 2rem;
    }

    /* Cards personalizadas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }

    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Botones mejorados */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.5rem;
    }

    /* Progress bar mejorado */
    .stProgress > div > div {
        border-radius: 10px;
    }

    /* Upload zone */
    .uploadedFile {
        border-radius: 8px;
    }

    /* Sidebar styling - Light theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }

    [data-testid="stSidebar"] * {
        color: #1f1f1f !important;
    }

    [data-testid="stSidebar"] h3 {
        color: #1f1f1f !important;
    }

    [data-testid="stSidebar"] a {
        color: #667eea !important;
    }

    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: #666 !important;
    }

    /* Dark theme overrides */
    @media (prefers-color-scheme: dark) {
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a1a 0%, #0e1117 100%);
        }

        [data-testid="stSidebar"] * {
            color: #fafafa !important;
        }

        [data-testid="stSidebar"] h3 {
            color: #fafafa !important;
        }

        [data-testid="stSidebar"] a {
            color: #8b9eff !important;
        }

        [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
            color: #a0a0a0 !important;
        }
    }

    /* Forzar estilos cuando Streamlit detecta dark theme */
    [data-theme="dark"] [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0e1117 100%);
    }

    [data-theme="dark"] [data-testid="stSidebar"] * {
        color: #fafafa !important;
    }

    [data-theme="dark"] [data-testid="stSidebar"] h3 {
        color: #fafafa !important;
    }

    [data-theme="dark"] [data-testid="stSidebar"] a {
        color: #8b9eff !important;
    }

    [data-theme="dark"] [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: #a0a0a0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Sidebar - Navegación principal
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: #667eea; margin: 0;'>🏛️ APF</h2>
            <p style='opacity: 0.8; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Sistema de Homologación</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navegación con radio buttons (mejor UX que múltiples botones)
    st.markdown("### 🧭 Navegación")

    page_options = {
        "🏠 Inicio": "home",
        "🆕 Nuevo Análisis": "new_analysis",
        "📊 Resultados": "results",
        "📚 Historial": "history"
    }

    # Encontrar página actual para el radio button
    current_page_label = [k for k, v in page_options.items() if v == st.session_state.page][0]

    selected_page = st.radio(
        "Selecciona una página:",
        options=list(page_options.keys()),
        index=list(page_options.keys()).index(current_page_label),
        label_visibility="collapsed"
    )

    # Cambiar página si selecciona otra
    if page_options[selected_page] != st.session_state.page:
        st.session_state.page = page_options[selected_page]
        st.rerun()

    st.markdown("---")

    # Información del sistema
    st.markdown("### ℹ️ Sistema")
    st.markdown(f"""
    **Versión**: v5.41
    **Estado**: ✅ Operativo
    **Modelo**: GPT-4o-mini
    **Última actualización**: 2025-11-19

    🆕 **Nuevo en v5.41:**
    Sistema Jerárquico de Herencia Normativa con 4 niveles de alineación
    """)

    st.markdown("---")

    # Links útiles
    st.markdown("### 🔗 Enlaces")
    st.markdown("""
    - [📖 Documentación](https://docs.example.com)
    - [🐛 Reportar Bug](https://github.com/repo/issues)
    - [💬 Soporte](mailto:soporte@example.com)
    """)

    st.markdown("---")

    # Footer sidebar
    st.caption("🏛️ Sistema de Homologación APF")
    st.caption("v5.41 © 2025")

# Cargar página correspondiente
if st.session_state.page == 'home':
    from pages import home
    home.show()
elif st.session_state.page == 'new_analysis':
    from pages import new_analysis
    new_analysis.show()
elif st.session_state.page == 'results':
    from pages import results
    results.show()
elif st.session_state.page == 'history':
    from pages import history
    history.show()

# Footer global en todas las páginas (parte inferior)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.85rem; padding: 1rem 0;'>"
    "Sistema de Homologación APF <strong>v5.41</strong> - Sistema Jerárquico de Herencia Normativa | Powered by OpenAI GPT-4o-mini"
    "</div>",
    unsafe_allow_html=True
)
