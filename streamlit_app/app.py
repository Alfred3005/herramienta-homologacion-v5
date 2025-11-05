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

# Configuración de página
st.set_page_config(
    page_title="Sistema de Homologación APF",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/tu-repo/herramienta-homologacion',
        'Report a bug': 'https://github.com/tu-repo/herramienta-homologacion/issues',
        'About': """
        # Sistema de Homologación APF v5.0

        Herramienta para análisis y validación de puestos de la
        Administración Pública Federal contra normativas oficiales.

        **Desarrollado con**: Python 3.12, Streamlit, OpenAI GPT-4
        """
    }
)

# CSS personalizado
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

    /* Alerts mejorados */
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }

    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }

    .warning-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }

    /* Progress bar mejorado */
    .stProgress > div > div {
        border-radius: 10px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }

    /* Upload zone */
    .uploadedFile {
        border-radius: 8px;
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
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=APF+Homologación",
             use_container_width=True)

    st.markdown("---")

    st.markdown("### 🧭 Navegación")

    # Botones de navegación
    if st.button("🏠 Inicio", use_container_width=True,
                 type="primary" if st.session_state.page == 'home' else "secondary"):
        st.session_state.page = 'home'
        st.rerun()

    if st.button("🆕 Nuevo Análisis", use_container_width=True,
                 type="primary" if st.session_state.page == 'new_analysis' else "secondary"):
        st.session_state.page = 'new_analysis'
        st.rerun()

    if st.button("📊 Resultados", use_container_width=True,
                 type="primary" if st.session_state.page == 'results' else "secondary"):
        st.session_state.page = 'results'
        st.rerun()

    if st.button("📚 Historial", use_container_width=True,
                 type="primary" if st.session_state.page == 'history' else "secondary"):
        st.session_state.page = 'history'
        st.rerun()

    st.markdown("---")

    # Información del sistema
    st.markdown("### ℹ️ Sistema")
    st.markdown("""
    **Versión**: 5.0
    **Estado**: ✅ Operativo
    **Modelo**: GPT-4o
    """)

    st.markdown("---")

    # Links útiles
    st.markdown("### 🔗 Enlaces")
    st.markdown("""
    - 📖 [Documentación](https://docs.example.com)
    - 🐛 [Reportar Bug](https://github.com/repo/issues)
    - 💬 [Soporte](mailto:soporte@example.com)
    """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>🏛️ Sistema de Homologación APF</p>
        <p>© 2025 - Desarrollado con ❤️</p>
    </div>
    """, unsafe_allow_html=True)

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
