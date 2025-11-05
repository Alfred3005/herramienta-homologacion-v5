"""
Ejemplo Simplificado: Sistema de 3 Criterios con Matriz 2-of-3

Demuestra cómo funcionará la integración completa:
- Criterio 1: Verbos Débiles (threshold 50%)
- Criterio 2: Validación Contextual (referencias institucionales)
- Criterio 3: Apropiación de Impacto Jerárquico (NUEVO)
- Decisión Final: Matriz 2-of-3

Fecha: 2025-11-05
Versión: 5.0
"""

import sys
from pathlib import Path

# Agregar src al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.config.verb_hierarchy import (
    get_level_profile,
    get_expected_impact_profile,
    is_verb_appropriate,
    is_verb_forbidden
)
from src.validators.impact_analyzer import ImpactAnalyzer
from src.validators.models import (
    Criterion1Result,
    Criterion2Result,
    Criterion3Result,
    FunctionImpactAnalysis,
    ValidationResult,
    ValidationSeverity,
    calculate_final_decision,
    create_flag
)


# ==========================================
# DATOS DE EJEMPLO: Puesto Director (M1)
# ==========================================

PUESTO_EJEMPLO = {
    "codigo": "21-F00-1-CFMA001-0000016-E-C-D",
    "denominacion": "DIRECTOR DE ANÁLISIS DE INFORMACIÓN",
    "nivel_salarial": "M1",
    "unidad_responsable": "21 - TURISMO",
    "funciones": [
        {
            "id": "F001",
            "descripcion_completa": "Coordinar la elaboración de análisis estadísticos del sector turístico",
            "que_hace": "Coordinar la elaboración",
            "para_que_lo_hace": "para proporcionar información estratégica a la Secretaría"
        },
        {
            "id": "F002",
            "descripcion_completa": "Supervisar el equipo de analistas de datos",
            "que_hace": "Supervisar el equipo",
            "para_que_lo_hace": "para asegurar la calidad de los reportes"
        },
        {
            "id": "F003",
            "descripcion_completa": "Aprobar la asignación de recursos para proyectos a nivel federal",
            "que_hace": "Aprobar la asignación",
            "para_que_lo_hace": "para garantizar recursos a nivel federal"
        },
        # ↑ Esta función tiene PROBLEMA: alcance "strategic_national" pero puesto es M1 (institutional)
        {
            "id": "F004",
            "descripcion_completa": "Coadyuvar en las actividades administrativas del departamento",
            "que_hace": "Coadyuvar",
            "para_que_lo_hace": "para apoyar las operaciones diarias"
        }
        # ↑ Esta función tiene VERBO DÉBIL: "coadyuvar"
    ]
}


# ==========================================
# SIMULACIÓN DE CRITERIOS
# ==========================================

def simular_criterio_1_verbos_debiles(puesto: dict) -> Criterion1Result:
    """
    Simula evaluación de Criterio 1: Verbos Débiles

    Threshold: >50% funciones con verbos CRÍTICOS → FAIL
    """
    print("\n" + "="*80)
    print("CRITERIO 1: CONGRUENCIA DE VERBOS DÉBILES")
    print("="*80)

    functions = puesto["funciones"]
    total_functions = len(functions)
    critical_count = 0

    # Simular detección de verbos débiles
    verbos_debiles = ["coadyuvar", "apoyar", "auxiliar", "gestionar"]

    for func in functions:
        que_hace = func["que_hace"].lower()
        es_debil = any(verbo in que_hace for verbo in verbos_debiles)

        if es_debil:
            critical_count += 1
            print(f"  ❌ {func['id']}: Verbo débil detectado - '{func['que_hace']}'")
        else:
            print(f"  ✅ {func['id']}: OK - '{func['que_hace']}'")

    critical_rate = critical_count / total_functions
    is_passing = critical_rate <= 0.50

    print(f"\n  📊 Resultado: {critical_count}/{total_functions} funciones con verbos débiles ({critical_rate:.0%})")
    print(f"  🎯 Threshold: 50%")
    print(f"  {'✅ PASS' if is_passing else '❌ FAIL'}: Criterio 1")

    return Criterion1Result(
        result=ValidationResult.PASS if is_passing else ValidationResult.FAIL,
        total_functions=total_functions,
        functions_critical=critical_count,
        critical_rate=critical_rate,
        confidence=0.85,
        reasoning=f"Tasa de verbos débiles: {critical_rate:.0%} {'≤' if is_passing else '>'} 50%"
    )


