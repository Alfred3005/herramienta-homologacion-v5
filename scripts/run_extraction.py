#!/usr/bin/env python3
"""
Script de ejemplo para extracción de información de puestos APF

Demuestra cómo usar el sistema de homologación v5.0 con el nuevo
pipeline basado en Dependency Injection.
"""

import sys
import os
import json
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import PipelineFactory
from src.core import ExtractionMode


def main():
    """Función principal"""
    print("=" * 70)
    print("Sistema de Homologación APF v5.0 - Extractor de Puestos")
    print("=" * 70)
    print()

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python run_extraction.py <ruta_archivo_puesto> [modo]")
        print()
        print("Modos disponibles:")
        print("  - fast: Extracción rápida (mínimos campos)")
        print("  - intelligent: Balanceado (recomendado)")
        print("  - thorough: Exhaustivo (máxima precisión)")
        print()
        print("Ejemplo:")
        print("  python run_extraction.py ../data/examples/puesto_ejemplo.pdf intelligent")
        sys.exit(1)

    file_path = sys.argv[1]
    mode_str = sys.argv[2] if len(sys.argv) > 2 else "intelligent"

    # Validar archivo
    if not Path(file_path).exists():
        print(f"❌ Error: Archivo no encontrado: {file_path}")
        sys.exit(1)

    # Parsear modo
    mode_map = {
        "fast": ExtractionMode.FAST,
        "intelligent": ExtractionMode.INTELLIGENT,
        "thorough": ExtractionMode.THOROUGH
    }

    if mode_str not in mode_map:
        print(f"❌ Error: Modo inválido '{mode_str}'")
        print(f"   Modos válidos: {', '.join(mode_map.keys())}")
        sys.exit(1)

    mode = mode_map[mode_str]

    print(f"📄 Archivo: {Path(file_path).name}")
    print(f"🔧 Modo: {mode_str}")
    print()

    # Crear pipeline
    print("🚀 Inicializando pipeline...")
    try:
        extractor = PipelineFactory.create_simple_pipeline(
            model="openai/gpt-4o",
            enable_logging=True
        )
        print("✅ Pipeline inicializado")
        print()
    except Exception as e:
        print(f"❌ Error al inicializar pipeline: {e}")
        print()
        print("💡 Asegúrate de configurar tu API key de OpenAI:")
        print("   export OPENAI_API_KEY='tu_api_key'")
        sys.exit(1)

    # Ejecutar extracción
    print("🔍 Extrayendo información del puesto...")
    print("-" * 70)
    try:
        result = extractor.extract_from_file(
            file_path=file_path,
            mode=mode,
            max_tokens=4000,
            temperature=0.1
        )

        print()
        print("=" * 70)
        print("📊 RESULTADO DE EXTRACCIÓN")
        print("=" * 70)
        print()

        # Mostrar resumen
        status = result['status']
        validation = result['validation']

        if status == "success":
            print("✅ Extracción exitosa")
        else:
            print("⚠️  Extracción parcial (con errores de validación)")

        print()
        print(f"Errores de validación: {validation['error_count']}")
        print(f"Warnings: {validation['warning_count']}")
        print()

        # Mostrar datos extraídos
        data = result['data']

        if 'identificacion_puesto' in data:
            ident = data['identificacion_puesto']
            print("📋 IDENTIFICACIÓN:")
            print(f"  Denominación: {ident.get('denominacion_puesto', 'N/A')}")
            print(f"  Código: {ident.get('codigo_puesto', 'N/A')}")

            if 'nivel_salarial' in ident and ident['nivel_salarial']:
                nivel = ident['nivel_salarial']
                print(f"  Nivel: {nivel.get('codigo', 'N/A')} - {nivel.get('descripcion', 'N/A')}")

            print()

        if 'objetivo_general' in data and data['objetivo_general']:
            obj = data['objetivo_general']
            print("🎯 OBJETIVO GENERAL:")
            desc = obj.get('descripcion_completa', 'N/A')
            print(f"  {desc[:200]}{'...' if len(desc) > 200 else ''}")
            print()

        if 'funciones' in data and data['funciones']:
            print(f"📝 FUNCIONES EXTRAÍDAS: {len(data['funciones'])}")
            for i, func in enumerate(data['funciones'][:5], 1):  # Mostrar máximo 5
                verbo = func.get('verbo_accion', 'N/A')
                desc = func.get('descripcion_completa', 'N/A')
                print(f"  {i}. [{verbo}] {desc[:100]}{'...' if len(desc) > 100 else ''}")

            if len(data['funciones']) > 5:
                print(f"  ... y {len(data['funciones']) - 5} funciones más")
            print()

        # Mostrar issues si hay
        if validation['error_count'] > 0 or validation['warning_count'] > 0:
            print("⚠️  ISSUES ENCONTRADOS:")
            for issue in validation['issues'][:5]:  # Mostrar máximo 5
                severity = issue['severity'].upper()
                field = issue['field']
                message = issue['message']
                print(f"  [{severity}] {field}: {message}")

            if len(validation['issues']) > 5:
                print(f"  ... y {len(validation['issues']) - 5} issues más")
            print()

        # Opción para guardar JSON completo
        print("=" * 70)
        save = input("¿Guardar resultado completo en JSON? (s/n): ")

        if save.lower() == 's':
            output_file = Path(file_path).stem + "_extracted.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ Guardado en: {output_file}")

        print()
        print("✨ Extracción completada")

    except Exception as e:
        print(f"❌ Error durante extracción: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
