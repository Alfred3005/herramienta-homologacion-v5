#!/usr/bin/env python3
"""
Analiza archivos JSON de validación para calcular uso real de tokens.
Extrae métricas de llamadas LLM y genera estadísticas promedio.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
import statistics

def analizar_archivo_validacion(filepath: str) -> Dict[str, Any]:
    """
    Analiza un archivo de validación y extrae métricas de tokens.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extraer información del puesto
        codigo = data.get('codigo', 'UNKNOWN')
        nivel = data.get('nivel', 'UNKNOWN')
        nivel_salarial = data.get('nivel_salarial', nivel)
        num_funciones = len(data.get('funciones', []))

        # Buscar métricas de uso de tokens
        metricas = {
            'codigo': codigo,
            'nivel': nivel_salarial,
            'num_funciones': num_funciones,
            'tokens_input': 0,
            'tokens_output': 0,
            'tokens_total': 0,
            'num_llamadas_llm': 0
        }

        # Buscar en criterios (pueden tener usage info)
        criterios = data.get('criterios', {})

        # Criterio 1: Análisis por función
        if 'criterio_1' in criterios:
            c1 = criterios['criterio_1']
            if 'funciones_analizadas' in c1:
                metricas['num_llamadas_llm'] += len(c1['funciones_analizadas'])

        # Buscar en validaciones_adicionales (v5.33-new)
        if 'validaciones_adicionales' in data:
            # Esto indica que se ejecutó AdvancedQualityValidator
            metricas['num_llamadas_llm'] += 1

        # Buscar usage info en cualquier nivel del JSON
        def buscar_usage(obj, path=""):
            if isinstance(obj, dict):
                if 'usage' in obj:
                    usage = obj['usage']
                    if 'prompt_tokens' in usage:
                        metricas['tokens_input'] += usage.get('prompt_tokens', 0)
                    if 'completion_tokens' in usage:
                        metricas['tokens_output'] += usage.get('completion_tokens', 0)
                    if 'total_tokens' in usage:
                        metricas['tokens_total'] += usage.get('total_tokens', 0)

                for key, value in obj.items():
                    buscar_usage(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    buscar_usage(item, f"{path}[{i}]")

        buscar_usage(data)

        # Si no encontramos tokens_total pero sí input/output, calcularlo
        if metricas['tokens_total'] == 0 and (metricas['tokens_input'] > 0 or metricas['tokens_output'] > 0):
            metricas['tokens_total'] = metricas['tokens_input'] + metricas['tokens_output']

        return metricas

    except Exception as e:
        print(f"Error analizando {filepath}: {e}")
        return None

def main():
    """Analiza todos los archivos de validación disponibles."""

    # Buscar archivos de validación
    base_dir = Path('/home/alfred/herramienta-homologacion-v5')

    # Patrones de búsqueda
    archivos_validacion = list(base_dir.glob('output/analisis/*_validacion.json'))
    archivos_validacion += list(base_dir.glob('streamlit_app/output/analisis/*_validacion.json'))

    print(f"🔍 Encontrados {len(archivos_validacion)} archivos de validación")
    print("-" * 80)

    resultados = []

    for archivo in archivos_validacion:
        metricas = analizar_archivo_validacion(str(archivo))
        if metricas and metricas['tokens_total'] > 0:
            resultados.append(metricas)
            print(f"✅ {metricas['codigo']:<30} | Funciones: {metricas['num_funciones']:>2} | "
                  f"Tokens: {metricas['tokens_total']:>8,} | "
                  f"Input: {metricas['tokens_input']:>7,} | "
                  f"Output: {metricas['tokens_output']:>7,}")

    print("-" * 80)
    print(f"\n📊 ESTADÍSTICAS ({len(resultados)} puestos analizados)")
    print("=" * 80)

    if not resultados:
        print("⚠️  No se encontraron datos de uso de tokens en los archivos.")
        print("   Los archivos pueden no contener información de 'usage'.")
        return

    # Calcular estadísticas
    total_funciones = [r['num_funciones'] for r in resultados]
    total_tokens = [r['tokens_total'] for r in resultados]
    input_tokens = [r['tokens_input'] for r in resultados]
    output_tokens = [r['tokens_output'] for r in resultados]
    llamadas_llm = [r['num_llamadas_llm'] for r in resultados]

    print(f"\n🔢 FUNCIONES POR PUESTO:")
    print(f"   Promedio:  {statistics.mean(total_funciones):.1f}")
    print(f"   Mediana:   {statistics.median(total_funciones):.1f}")
    print(f"   Mínimo:    {min(total_funciones)}")
    print(f"   Máximo:    {max(total_funciones)}")

    print(f"\n💰 TOKENS TOTALES POR PUESTO:")
    print(f"   Promedio:  {statistics.mean(total_tokens):>10,.0f} tokens")
    print(f"   Mediana:   {statistics.median(total_tokens):>10,.0f} tokens")
    print(f"   Mínimo:    {min(total_tokens):>10,} tokens")
    print(f"   Máximo:    {max(total_tokens):>10,} tokens")

    print(f"\n📥 TOKENS INPUT (Prompt):")
    print(f"   Promedio:  {statistics.mean(input_tokens):>10,.0f} tokens")
    print(f"   Total:     {sum(input_tokens):>10,} tokens")

    print(f"\n📤 TOKENS OUTPUT (Completion):")
    print(f"   Promedio:  {statistics.mean(output_tokens):>10,.0f} tokens")
    print(f"   Total:     {sum(output_tokens):>10,} tokens")

    print(f"\n🔄 LLAMADAS LLM:")
    print(f"   Promedio:  {statistics.mean(llamadas_llm):.1f} llamadas/puesto")

    # Calcular costos con diferentes modelos
    avg_input = statistics.mean(input_tokens)
    avg_output = statistics.mean(output_tokens)
    avg_total = statistics.mean(total_tokens)

    print(f"\n💵 COSTO PROMEDIO POR PUESTO:")
    print("-" * 80)

    # Precios (por 1M tokens)
    modelos = [
        ("GPT-4o (actual)", 3.00, 10.00),
        ("GPT-4o-mini", 0.15, 0.60),
        ("GPT-3.5-turbo", 0.50, 1.50),
        ("DeepSeek V3.2-Exp", 0.28, 0.42),
        ("Gemini 2.5 Flash", 0.15, 0.60),
    ]

    costos = []
    for nombre, precio_input, precio_output in modelos:
        costo_in = (avg_input / 1_000_000) * precio_input
        costo_out = (avg_output / 1_000_000) * precio_output
        costo_total = costo_in + costo_out
        costos.append((nombre, costo_total))

        ahorro = ((costos[0][1] - costo_total) / costos[0][1] * 100) if costos else 0
        ahorro_str = f"(-{ahorro:.1f}%)" if ahorro > 0 else ""

        print(f"   {nombre:<25} ${costo_total:>8.4f} {ahorro_str:>10}")

    # Proyección anual
    print(f"\n📅 PROYECCIÓN ANUAL (5,000 puestos):")
    print("-" * 80)
    for nombre, costo in costos:
        costo_anual = costo * 5000
        ahorro_anual = (costos[0][1] - costo) * 5000
        ahorro_pct = ((costos[0][1] - costo) / costos[0][1] * 100) if costos[0][1] > 0 else 0

        if ahorro_anual > 0:
            print(f"   {nombre:<25} ${costo_anual:>10,.2f}/año  (ahorro: ${ahorro_anual:>9,.2f} | {ahorro_pct:.1f}%)")
        else:
            print(f"   {nombre:<25} ${costo_anual:>10,.2f}/año")

    print("\n" + "=" * 80)
    print("✅ Análisis completado")

if __name__ == '__main__':
    main()