def simular_criterio_2_contextual(puesto: dict) -> Criterion2Result:
    """
    Simula evaluación de Criterio 2: Validación Contextual

    Verifica referencias institucionales coherentes
    """
    print("\n" + "="*80)
    print("CRITERIO 2: VALIDACIÓN CONTEXTUAL")
    print("="*80)

    # Simular: referencias institucionales coinciden (TURISMO mencionado)
    instituciones_mencionadas = ["secretaría", "turismo", "dirección"]
    instituciones_normativa = ["turismo", "secretaría de turismo"]

    match = any(inst in str(puesto).lower() for inst in instituciones_normativa)

    print(f"  🏛️  Institución del puesto: {puesto['unidad_responsable']}")
    print(f"  📄 Referencias encontradas: {instituciones_mencionadas}")
    print(f"  {'✅' if match else '❌'} Coincidencia con normativa")

    is_passing = match

    print(f"\n  {'✅ PASS' if is_passing else '❌ FAIL'}: Criterio 2")

    return Criterion2Result(
        result=ValidationResult.PASS if is_passing else ValidationResult.FAIL,
        institutional_references_match=match,
        alignment_classification="ALIGNED" if match else "NOT_ALIGNED",
        alignment_confidence=0.90 if match else 0.30,
        reasoning=f"Referencias institucionales {'coinciden' if match else 'NO coinciden'}"
    )


def simular_criterio_3_impacto_jerarquico(puesto: dict) -> Criterion3Result:
    """
    Simula evaluación de Criterio 3: Apropiación de Impacto Jerárquico

    Este es el NUEVO criterio que combina:
    1. Verbos apropiados por nivel
    2. Impacto coherente con nivel
    3. Validación normativa de discrepancias
    """
    print("\n" + "="*80)
    print("CRITERIO 3: APROPIACIÓN DE IMPACTO JERÁRQUICO")
    print("="*80)

    nivel = puesto["nivel_salarial"]
    functions = puesto["funciones"]

    # Obtener perfil esperado
    profile = get_level_profile(nivel)
    expected_impact = get_expected_impact_profile(nivel)

    print(f"  📊 Nivel: {nivel} - {profile.get('level_name', '')}")
    print(f"  🎯 Perfil esperado:")
    print(f"     • Alcance: {expected_impact.get('decision_scope')}")
    print(f"     • Consecuencias: {expected_impact.get('error_consequences')}")
    print(f"     • Complejidad: {expected_impact.get('complexity_level')}")

    # Inicializar analizador
    analyzer = ImpactAnalyzer()

    function_analyses = []
    critical_count = 0
    moderate_count = 0

    print(f"\n  🔍 Análisis por función:")

    for func in functions:
        func_id = func["id"]
        que_hace = func["que_hace"]
        para_que = func["para_que_lo_hace"]

        # Extraer verbo
        verbo = analyzer.extract_main_verb(que_hace)

        # Verificar apropiación
        es_apropiado = is_verb_appropriate(verbo, nivel)
        es_prohibido = is_verb_forbidden(verbo, nivel)

        # Analizar impacto
        impact = analyzer.analyze_single_function(func)

        # Evaluar coherencia de alcance
        scope_eval = analyzer.evaluate_scope_coherence(
            impact.detected_scope,
            expected_impact.get("decision_scope", "institutional"),
            nivel
        )

        # Evaluar coherencia de consecuencias
        cons_eval = analyzer.evaluate_consequences_coherence(
            impact.detected_consequences,
            expected_impact.get("error_consequences", "tactical"),
            nivel
        )

        # Determinar si hay discrepancia
        has_discrepancy = (
            es_prohibido or
            not es_apropiado or
            not scope_eval.is_coherent or
            not cons_eval.is_coherent
        )

        # Simular búsqueda de respaldo normativo
        normative_backing = None
        severity = ValidationSeverity.NONE

        if has_discrepancy:
            # Simular: solo F003 tiene problema SIN respaldo
            if func_id == "F003":
                # Alcance "strategic_national" para nivel M1 (institutional) → SIN RESPALDO
                severity = ValidationSeverity.CRITICAL
                issue = f"Alcance '{impact.detected_scope}' no coherente con nivel {nivel}"
                print(f"     ❌ {func_id}: {issue} (SIN respaldo normativo)")
                critical_count += 1
            else:
                # Otros problemas tienen respaldo (simulado)
                severity = ValidationSeverity.MODERATE
                normative_backing = "Artículo 15, fracción III (simulado)"
                print(f"     ⚠️  {func_id}: Discrepancia detectada pero CON respaldo normativo")
                moderate_count += 1
        else:
            print(f"     ✅ {func_id}: Verbo '{verbo}' apropiado, impacto coherente")

        # Crear análisis
        analysis = FunctionImpactAnalysis(
            funcion_id=func_id,
            descripcion=func["descripcion_completa"],
            que_hace=que_hace,
            para_que_lo_hace=para_que,
            verbo_principal=verbo,
            es_verbo_apropiado=es_apropiado,
            es_verbo_prohibido=es_prohibido,
            detected_scope=impact.detected_scope,
            detected_consequences=impact.detected_consequences,
            detected_complexity=impact.detected_complexity,
            scope_coherent=scope_eval.is_coherent,
            consequences_coherent=cons_eval.is_coherent,
            normative_backing=normative_backing,
            severity=severity,
            issue_detected=issue if has_discrepancy and severity == ValidationSeverity.CRITICAL else None
        )

        function_analyses.append(analysis)

    # Calcular threshold
    total_functions = len(functions)
    critical_rate = critical_count / total_functions if total_functions > 0 else 0.0

    is_passing = critical_rate <= 0.50

    print(f"\n  📊 Resultado:")
    print(f"     • CRITICAL (sin respaldo): {critical_count}/{total_functions} ({critical_rate:.0%})")
    print(f"     • MODERATE (con respaldo): {moderate_count}/{total_functions}")
    print(f"     • Threshold: 50%")
    print(f"  {'✅ PASS' if is_passing else '❌ FAIL'}: Criterio 3")

    return Criterion3Result(
        result=ValidationResult.PASS if is_passing else ValidationResult.FAIL,
        total_functions=total_functions,
        functions_critical=critical_count,
        functions_moderate=moderate_count,
        critical_rate=critical_rate,
        function_analyses=function_analyses,
        confidence=0.80,
        reasoning=f"Tasa de funciones CRÍTICAS: {critical_rate:.0%} {'≤' if is_passing else '>'} 50%"
    )


