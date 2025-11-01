#!/usr/bin/env python3
"""
Script de Validación v4 vs v5

Compara resultados de extracción entre v4 y v5 para asegurar
que la migración no afectó la funcionalidad ni la calibración.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
import difflib

# Agregar paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import PipelineFactory
from src.core import ExtractionMode


@dataclass
class ComparisonResult:
    """Resultado de comparación entre v4 y v5"""
    file_name: str
    v4_success: bool
    v5_success: bool
    fields_compared: int
    fields_matching: int
    fields_different: int
    match_percentage: float
    differences: List[Dict[str, Any]]
    v4_functions_count: int
    v5_functions_count: int
    v4_has_denominacion: bool
    v5_has_denominacion: bool
    v4_has_nivel: bool
    v5_has_nivel: bool
    notes: List[str]


def load_v4_result(file_path: str) -> Dict[str, Any]:
    """
    Carga resultado de v4 desde JSON.

    Args:
        file_path: Ruta al JSON de resultado v4

    Returns:
        Dict con datos de v4
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error cargando resultado v4: {e}")
        return None


def extract_with_v5(puesto_file: str) -> Dict[str, Any]:
    """
    Ejecuta extracción con v5.

    Args:
        puesto_file: Ruta al archivo del puesto

    Returns:
        Dict con resultado de v5
    """
    try:
        print(f"  🔄 Extrayendo con v5...")
        extractor = PipelineFactory.create_simple_pipeline(
            model="openai/gpt-4o",
            enable_logging=False
        )

        result = extractor.extract_from_file(
            puesto_file,
            mode=ExtractionMode.INTELLIGENT,
            max_tokens=4000,
            temperature=0.1
        )

        return result
    except Exception as e:
        print(f"  ❌ Error en extracción v5: {e}")
        return {"status": "error", "error": str(e)}


def compare_identificacion(v4_data: Dict, v5_data: Dict) -> Dict[str, Any]:
    """Compara sección de identificación"""
    v4_ident = v4_data.get("identificacion_puesto", {})
    v5_ident = v5_data.get("identificacion_puesto", {})

    differences = []

    # Comparar denominación
    v4_denom = v4_ident.get("denominacion_puesto", "")
    v5_denom = v5_ident.get("denominacion_puesto", "")

    if v4_denom != v5_denom:
        similarity = difflib.SequenceMatcher(None, v4_denom, v5_denom).ratio()
        differences.append({
            "field": "identificacion_puesto.denominacion_puesto",
            "v4_value": v4_denom,
            "v5_value": v5_denom,
            "similarity": similarity
        })

    # Comparar código
    v4_codigo = v4_ident.get("codigo_puesto", "")
    v5_codigo = v5_ident.get("codigo_puesto", "")

    if v4_codigo != v5_codigo:
        differences.append({
            "field": "identificacion_puesto.codigo_puesto",
            "v4_value": v4_codigo,
            "v5_value": v5_codigo
        })

    # Comparar nivel salarial
    v4_nivel = v4_ident.get("nivel_salarial", {})
    v5_nivel = v5_ident.get("nivel_salarial", {})

    v4_nivel_codigo = v4_nivel.get("codigo", "") if isinstance(v4_nivel, dict) else ""
    v5_nivel_codigo = v5_nivel.get("codigo", "") if isinstance(v5_nivel, dict) else ""

    if v4_nivel_codigo != v5_nivel_codigo:
        differences.append({
            "field": "identificacion_puesto.nivel_salarial.codigo",
            "v4_value": v4_nivel_codigo,
            "v5_value": v5_nivel_codigo
        })

    return {
        "differences": differences,
        "v4_has_denominacion": bool(v4_denom),
        "v5_has_denominacion": bool(v5_denom),
        "v4_has_nivel": bool(v4_nivel_codigo),
        "v5_has_nivel": bool(v5_nivel_codigo)
    }


