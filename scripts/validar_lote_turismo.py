#!/usr/bin/env python3
"""
Script para validar puestos procesados contra normativa de TURISMO.
Toma los documentos RHNet generados y los valida contra el reglamento.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.agente_extractor import APFExtractor
from src.engines.contextual_validator import ContextualValidator
from src.providers.openai_provider import OpenAIProvider


def validar_lote_turismo(documentos_dir: str, normativa_path: str, output_dir: str):
    """
    Valida un lote de documentos RHNet contra normativa de TURISMO.

    Args:
        documentos_dir: Directorio con documentos RHNet (.txt)
        normativa_path: Ruta al archivo de normativa (REGLAMENTO)
        output_dir: Directorio donde guardar resultados
    """

    print("=" * 70)
    print("🔍 VALIDACIÓN EN LOTE - TURISMO")
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
        print("⚠️ No se encontraron documentos RHNet en el directorio")
        return

    print(f"📋 Total documentos a validar: {len(documentos)}")
    print()

    # Inicializar componentes
    print("🔧 Inicializando pipeline de validación...")
    llm_provider = OpenAIProvider()
    extractor = APFExtractor(llm_provider=llm_provider)
    validator = ContextualValidator(llm_provider=llm_provider)
    print("✅ Pipeline listo")
    print()

    # Cargar normativa
    print("📖 Cargando normativa...")
    with open(normativa_path, 'r', encoding='utf-8') as f:
        normativa_content = f.read()
    print(f"✅ Normativa cargada: {len(normativa_content)} caracteres")
    print()

    # Procesar cada documento
    print("=" * 70)
    print("VALIDANDO PUESTOS")
    print("=" * 70)
    print()

    resultados = []
    inicio = datetime.now()

    for idx, doc_path in enumerate(documentos, 1):
        codigo_puesto = doc_path.stem.replace("_rhnet", "")
        print(f"[{idx}/{len(documentos)}] Validando: {codigo_puesto}")

        try:
            # Leer documento
            with open(doc_path, 'r', encoding='utf-8') as f:
                documento_text = f.read()

            # Extraer datos APF
            print("  📄 Extrayendo datos APF...")
            datos_apf = extractor.extraer(documento_text)

            if datos_apf.get("error"):
                print(f"  ❌ Error en extracción: {datos_apf['error']}")
                resultados.append({
                    "codigo": codigo_puesto,
                    "status": "error_extraccion",
                    "error": datos_apf['error'],
                    "documento": str(doc_path)
                })
                continue

            # Validar contra normativa
            print("  🔍 Validando contra normativa...")
            resultado_validacion = validator.validar(
                puesto_data=datos_apf,
                normativa_fragmentos=[normativa_content]
            )

            print(f"  ✅ Resultado: {resultado_validacion.get('overall_assessment', 'N/A')}")

            # Guardar resultado individual
            resultado_file = output_path / f"{codigo_puesto}_validacion.json"
            with open(resultado_file, 'w', encoding='utf-8') as f:
                json.dump(resultado_validacion, f, indent=2, ensure_ascii=False)

            # Agregar a consolidado
            resultados.append({
                "codigo": codigo_puesto,
                "denominacion": datos_apf.get("identificacion", {}).get("denominacion_puesto", "N/A"),
                "nivel_salarial": datos_apf.get("identificacion", {}).get("nivel_salarial", {}).get("codigo", "N/A"),
                "status": "validado",
                "assessment": resultado_validacion.get("overall_assessment", "N/A"),
                "confidence": resultado_validacion.get("confidence_score", 0),
                "documento": str(doc_path),
                "resultado_path": str(resultado_file)
            })

        except Exception as e:
            print(f"  ❌ Error: {e}")
            resultados.append({
                "codigo": codigo_puesto,
                "status": "error",
                "error": str(e),
                "documento": str(doc_path)
            })

        print()

    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()

    # Generar resumen
    print()
    print("=" * 70)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 70)
    print(f"Inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duración: {duracion:.1f} segundos")
    print()

    total = len(resultados)
    validados = len([r for r in resultados if r["status"] == "validado"])
    errores = total - validados

    print(f"Total documentos: {total}")
    print(f"Validados: {validados} ({100*validados/total:.1f}%)")
    print(f"Errores: {errores}")
    print()

    # Estadísticas por assessment
    if validados > 0:
        print("Distribución por assessment:")
        assessments = {}
        for r in resultados:
            if r["status"] == "validado":
                assessment = r["assessment"]
                assessments[assessment] = assessments.get(assessment, 0) + 1

        for assessment, count in sorted(assessments.items()):
            print(f"  • {assessment}: {count} ({100*count/validados:.1f}%)")
        print()

    # Guardar consolidado
    consolidado_path = output_path / "validacion_consolidada.json"
    consolidado = {
        "metadata": {
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "duracion_segundos": duracion,
            "total_documentos": total,
            "validados": validados,
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
    resumen_path = output_path / "validacion_resumen.txt"
    with open(resumen_path, 'w', encoding='utf-8') as f:
        f.write("📊 RESUMEN DE VALIDACIÓN - TURISMO G-K\n")
        f.write("=" * 70 + "\n")
        f.write(f"Inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Fin: {fin.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duración: {duracion:.1f} segundos\n\n")
        f.write(f"Total documentos: {total}\n")
        f.write(f"Validados: {validados} ({100*validados/total:.1f}%)\n")
        f.write(f"Errores: {errores}\n\n")

        if validados > 0:
            f.write("Distribución por assessment:\n")
            for assessment, count in sorted(assessments.items()):
                f.write(f"  • {assessment}: {count} ({100*count/validados:.1f}%)\n")
            f.write("\n")

        f.write("Resultados detallados:\n")
        for r in resultados:
            if r["status"] == "validado":
                f.write(f"  {r['codigo']}: {r['assessment']} (confidence: {r['confidence']:.2f})\n")
            else:
                f.write(f"  {r['codigo']}: {r['status']}\n")

    print(f"✅ Resumen texto: {resumen_path}")
    print()
    print("=" * 70)
    print("✅ VALIDACIÓN COMPLETADA")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python validar_lote_turismo.py <documentos_dir> [normativa_path] [output_dir]")
        print()
        print("Ejemplo:")
        print("  python scripts/validar_lote_turismo.py \\")
        print("    output/Reporte_DPP_21_000_03-11-2025_TURISMO_SC_niveles_G_H_J_K/documentos")
        sys.exit(1)

    documentos_dir = sys.argv[1]

    # Normativa por defecto
    normativa_path = sys.argv[2] if len(sys.argv) > 2 else \
        "validación comparativa con otras URs/REGLAMENTO Interior de la Secretaría de Turismo.txt"

    # Output por defecto
    output_dir = sys.argv[3] if len(sys.argv) > 3 else \
        str(Path(documentos_dir).parent / "validaciones")

    validar_lote_turismo(documentos_dir, normativa_path, output_dir)
