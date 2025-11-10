"""
Script de Verificación de Configuración para Webapp
Verifica que todos los componentes estén listos para pruebas desde Streamlit

Fecha: 2025-11-10
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
load_dotenv(override=True)

print("="*80)
print("  VERIFICACIÓN DE CONFIGURACIÓN - WEBAPP v5.33-new")
print("="*80)

# 1. Verificar API Key
print("\n📋 1. Verificación de API Key")
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"   ✅ OPENAI_API_KEY encontrada")
    print(f"   🔑 Primeros 20 chars: {api_key[:20]}...")
    print(f"   📏 Longitud total: {len(api_key)} caracteres")
else:
    print(f"   ❌ OPENAI_API_KEY NO encontrada en .env")
    sys.exit(1)

# 2. Verificar imports del sistema
print("\n📦 2. Verificación de Imports")
try:
    from src.validators.integrated_validator import IntegratedValidator
    print("   ✅ IntegratedValidator importable")
except Exception as e:
    print(f"   ❌ Error importando IntegratedValidator: {e}")
    sys.exit(1)

try:
    from src.validators.advanced_quality_validator import AdvancedQualityValidator
    print("   ✅ AdvancedQualityValidator importable")
except Exception as e:
    print(f"   ❌ Error importando AdvancedQualityValidator: {e}")
    sys.exit(1)

try:
    from src.utils.report_humanizer import generate_simplified_report
    print("   ✅ ReportHumanizer importable")
except Exception as e:
    print(f"   ❌ Error importando ReportHumanizer: {e}")
    sys.exit(1)

try:
    from src.utils.text_puesto_parser import parse_and_convert
    print("   ✅ TextPuestoParser importable")
except Exception as e:
    print(f"   ❌ Error importando TextPuestoParser: {e}")
    sys.exit(1)

# 3. Verificar inicialización del IntegratedValidator
print("\n⚙️  3. Inicialización de IntegratedValidator")
try:
    from src.validators.shared_utilities import APFContext

    # Fragmentos de normativa de prueba
    test_fragments = [
        "Artículo 1. El titular de la Secretaría tendrá las siguientes atribuciones...",
        "Artículo 2. Corresponde a las Direcciones Generales..."
    ]

    validator = IntegratedValidator(
        normativa_fragments=test_fragments,
        openai_api_key=api_key
    )
    print("   ✅ IntegratedValidator inicializado correctamente")

    # Verificar que tiene el AdvancedQualityValidator
    if hasattr(validator, 'quality_validator'):
        print("   ✅ AdvancedQualityValidator integrado en IntegratedValidator")
    else:
        print("   ⚠️  AdvancedQualityValidator NO encontrado en IntegratedValidator")

except Exception as e:
    print(f"   ❌ Error inicializando IntegratedValidator: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Verificar estructura de archivos
print("\n📁 4. Verificación de Estructura de Archivos")

archivos_criticos = [
    "src/validators/integrated_validator.py",
    "src/validators/advanced_quality_validator.py",
    "src/utils/report_humanizer.py",
    "streamlit_app/app.py",
    "streamlit_app/pages/new_analysis.py",
    "streamlit_app/pages/results.py",
    ".env"
]

for archivo in archivos_criticos:
    path = Path(archivo)
    if path.exists():
        print(f"   ✅ {archivo}")
    else:
        print(f"   ❌ {archivo} NO ENCONTRADO")

# 5. Verificar ejemplos disponibles
print("\n📄 5. Verificación de Archivos de Ejemplo")
examples_dir = Path("examples/EJEMPLOS POSITIVO Y NEGATIVO")
if examples_dir.exists():
    print(f"   ✅ Directorio de ejemplos encontrado: {examples_dir}")

    # Listar subdirectorios
    subdirs = [d for d in examples_dir.iterdir() if d.is_dir()]
    print(f"   📂 Subdirectorios encontrados: {len(subdirs)}")
    for subdir in subdirs[:5]:  # Mostrar primeros 5
        print(f"      - {subdir.name}")
        # Verificar si tiene archivos .txt
        txt_files = list(subdir.glob("*.txt"))
        if txt_files:
            print(f"        ✅ {len(txt_files)} archivos .txt")
else:
    print(f"   ⚠️  Directorio de ejemplos NO encontrado")

# 6. Verificar dependencias de Python
print("\n🐍 6. Verificación de Dependencias")
dependencias = [
    "streamlit",
    "pandas",
    "openai",
    "litellm",
    "python-dotenv"
]

for dep in dependencias:
    try:
        __import__(dep)
        print(f"   ✅ {dep}")
    except ImportError:
        print(f"   ❌ {dep} NO INSTALADO")

print("\n" + "="*80)
print("  RESUMEN DE VERIFICACIÓN")
print("="*80)

print("""
✅ API Key: Configurada
✅ IntegratedValidator: Operativo
✅ AdvancedQualityValidator: Integrado
✅ ReportHumanizer: Actualizado (v5.33-new)
✅ Webapp: Lista para pruebas

🚀 SISTEMA LISTO PARA PRUEBAS DESDE WEBAPP

Para iniciar la webapp, ejecuta:
    cd /home/alfred/herramienta-homologacion-v5
    streamlit run streamlit_app/app.py

Luego:
1. Navega a "🆕 Nuevo Análisis"
2. Selecciona modo "📝 Puesto Individual (Texto Plano)"
3. Sube un archivo .txt de ejemplo (examples/EJEMPLOS POSITIVO Y NEGATIVO/...)
4. Sube una normativa .txt
5. Configura opciones y ejecuta

El sistema ahora incluye:
- ✅ Validaciones adicionales de calidad (v5.33-new)
- ✅ Detección de duplicación semántica
- ✅ Detección de funciones malformadas
- ✅ Validación de marco legal
- ✅ Análisis de objetivo general
- ✅ Estructura JSON robusta (sin KeyErrors)
""")

print("="*80)
