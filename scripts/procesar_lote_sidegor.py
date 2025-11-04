#!/usr/bin/env python3
"""
Script para procesar puestos en lote desde archivos Excel Sidegor.
Genera documentos RHNet virtuales y reportes consolidados.

Uso:
    python scripts/procesar_lote_sidegor.py <archivo_excel> <niveles> [ur]

Ejemplos:
    # Procesar TURISMO niveles G-K
    python scripts/procesar_lote_sidegor.py "validación comparativa con otras URs/Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx" "G,H,I,J,K"

    # Procesar HACIENDA niveles G-K para UR 06
    python scripts/procesar_lote_sidegor.py "validación comparativa con otras URs/Reporte_DPP_06_000_03-11-2025 HACIENDA SC.xlsx" "G,H,I,J,K" "06"
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.adapters import (
    SidegorAdapter,
    RHNetDocumentGenerator,
    SidegorBatchProcessor
)
from src.filters import NivelSalarialFilter, URFilter
from src.reporting import BatchReporter


def main():
    """Función principal"""
    print("=" * 70)
    print("🚀 PROCESAMIENTO EN LOTE - SIDEGOR")
    print("=" * 70)
    print()

    # Parsear argumentos
    if len(sys.argv) < 3:
        print("❌ Error: Argumentos insuficientes")
        print()
        print("Uso:")
        print('  python scripts/procesar_lote_sidegor.py <archivo_excel> "<niveles>" [ur]')
        print()
        print("Ejemplos:")
        print('  python scripts/procesar_lote_sidegor.py "validación comparativa con otras URs/Reporte_DPP_21_000_03-11-2025 TURISMO SC.xlsx" "G,H,I,J,K"')
        print('  python scripts/procesar_lote_sidegor.py "archivo.xlsx" "K,L,M" "27"')
        print()
        print("Archivos disponibles:")
        validacion_dir = Path("validación comparativa con otras URs")
        if validacion_dir.exists():
            for f in validacion_dir.glob("*.xlsx"):
                print(f"  - {f}")
        return

    archivo_excel = sys.argv[1]
    niveles_str = sys.argv[2]
    ur_code = sys.argv[3] if len(sys.argv) > 3 else None

    # Parsear niveles
    niveles = [n.strip().upper() for n in niveles_str.split(",")]

    # Configuración
    archivo_path = Path(archivo_excel)
    archivo_nombre = archivo_path.stem.replace(" ", "_")
    niveles_nombre = "_".join(niveles)

    output_dir = f"output/{archivo_nombre}_niveles_{niveles_nombre}"

    # Verificar que archivo existe
    if not archivo_path.exists():
        print(f"❌ Error: Archivo no encontrado: {archivo_excel}")
        return

    print(f"📂 Archivo Excel: {archivo_excel}")
    print(f"📁 Directorio salida: {output_dir}")
    print(f"📊 Niveles a procesar: {', '.join(niveles)}")
    if ur_code:
        print(f"🏢 Unidad Responsable: {ur_code}")
    print()

    # Paso 1: Cargar archivo Excel
    print("=" * 70)
    print("PASO 1: Cargar archivo Excel Sidegor")
    print("=" * 70)
    print()

    adapter = SidegorAdapter()

    if not adapter.cargar_archivo(archivo_excel):
        print("❌ Error cargando archivo")
        return

    print()

    # Paso 2: Configurar generador de documentos
    print("=" * 70)
    print("PASO 2: Configurar generador de documentos RHNet")
    print("=" * 70)
    print()

    generator = RHNetDocumentGenerator(template="default")
    print("✅ Generador configurado (template: default)")
    print()

    # Paso 3: Configurar procesador en lote
    print("=" * 70)
    print("PASO 3: Configurar procesador en lote")
    print("=" * 70)
    print()

    processor = SidegorBatchProcessor(
        adapter=adapter,
        document_generator=generator,
        validation_pipeline=None  # Sin validación por ahora
    )

    # Agregar filtros
    filtro_niveles = NivelSalarialFilter(niveles)
    processor.add_filter(filtro_niveles)

    if ur_code:
        filtro_ur = URFilter([ur_code])
        processor.add_filter(filtro_ur)

    print("✅ Procesador configurado")
    print(f"   Filtros: {len(processor.filtros)}")
    print()

    # Paso 4: Procesar lote
    print("=" * 70)
    print("PASO 4: Procesar lote completo")
    print("=" * 70)
    print()

    resultado = processor.procesar_lote(
        validar=False,  # Sin validación por ahora
        generar_documentos=True,
        output_dir=output_dir,
        guardar_intermedios=True
    )

    # Paso 5: Generar reportes
    print("=" * 70)
    print("PASO 5: Generar reportes consolidados")
    print("=" * 70)
    print()

    reporter = BatchReporter(resultado)

    # Reporte JSON
    json_path = f"{output_dir}/reporte_consolidado.json"
    reporter.generar_reporte_json(json_path)

    # Reporte Excel
    try:
        excel_path = f"{output_dir}/reporte_consolidado.xlsx"
        reporter.generar_reporte_excel(excel_path)
    except ImportError:
        print("⚠️ pandas no disponible, no se puede generar reporte Excel")
        print("   Instalar con: pip install pandas openpyxl")

    # Resumen texto
    txt_path = f"{output_dir}/resumen.txt"
    reporter.generar_resumen_texto(txt_path)

    # Estadísticas por nivel
    print()
    reporter.imprimir_estadisticas_por_nivel()

    # Resumen final
    print("=" * 70)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("=" * 70)
    print()
    print(f"📁 Archivos generados en: {output_dir}/")
    print(f"   • Documentos RHNet: {output_dir}/documentos/")
    print(f"   • Datos APF (JSON): {output_dir}/datos_apf/")
    print(f"   • Reporte JSON: {json_path}")
    print(f"   • Resumen texto: {txt_path}")

    if Path(f"{output_dir}/reporte_consolidado.xlsx").exists():
        print(f"   • Reporte Excel: {output_dir}/reporte_consolidado.xlsx")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