# ==========================================
# DECISIÓN FINAL: MATRIZ 2-of-3
# ==========================================

def ejecutar_ejemplo_completo():
    """Ejecuta el ejemplo completo del sistema de 3 criterios"""

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  SISTEMA DE HOMOLOGACIÓN APF v5.0 - EJEMPLO SIMPLIFICADO".center(78) + "█")
    print("█" + "  Matriz de Decisión 2-of-3 Criterios".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    print(f"\n📄 Puesto: {PUESTO_EJEMPLO['denominacion']}")
    print(f"🏷️  Código: {PUESTO_EJEMPLO['codigo']}")
    print(f"📊 Nivel: {PUESTO_EJEMPLO['nivel_salarial']}")
    print(f"🏢 UR: {PUESTO_EJEMPLO['unidad_responsable']}")
    print(f"📝 Funciones: {len(PUESTO_EJEMPLO['funciones'])}")

    # Evaluar los 3 criterios
    criterion_1 = simular_criterio_1_verbos_debiles(PUESTO_EJEMPLO)
    criterion_2 = simular_criterio_2_contextual(PUESTO_EJEMPLO)
    criterion_3 = simular_criterio_3_impacto_jerarquico(PUESTO_EJEMPLO)

    # Calcular decisión final
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

    # Explicar la decisión
    print(f"\n  💡 Explicación:")
    for line in final_decision.reasoning.split('\n'):
        print(f"     {line}")

    # Resumen de flags
    critical_flags = [f for f in final_decision.all_flags if f.severity == ValidationSeverity.CRITICAL]
    moderate_flags = [f for f in final_decision.all_flags if f.severity == ValidationSeverity.MODERATE]

    print(f"\n  🚩 Flags Detectados:")
    print(f"     • CRITICAL: {len(critical_flags)}")
    print(f"     • MODERATE: {len(moderate_flags)}")

    # Ejemplo de salida estructurada
    print("\n" + "="*80)
    print("EJEMPLO DE SALIDA JSON")
    print("="*80)

    output_json = {
        "puesto": {
            "codigo": PUESTO_EJEMPLO["codigo"],
            "denominacion": PUESTO_EJEMPLO["denominacion"],
            "nivel": PUESTO_EJEMPLO["nivel_salarial"]
        },
        "validacion": {
            "resultado": final_decision.resultado,
            "clasificacion": final_decision.clasificacion.value,
            "criterios_aprobados": final_decision.criteria_passed,
            "confianza": round(final_decision.confidence_global, 2),
            "criterios": {
                "criterio_1_verbos": {
                    "resultado": criterion_1.result.value,
                    "tasa_critica": round(criterion_1.critical_rate, 2),
                    "threshold": criterion_1.threshold
                },
                "criterio_2_contextual": {
                    "resultado": criterion_2.result.value,
                    "referencias_coinciden": criterion_2.institutional_references_match,
                    "alineacion": criterion_2.alignment_classification
                },
                "criterio_3_impacto": {
                    "resultado": criterion_3.result.value,
                    "tasa_critica": round(criterion_3.critical_rate, 2),
                    "threshold": criterion_3.threshold,
                    "funciones_critical": criterion_3.functions_critical,
                    "funciones_moderate": criterion_3.functions_moderate
                }
            },
            "accion_requerida": final_decision.accion_requerida
        }
    }

    import json
    print(json.dumps(output_json, indent=2, ensure_ascii=False))

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  FIN DEL EJEMPLO".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80 + "\n")


if __name__ == "__main__":
    ejecutar_ejemplo_completo()
