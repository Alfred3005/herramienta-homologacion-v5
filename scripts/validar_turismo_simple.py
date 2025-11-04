#!/usr/bin/env python3
"""
Script simplificado para extraer y analizar puestos de TURISMO niveles G-K.
Extrae información de cada puesto y genera reporte básico.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import PipelineFactory
from src.core import ExtractionMode


def main():
    documentos_dir = sys.argv[1] if len(sys.argv) > 1 else \
        "output/Reporte_DPP_21_000_03-11-2025_TURISMO_SC_niveles_G_H_J_K/documentos"

    normativa_path = sys.argv[2] if len(sys.argv) > 2 else \
        "validación comparativa con otras URs/REGLAMENTO Interior de la Secretaría de Turismo.txt"

    output_dir = sys.argv[3] if len(sys.argv) > 3 else \
        str(Path(documentos_dir).parent / "analisis")

    print("=" * 70)
    print("🔍 ANÁLISIS DE PUESTOS - TURISMO G-K")
    print("=" * 70)
    print()
    print(f"📂 Documentos: {documentos_dir}")
    print(f"📜 Normativa: {normativa_path}")
    print(f"📁 Salida: {output_dir}")
    print()

    # Crear directorio de salida
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Listar documentos
    docs_path = Path(documentos_dir)
    documentos = sorted(docs_path.glob("*_rhnet.txt"))

    if not documentos:
        print("⚠️ No se encontraron documentos RHNet")
        return

    print(f"📋 Total documentos: {len(documentos)}")
    print()

    # Cargar normativa
    print("📖 Cargando normativa...")
    with open(normativa_path, 'r', encoding='utf-8') as f:
        normativa_content = f.read()
    print(f"✅ Normativa: {len(normativa_content)} caracteres")
    print()

    # Inicializar pipeline
    print("🔧 Inicializando pipeline de extracción...")
    extractor = PipelineFactory.create_simple_pipeline(
        model="openai/gpt-4o",
        enable_logging=False
    )
    print("✅ Pipeline listo")
    print()

    # Procesar cada documento
    print("=" * 70)
    print("EXTRAYENDO INFORMACIÓN DE PUESTOS")
    print("=" * 70)
    print()

    resultados = []
    inicio = datetime.now()

    for idx, doc_path in enumerate(documentos, 1):
        codigo_puesto = doc_path.stem.replace("_rhnet", "")
        print(f"[{idx}/{len(documentos)}] Procesando: {codigo_puesto}")

        try:
            # Extraer información
            result = extractor.extract_from_file(
                str(doc_path),
                mode=ExtractionMode.INTELLIGENT,
                max_tokens=4000,
                temperature=0.1
            )

            if result['status'] == 'success':
                data = result['data']
                ident = data.get('identificacion_puesto', {})
                funciones = data.get('funciones', [])
                validation = result.get('validation', {})

                print(f"  ✅ Extraído: {len(funciones)} funciones")
                print(f"  📊 Validación: {validation.get('error_count', 0)} errores, "
                      f"{validation.get('warning_count', 0)} warnings")

                # Guardar JSON individual
                json_path = output_path / f"{codigo_puesto}_extracted.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                # Agregar a resultados
                resultados.append({
                    "codigo": codigo_puesto,
                    "denominacion": ident.get('denominacion_puesto', 'N/A'),
                    "nivel_salarial": ident.get('nivel_salarial', {}).get('codigo', 'N/A'),
                    "num_funciones": len(funciones),
                    "error_count": validation.get('error_count', 0),
                    "warning_count": validation.get('warning_count', 0),
                    "status": "success",
                    "documento": str(doc_path),
                    "json_path": str(json_path)
                })

            else:
                print(f"  ❌ Error: {result.get('error', 'Unknown')}")
                resultados.append({
                    "codigo": codigo_puesto,
                    "status": "error",
                    "error": result.get('error', 'Unknown'),
                    "documento": str(doc_path)
                })

        except Exception as e:
            print(f"  ❌ Excepción: {e}")
            resultados.append({
                "codigo": codigo_puesto,
                "status": "exception",
                "error": str(e),
                "documento": str(doc_path)
            })

        print()

    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()

    # Generar resumen
    print()
    print("=" * 70)
    print("📊 RESUMEN DEL ANÁLISIS")
    print("=" * 70)
    print(f"Inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duración: {duracion:.1f} segundos")
    print()

    total = len(resultados)
    exitosos = len([r for r in resultados if r["status"] == "success"])
    errores = total - exitosos

    print(f"Total documentos: {total}")
    print(f"Exitosos: {exitosos} ({100*exitosos/total:.1f}%)")
    print(f"Errores: {errores}")
    print()

    if exitosos > 0:
        # Estadísticas
        total_funciones = sum(r.get("num_funciones", 0) for r in resultados if r["status"] == "success")
        total_errors = sum(r.get("error_count", 0) for r in resultados if r["status"] == "success")
        total_warnings = sum(r.get("warning_count", 0) for r in resultados if r["status"] == "success")

        print(f"Total funciones extraídas: {total_funciones}")
        print(f"Promedio por puesto: {total_funciones/exitosos:.1f}")
        print()
        print(f"Total errores de validación: {total_errors}")
        print(f"Total warnings de validación: {total_warnings}")
        print()

    # Guardar consolidado
    consolidado_path = output_path / "analisis_consolidado.json"
    consolidado = {
        "metadata": {
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "duracion_segundos": duracion,
            "total_documentos": total,
            "exitosos": exitosos,
            "errores": errores,
            "normativa": str(normativa_path),
            "documentos_dir": str(documentos_dir)
        },
        "resultados": resultados
    }

    with open(consolidado_path, 'w', encoding='utf-8') as f:
        json.dump(consolidado, f, indent=2, ensure_ascii=False)

    print(f"✅ Reporte consolidado: {consolidado_path}")
    print()

    # Generar resumen de texto
    resumen_path = output_path / "analisis_resumen.txt"
    with open(resumen_path, 'w', encoding='utf-8') as f:
        f.write("📊 RESUMEN DE ANÁLISIS - TURISMO G-K\n")
        f.write("=" * 70 + "\n")
        f.write(f"Inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duración: {duracion:.1f} segundos\n\n")
        f.write(f"Total documentos: {total}\n")
        f.write(f"Exitosos: {exitosos} ({100*exitosos/total:.1f}%)\n")
        f.write(f"Errores: {errores}\n\n")

        if exitosos > 0:
            f.write(f"Total funciones extraídas: {total_funciones}\n")
            f.write(f"Promedio por puesto: {total_funciones/exitosos:.1f}\n\n")

        f.write("Resultados detallados:\n")
        for r in resultados:
            if r["status"] == "success":
                f.write(f"  {r['codigo']}: {r['num_funciones']} funciones, "
                        f"{r['error_count']} errores, {r['warning_count']} warnings\n")
            else:
                f.write(f"  {r['codigo']}: {r['status']}\n")

    print(f"✅ Resumen texto: {resumen_path}")
    print()
    print("=" * 70)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 70)
    print()
    print("📝 NOTA: Este análisis extrae información de cada puesto.")
    print("   Para validar contra normativa, se requiere implementar")
    print("   el ContextualValidator con comparación semántica.")


if __name__ == "__main__":
    main()