def compare_funciones(v4_data: Dict, v5_data: Dict) -> Dict[str, Any]:
    """Compara sección de funciones"""
    v4_funcs = v4_data.get("funciones", [])
    v5_funcs = v5_data.get("funciones", [])

    v4_count = len(v4_funcs)
    v5_count = len(v5_funcs)

    differences = []

    if v4_count != v5_count:
        differences.append({
            "field": "funciones.count",
            "v4_value": v4_count,
            "v5_value": v5_count,
            "difference": abs(v4_count - v5_count)
        })

    # Comparar verbos de acción de primeras 5 funciones
    for i in range(min(5, v4_count, v5_count)):
        v4_verbo = v4_funcs[i].get("verbo_accion", "")
        v5_verbo = v5_funcs[i].get("verbo_accion", "")

        if v4_verbo != v5_verbo:
            differences.append({
                "field": f"funciones[{i}].verbo_accion",
                "v4_value": v4_verbo,
                "v5_value": v5_verbo
            })

    return {
        "v4_count": v4_count,
        "v5_count": v5_count,
        "differences": differences
    }


def compare_results(v4_data: Dict, v5_result: Dict, file_name: str) -> ComparisonResult:
    """
    Compara resultados completos de v4 y v5.

    Args:
        v4_data: Datos de v4
        v5_result: Resultado completo de v5
        file_name: Nombre del archivo

    Returns:
        ComparisonResult con análisis completo
    """
    # Extraer data de v5
    v5_status = v5_result.get("status", "error")
    v5_data = v5_result.get("data", {})

    # Comparar identificación
    ident_comparison = compare_identificacion(v4_data, v5_data)

    # Comparar funciones
    func_comparison = compare_funciones(v4_data, v5_data)

    # Consolidar diferencias
    all_differences = ident_comparison["differences"] + func_comparison["differences"]

    # Calcular métricas
    fields_compared = 5  # denominacion, codigo, nivel, funciones_count, verbos
    fields_different = len(all_differences)
    fields_matching = fields_compared - fields_different
    match_percentage = (fields_matching / fields_compared * 100) if fields_compared > 0 else 0

    # Generar notas
    notes = []

    if v5_status == "success" and not v4_data.get("status"):
        notes.append("✅ v5 extrajo exitosamente")
    elif v5_status != "success":
        notes.append("⚠️ v5 tuvo errores de extracción")

    if func_comparison["v5_count"] > func_comparison["v4_count"]:
        notes.append(f"✅ v5 extrajo más funciones (+{func_comparison['v5_count'] - func_comparison['v4_count']})")
    elif func_comparison["v5_count"] < func_comparison["v4_count"]:
        notes.append(f"⚠️ v5 extrajo menos funciones (-{func_comparison['v4_count'] - func_comparison['v5_count']})")

    if ident_comparison["v5_has_denominacion"] and not ident_comparison["v4_has_denominacion"]:
        notes.append("✅ v5 extrajo denominación (v4 no)")

    return ComparisonResult(
        file_name=file_name,
        v4_success=True,
        v5_success=(v5_status == "success"),
        fields_compared=fields_compared,
        fields_matching=fields_matching,
        fields_different=fields_different,
        match_percentage=match_percentage,
        differences=all_differences,
        v4_functions_count=func_comparison["v4_count"],
        v5_functions_count=func_comparison["v5_count"],
        v4_has_denominacion=ident_comparison["v4_has_denominacion"],
        v5_has_denominacion=ident_comparison["v5_has_denominacion"],
        v4_has_nivel=ident_comparison["v4_has_nivel"],
        v5_has_nivel=ident_comparison["v5_has_nivel"],
        notes=notes
    )


