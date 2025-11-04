#!/usr/bin/env python3
"""
Script para procesar puestos SABG de niveles G a K.
Genera documentos RHNet virtuales y reportes consolidados.
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
    print("🚀 PROCESAMIENTO EN LOTE - SABG NIVELES G-K")
    print("=" * 70)
    print()

    # Configuración
    archivo_excel = "validación comparativa con otras URs/Reporte_DPP_27_000_SABG.xlsx"
    output_dir = "output/sabg_niveles_g_k"
    niveles = ["G", "H", "I", "J", "K"]
    ur_sabg = "27"

    # Verificar que archivo existe
    if not Path(archivo_excel).exists():
        print(f"❌ Error: Archivo no encontrado: {archivo_excel}")
        print()
        print("💡 Asegúrate de tener el archivo en la ubicación correcta.")
        print("   Archivos disponibles en 'validación comparativa con otras URs/':")

        validacion_dir = Path("validación comparativa con otras URs")
        if validacion_dir.exists():
            for f in validacion_dir.glob("*.xlsx"):
                print(f"   - {f.name}")

        return

    print(f"📂 Archivo Excel: {archivo_excel}")
    print(f"📁 Directorio salida: {output_dir}")
    print(f"📊 Niveles a procesar: {', '.join(niveles)}")
    print(f"🏢 Unidad Responsable: {ur_sabg}")
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
    filtro_ur = URFilter([ur_sabg])

    processor.add_filter(filtro_niveles)
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
