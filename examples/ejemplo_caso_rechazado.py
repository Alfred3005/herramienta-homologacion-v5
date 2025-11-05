"""
Ejemplo: Caso RECHAZADO - Falla 2 de 3 criterios

Demuestra un puesto que NO pasa la validación porque
falla 2 criterios (solo 1 de 3 PASS).

Fecha: 2025-11-05
Versión: 5.0
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from examples.ejemplo_sistema_3_criterios import (
    simular_criterio_1_verbos_debiles,
    simular_criterio_2_contextual,
    simular_criterio_3_impacto_jerarquico
)
from src.validators.models import calculate_final_decision


# ==========================================
# PUESTO PROBLEMÁTICO: Muchos verbos débiles + impacto incoherente
# ==========================================

PUESTO_RECHAZADO = {
    "codigo": "21-F00-1-CFMA001-0000099-E-C-D",
    "denominacion": "JEFE DE DEPARTAMENTO DE ESTRATEGIA NACIONAL",
    "nivel_salarial": "O21",  # ← Jefe Departamento (bajo)
    "unidad_responsable": "21 - TURISMO",
    "funciones": [
        {
            "id": "F001",
            "descripcion_completa": "Coadyuvar en el diseño de políticas nacionales de turismo",
            "que_hace": "Coadyuvar en el diseño",  # ← VERBO DÉBIL
            "para_que_lo_hace": "para apoyar la estrategia del país"  # ← Alcance demasiado alto
        },
        {
            "id": "F002",
            "que_hace": "Apoyar la elaboración",  # ← VERBO DÉBIL
            "para_que_lo_hace": "para garantizar recursos a nivel federal"  # ← Alcance muy alto
        },
        {
            "id": "F003",
            "descripcion_completa": "Auxiliar en la coordinación interinstitucional con otras secretarías",
            "que_hace": "Auxiliar en la coordinación",  # ← VERBO DÉBIL
            "para_que_lo_hace": "para alinear estrategias a nivel república"  # ← Alcance muy alto
        },
        {
            "id": "F004",
            "descripcion_completa": "Gestionar las relaciones internacionales del sector turístico",
            "que_hace": "Gestionar las relaciones",  # ← VERBO DÉBIL + verbo inapropiado para O
            "para_que_lo_hace": "para posicionar al país en el mercado global"  # ← Alcance muy alto
        },
        {
            "id": "F005",
            "descripcion_completa": "Procurar el cumplimiento de normativas internacionales",
            "que_hace": "Procurar el cumplimiento",  # ← VERBO DÉBIL
            "para_que_lo_hace": "para alinear con estándares globales"
        }
        # 5 de 5 funciones tienen verbos débiles → 100% > 50% → FAIL Criterio 1
        # Alcance "strategic_national" pero nivel O (local) → FAIL Criterio 3
    ]
}


def ejecutar_ejemplo_rechazado():
    """Ejecuta ejemplo de puesto RECHAZADO"""

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  EJEMPLO: CASO RECHAZADO (Falla 2 de 3 Criterios)".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    print(f"\n📄 Puesto: {PUESTO_RECHAZADO['denominacion']}")
    print(f"🏷️  Código: {PUESTO_RECHAZADO['codigo']}")
    print(f"📊 Nivel: {PUESTO_RECHAZADO['nivel_salarial']} (Jefe de Departamento)")
    print(f"🏢 UR: {PUESTO_RECHAZADO['unidad_responsable']}")
    print(f"📝 Funciones: {len(PUESTO_RECHAZADO['funciones'])}")

    print(f"\n⚠️  Problemas esperados:")
    print(f"   • TODAS las funciones tienen verbos débiles (100% > 50%)")
    print(f"   • Alcance 'strategic_national' pero puesto es nivel O (local)")
    print(f"   • Funciones propias de Secretario/Subsecretario, no de Jefe Depto")

    # Evaluar criterios
    criterion_1 = simular_criterio_1_verbos_debiles(PUESTO_RECHAZADO)
    criterion_2 = simular_criterio_2_contextual(PUESTO_RECHAZADO)
    criterion_3 = simular_criterio_3_impacto_jerarquico(PUESTO_RECHAZADO)

    # Decisión final
    print("\n" + "="*80)
    print("DECISIÓN FINAL: MATRIZ 2-of-3")
    print("="*80)

    final_decision = calculate_final_decision(criterion_1, criterion_2, criterion_3)

    print(f"\n  📊 Criterios Aprobados: {final_decision.criteria_passed}/3")
    print(f"     • Criterio 1 (Verbos): {criterion_1.result.value}")
    print(f"     • Criterio 2 (Contextual): {criterion_2.result.value}")
    print(f"     • Criterio 3 (Impacto): {criterion_3.result.value}")

    print(f"\n  🎯 Resultado: {final_decision.resultado}")
    print(f"  🏆 Clasificación: {final_decision.clasificacion.value}")
    print(f"  📋 Acción: {final_decision.accion_requerida}")
    print(f"  💯 Confianza Global: {final_decision.confidence_global:.0%}")

    print(f"\n  💡 Explicación:")
    for line in final_decision.reasoning.split('\n'):
        print(f"     {line}")

    # Diagnóstico detallado
    print(f"\n" + "="*80)
    print("DIAGNÓSTICO DETALLADO")
    print("="*80)

    if criterion_1.result.value == "FAIL":
        print(f"\n  ❌ CRITERIO 1 FALLIDO:")
        print(f"     • {criterion_1.functions_critical}/{criterion_1.total_functions} funciones con verbos débiles ({criterion_1.critical_rate:.0%})")
        print(f"     • Threshold máximo: 50%")
        print(f"     • Exceso: {(criterion_1.critical_rate - 0.50):.0%}")

    if criterion_3.result.value == "FAIL":
        print(f"\n  ❌ CRITERIO 3 FALLIDO:")
        print(f"     • {criterion_3.functions_critical}/{criterion_3.total_functions} funciones CRÍTICAS ({criterion_3.critical_rate:.0%})")
        print(f"     • Threshold máximo: 50%")
        print(f"     • Problema: Funciones con alcance/impacto NO coherente con nivel jerárquico")
        print(f"     • Sin respaldo normativo para las discrepancias detectadas")

    print(f"\n  ✅ CRITERIO 2 APROBADO:")
    print(f"     • Referencias institucionales coinciden")
    print(f"     • Puesto pertenece a TURISMO, normativa es de TURISMO")

    print(f"\n  🔧 Recomendaciones:")
    print(f"     1. Reemplazar verbos débiles (coadyuvar, apoyar, auxiliar, gestionar)")
    print(f"     2. Ajustar alcance de funciones a nivel departamental (local)")
    print(f"     3. Funciones apropiadas para O: ejecutar, elaborar, supervisar, analizar")
    print(f"     4. Eliminar referencias a 'nacional', 'república', 'internacional', 'global'")
    print(f"     5. Enfocarse en operaciones del departamento, no estrategias nacionales")

    print("\n" + "█"*80 + "\n")


if __name__ == "__main__":
    ejecutar_ejemplo_rechazado()