def print_comparison_report(results: List[ComparisonResult]):
    """Imprime reporte de comparación"""
    print("\n" + "=" * 80)
    print("📊 REPORTE DE VALIDACIÓN v4 vs v5")
    print("=" * 80)
    print()

    total_tests = len(results)
    successful_v5 = sum(1 for r in results if r.v5_success)
    avg_match = sum(r.match_percentage for r in results) / total_tests if total_tests > 0 else 0

    print(f"Total de casos: {total_tests}")
    print(f"v5 exitosos: {successful_v5}/{total_tests} ({successful_v5/total_tests*100:.1f}%)")
    print(f"Similitud promedio: {avg_match:.1f}%")
    print()

    print("=" * 80)
    print("Resultados por Caso")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.file_name}")
        print(f"   Estado v5: {'✅ Success' if result.v5_success else '❌ Error'}")
        print(f"   Similitud: {result.match_percentage:.1f}%")
        print(f"   Funciones: v4={result.v4_functions_count}, v5={result.v5_functions_count}")
        print(f"   Campos diferentes: {result.fields_different}/{result.fields_compared}")

        if result.differences:
            print(f"   Diferencias:")
            for diff in result.differences[:3]:  # Mostrar máximo 3
                print(f"     - {diff['field']}: v4='{diff.get('v4_value', 'N/A')}' vs v5='{diff.get('v5_value', 'N/A')}'")
            if len(result.differences) > 3:
                print(f"     ... y {len(result.differences) - 3} más")

        if result.notes:
            print(f"   Notas:")
            for note in result.notes:
                print(f"     {note}")

    print("\n" + "=" * 80)
    print("Conclusiones")
    print("=" * 80)

    if avg_match >= 90:
        print("✅ EXCELENTE: v5 mantiene alta fidelidad con v4 (≥90%)")
    elif avg_match >= 75:
        print("✅ BUENO: v5 es compatible con v4 (≥75%)")
    elif avg_match >= 60:
        print("⚠️ ACEPTABLE: v5 tiene diferencias significativas pero funcional (≥60%)")
    else:
        print("❌ PROBLEMA: v5 tiene divergencia importante de v4 (<60%)")

    print()


def main():
    """Función principal"""
    print("=" * 80)
    print("🧪 Validación v4 vs v5 - Comparación de Resultados")
    print("=" * 80)
    print()

    # Casos de test (ajustar según disponibilidad)
    test_cases = [
        {
            "name": "Puesto SABG 1",
            "v4_result": "../HerramientaHomologaci-nDocker/data/resultados_validacion_sabg/puesto_1_result.json",
            "puesto_file": "../HerramientaHomologaci-nDocker/data/Secretaria Buen Gobierno/Puesto 1 SABG.txt"
        },
        # Agregar más casos según disponibilidad
    ]

    print(f"Casos de test configurados: {len(test_cases)}")
    print()

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Procesando: {test_case['name']}")

        # Verificar que archivos existen
        v4_result_path = Path(test_case['v4_result'])
        puesto_path = Path(test_case['puesto_file'])

        if not v4_result_path.exists():
            print(f"  ⚠️ Resultado v4 no encontrado: {v4_result_path}")
            continue

        if not puesto_path.exists():
            print(f"  ⚠️ Archivo de puesto no encontrado: {puesto_path}")
            continue

        # Cargar resultado v4
        v4_data = load_v4_result(str(v4_result_path))
        if not v4_data:
            continue

        print(f"  ✅ Resultado v4 cargado")

        # Extraer con v5
        v5_result = extract_with_v5(str(puesto_path))

        # Comparar
        comparison = compare_results(v4_data, v5_result, test_case['name'])
        results.append(comparison)

        print(f"  ✅ Comparación completada: {comparison.match_percentage:.1f}% similitud")
        print()

    if not results:
        print("❌ No se pudieron procesar casos de test")
        print()
        print("💡 Configura los casos de test editando el script:")
        print("   - Agrega rutas a resultados v4 (JSON)")
        print("   - Agrega rutas a archivos de puestos")
        return

    # Generar reporte
    print_comparison_report(results)

    # Guardar reporte detallado
    output_file = "validation_v4_vs_v5_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([
            {
                "file_name": r.file_name,
                "match_percentage": r.match_percentage,
                "v5_success": r.v5_success,
                "differences_count": r.fields_different,
                "differences": r.differences,
                "notes": r.notes
            }
            for r in results
        ], f, ensure_ascii=False, indent=2)

    print(f"📄 Reporte detallado guardado en: {output_file}")
    print()


if __name__ == "__main__":
    main()
