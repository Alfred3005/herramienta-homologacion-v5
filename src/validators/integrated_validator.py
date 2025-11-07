"""
Validador Integrado - Sistema Completo de 3 Criterios

Orquesta la validación completa de un puesto usando:
- Criterio 1: Congruencia de Verbos Débiles (CON LLM)
- Criterio 2: Validación Contextual (Referencias Institucionales CON LLM)
- Criterio 3: Apropiación de Impacto Jerárquico

Decisión Final: Matriz 2-of-3

Fecha: 2025-11-06
Versión: 5.0 - ADAPTADO CON VALIDADORES LLM DE V4
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from src.validators.criterion_3_validator import Criterion3Validator
from src.validators.contextual_verb_validator import ContextualVerbValidator
from src.validators.verb_semantic_analyzer import VerbSemanticAnalyzer
from src.validators.shared_utilities import APFContext
from src.validators.in_memory_normativa_adapter import create_loader_from_fragments
from src.validators.models import (
    Criterion1Result,
    Criterion2Result,
    Criterion3Result,
    FinalDecision,
    ValidationResult,
    calculate_final_decision
)

logger = logging.getLogger(__name__)


class IntegratedValidator:
    """
    Validador integrado que ejecuta los 3 criterios y calcula decisión final.

    VERSIÓN ADAPTADA: Usa validadores LLM reales de v4 para Criterio 1 y 2.
    """

    def __init__(
        self,
        normativa_fragments: Optional[List[str]] = None,
        openai_api_key: Optional[str] = None
    ):
        """
        Inicializa el validador integrado.

        Args:
            normativa_fragments: Fragmentos de normativa para validación
            openai_api_key: API key de OpenAI (para validadores LLM)
        """
        self.normativa_fragments = normativa_fragments or []
        self.openai_api_key = openai_api_key

        # Crear contexto APF para validadores v4
        self.context = APFContext()
        if openai_api_key:
            self.context.set_data('openai_api_key', openai_api_key, 'IntegratedValidator')
            self.context.set_data('api_key', openai_api_key, 'IntegratedValidator')

        # Crear NormativaLoader en memoria si hay fragmentos
        normativa_loader = None
        if normativa_fragments:
            try:
                logger.info(f"[IntegratedValidator] Creando NormativaLoader con {len(normativa_fragments)} fragmentos")
                normativa_loader = create_loader_from_fragments(
                    text_fragments=normativa_fragments,
                    document_title="Reglamento Interior",
                    use_embeddings=False,  # Deshabilitado por ahora para rapidez
                    context=self.context
                )
                logger.info("[IntegratedValidator] NormativaLoader creado exitosamente")
            except Exception as e:
                logger.error(f"[IntegratedValidator] Error creando NormativaLoader: {e}")
                normativa_loader = None

        # Inicializar validadores LLM de v4
        self.verb_analyzer = VerbSemanticAnalyzer(context=self.context)
        self.contextual_validator = ContextualVerbValidator(
            normativa_loader=normativa_loader,
            context=self.context
        )

        # Inicializar Criterion3Validator (ya existente en v5)
        self.criterion3_validator = Criterion3Validator(
            normativa_fragments=normativa_fragments,
            threshold=0.50
        )

        logger.info("[IntegratedValidator] Inicializado con validadores LLM v4")

    def validate_puesto(
        self,
        puesto_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Valida un puesto completo usando los 3 criterios.

        Args:
            puesto_data: Diccionario con datos del puesto
                {
                    "codigo": str,
                    "denominacion": str,
                    "nivel_salarial": str,
                    "unidad_responsable": str,
                    "funciones": List[Dict]
                }

        Returns:
            Diccionario con resultados completos de validación
        """
        codigo = puesto_data.get("codigo", "UNKNOWN")
        nivel = puesto_data.get("nivel_salarial", "P")
        funciones = puesto_data.get("funciones", [])

        logger.info(f"[IntegratedValidator] Validando puesto {codigo}")

        # Ejecutar 3 criterios CON LLM
        criterion_1 = self._validate_criterion_1(codigo, funciones, nivel)
        criterion_2 = self._validate_criterion_2(codigo, puesto_data)
        criterion_3 = self.criterion3_validator.validate(
            puesto_codigo=codigo,
            nivel_salarial=nivel,
            funciones=funciones
        )

        # Calcular decisión final
        final_decision = calculate_final_decision(
            criterion_1,
            criterion_2,
            criterion_3
        )

        # Construir resultado
        result = {
            "puesto": {
                "codigo": codigo,
                "denominacion": puesto_data.get("denominacion", ""),
                "nivel": nivel,
                "unidad_responsable": puesto_data.get("unidad_responsable", "")
            },
            "validacion": {
                "resultado": final_decision.resultado,
                "clasificacion": final_decision.clasificacion.value,
                "criterios_aprobados": final_decision.criteria_passed,
                "confianza": round(final_decision.confidence_global, 2),
                "criterios": {
                    "criterio_1_verbos": self._format_criterion_1(criterion_1),
                    "criterio_2_contextual": self._format_criterion_2(criterion_2),
                    "criterio_3_impacto": self._format_criterion_3(criterion_3)
                },
                "accion_requerida": final_decision.accion_requerida,
                "razonamiento": final_decision.reasoning
            }
        }

        return result

    def _validate_criterion_1(
        self,
        codigo: str,
        funciones: List[Dict[str, Any]],
        nivel_salarial: str = "P"
    ) -> Criterion1Result:
        """
        Valida Criterio 1: Congruencia de Verbos Débiles.

        VERSIÓN LLM: Usa VerbSemanticAnalyzer de v4 con análisis LLM real.

        Args:
            codigo: Código del puesto
            funciones: Lista de funciones
            nivel_salarial: Nivel jerárquico del puesto

        Returns:
            Criterion1Result
        """
        logger.info(f"[Criterio 1 LLM] Validando puesto {codigo} (nivel {nivel_salarial})")

        total_functions = len(funciones)
        critical_count = 0
        moderate_count = 0
        weak_verbs_detected = []

        # Analizar cada función con LLM
        for func in funciones:
            verbo = func.get("verbo_accion", "").strip()
            if not verbo:
                # Fallback: extraer primer verbo de descripción
                desc = func.get("descripcion_completa", "") or func.get("que_hace", "")
                if desc:
                    verbo = desc.split()[0] if desc.split() else ""

            if verbo:
                try:
                    # Llamar a verb_analyzer con LLM
                    analysis = self.verb_analyzer.analyze_verb_for_level(
                        verb=verbo,
                        nivel_jerarquico=nivel_salarial[0] if nivel_salarial else "P",
                        normativa_context=None
                    )

                    # Contar según severidad
                    # Nota: VerbAnalysisResult usa 'is_weak' no 'is_weak_verb'
                    if analysis.is_weak:
                        weak_verbs_detected.append(verbo)
                        # Si tiene respaldo normativo, es MODERATE, sino CRITICAL
                        # Verificar si viene de normativa o tiene confianza alta y es apropiado
                        if (analysis.source == "normativa" or
                            (analysis.is_appropriate and analysis.confidence > 0.7)):
                            moderate_count += 1
                        else:
                            critical_count += 1

                except Exception as e:
                    logger.warning(f"[Criterio 1 LLM] Error analizando verbo '{verbo}': {e}")
                    # Fallback: asumir verbo débil crítico
                    critical_count += 1
                    weak_verbs_detected.append(verbo)

        # Calcular tasa de fallo (solo CRITICAL cuenta)
        critical_rate = critical_count / total_functions if total_functions > 0 else 0.0
        is_passing = critical_rate <= 0.50  # Umbral del 50%

        logger.info(
            f"[Criterio 1 LLM] Verbos débiles: {len(weak_verbs_detected)}, "
            f"CRITICAL: {critical_count}, MODERATE: {moderate_count}, "
            f"Tasa crítica: {critical_rate:.0%} ({'PASS' if is_passing else 'FAIL'})"
        )

        return Criterion1Result(
            result=ValidationResult.PASS if is_passing else ValidationResult.FAIL,
            total_functions=total_functions,
            functions_critical=critical_count,
            functions_moderate=moderate_count,
            critical_rate=critical_rate,
            confidence=0.90,  # Mayor confianza con LLM
            reasoning=f"Análisis LLM: {critical_count} funciones CRÍTICAS de {total_functions} "
                     f"({critical_rate:.0%}). Umbral: 50%"
        )

    def _validate_criterion_2(
        self,
        codigo: str,
        puesto_data: Dict[str, Any]
    ) -> Criterion2Result:
        """
        Valida Criterio 2: Validación Contextual.

        VERSIÓN LLM: Usa ContextualVerbValidator de v4 con análisis LLM real.

        Args:
            codigo: Código del puesto
            puesto_data: Datos del puesto

        Returns:
            Criterion2Result
        """
        logger.info(f"[Criterio 2 LLM] Validando puesto {codigo}")

        # Extraer datos del puesto
        denominacion = puesto_data.get("denominacion", "")
        objetivo = puesto_data.get("objetivo_general", "")
        funciones = puesto_data.get("funciones", [])
        nivel = puesto_data.get("nivel_salarial", "P")

        # Detectar verbos débiles para pasar al validador contextual
        weak_verbs = []
        for func in funciones:
            verbo = func.get("verbo_accion", "").strip()
            if verbo:
                weak_verbs.append(verbo)

        try:
            # Llamar a contextual_validator con LLM
            validation_result = self.contextual_validator.validate_global(
                puesto_nombre=denominacion,
                objetivo_general=objetivo,
                funciones=funciones,
                nivel_jerarquico=nivel[0] if nivel else "P",
                weak_verbs_detected=weak_verbs
            )

            # Mapear resultado de v4 a Criterion2Result de v5
            alignment = validation_result.alignment_level.upper()
            is_aligned = alignment in ["ALIGNED", "PARTIALLY_ALIGNED"]

            logger.info(
                f"[Criterio 2 LLM] Alineación: {alignment}, "
                f"Confianza: {validation_result.confidence:.2f}, "
                f"Resultado: {'PASS' if is_aligned else 'FAIL'}"
            )

            return Criterion2Result(
                result=ValidationResult.PASS if is_aligned else ValidationResult.FAIL,
                institutional_references_match=validation_result.institutional_references_match,
                alignment_classification=alignment,
                alignment_confidence=validation_result.confidence,
                reasoning=validation_result.reasoning or f"Análisis LLM: {alignment}"
            )

        except Exception as e:
            logger.error(f"[Criterio 2 LLM] Error en validación: {e}")
            # Fallback: rechazar con baja confianza
            return Criterion2Result(
                result=ValidationResult.FAIL,
                institutional_references_match=False,
                alignment_classification="ERROR",
                alignment_confidence=0.30,
                reasoning=f"Error en validación LLM: {str(e)}"
            )

    def _format_criterion_1(self, criterion: Criterion1Result) -> Dict[str, Any]:
        """Formatea resultado de Criterio 1 para JSON"""
        return {
            "resultado": criterion.result.value,
            "tasa_critica": round(criterion.critical_rate, 2),
            "threshold": criterion.threshold,
            "funciones_critical": criterion.functions_critical,
            "total_funciones": criterion.total_functions
        }

    def _format_criterion_2(self, criterion: Criterion2Result) -> Dict[str, Any]:
        """Formatea resultado de Criterio 2 para JSON"""
        return {
            "resultado": criterion.result.value,
            "referencias_coinciden": criterion.institutional_references_match,
            "alineacion": criterion.alignment_classification,
            "confianza": round(criterion.alignment_confidence, 2)
        }

    def _format_criterion_3(self, criterion: Criterion3Result) -> Dict[str, Any]:
        """Formatea resultado de Criterio 3 para JSON"""
        return {
            "resultado": criterion.result.value,
            "tasa_critica": round(criterion.critical_rate, 2),
            "threshold": criterion.threshold,
            "funciones_critical": criterion.functions_critical,
            "funciones_moderate": criterion.functions_moderate,
            "total_funciones": criterion.total_functions
        }

    def validate_batch(
        self,
        puestos: List[Dict[str, Any]],
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Valida múltiples puestos en lote.

        Args:
            puestos: Lista de puestos a validar
            progress_callback: Callback(progreso_pct) para reportar progreso

        Returns:
            Lista de resultados de validación
        """
        results = []
        total = len(puestos)

        for idx, puesto in enumerate(puestos):
            try:
                result = self.validate_puesto(puesto)
                results.append(result)

                # Reportar progreso
                if progress_callback:
                    progress_pct = int((idx + 1) / total * 100)
                    progress_callback(progress_pct)

            except Exception as e:
                logger.error(f"Error validando puesto {puesto.get('codigo')}: {e}")
                # Agregar resultado de error
                results.append({
                    "puesto": {
                        "codigo": puesto.get("codigo", "UNKNOWN"),
                        "error": str(e)
                    },
                    "validacion": {
                        "resultado": "ERROR",
                        "mensaje": f"Error al procesar: {str(e)}"
                    }
                })

        return results
