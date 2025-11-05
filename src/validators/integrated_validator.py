"""
Validador Integrado - Sistema Completo de 3 Criterios

Orquesta la validación completa de un puesto usando:
- Criterio 1: Congruencia de Verbos Débiles
- Criterio 2: Validación Contextual (Referencias Institucionales)
- Criterio 3: Apropiación de Impacto Jerárquico

Decisión Final: Matriz 2-of-3

Fecha: 2025-11-05
Versión: 5.0
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from src.validators.criterion_3_validator import Criterion3Validator
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

    Este validador simplifica la integración al proveer una interfaz única
    para validar puestos completos.
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
            openai_api_key: API key de OpenAI (para Criterio 2)
        """
        self.normativa_fragments = normativa_fragments or []
        self.openai_api_key = openai_api_key

        # Inicializar Criterion3Validator
        self.criterion3_validator = Criterion3Validator(
            normativa_fragments=normativa_fragments,
            threshold=0.50
        )

        logger.info("[IntegratedValidator] Inicializado correctamente")

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

        # Ejecutar 3 criterios
        criterion_1 = self._validate_criterion_1(codigo, funciones)
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
        funciones: List[Dict[str, Any]]
    ) -> Criterion1Result:
        """
        Valida Criterio 1: Congruencia de Verbos Débiles.

        Esta es una implementación simplificada que detecta verbos débiles
        básicos. En producción, esto podría usar un LLM.

        Args:
            codigo: Código del puesto
            funciones: Lista de funciones

        Returns:
            Criterion1Result
        """
        logger.info(f"[Criterio 1] Validando puesto {codigo}")

        # Verbos débiles básicos
        verbos_debiles = [
            "coadyuvar", "apoyar", "auxiliar", "gestionar",
            "procurar", "colaborar", "contribuir"
        ]

        total_functions = len(funciones)
        critical_count = 0

        for func in funciones:
            que_hace = func.get("que_hace", "").lower()

            # Detectar si tiene verbo débil
            es_debil = any(verbo in que_hace for verbo in verbos_debiles)

            if es_debil:
                critical_count += 1

        critical_rate = critical_count / total_functions if total_functions > 0 else 0.0
        is_passing = critical_rate <= 0.50

        logger.info(
            f"[Criterio 1] Tasa verbos débiles: {critical_rate:.0%} ({'PASS' if is_passing else 'FAIL'})"
        )

        return Criterion1Result(
            result=ValidationResult.PASS if is_passing else ValidationResult.FAIL,
            total_functions=total_functions,
            functions_critical=critical_count,
            critical_rate=critical_rate,
            confidence=0.80,
            reasoning=f"Verbos débiles: {critical_count}/{total_functions} ({critical_rate:.0%})"
        )

    def _validate_criterion_2(
        self,
        codigo: str,
        puesto_data: Dict[str, Any]
    ) -> Criterion2Result:
        """
        Valida Criterio 2: Validación Contextual.

        Implementación simplificada que verifica referencias institucionales
        básicas. En producción, esto usaría LLM para análisis más profundo.

        Args:
            codigo: Código del puesto
            puesto_data: Datos del puesto

        Returns:
            Criterion2Result
        """
        logger.info(f"[Criterio 2] Validando puesto {codigo}")

        # Extraer UR
        ur = puesto_data.get("unidad_responsable", "").lower()

        # Detectar organismo principal
        organismo_principal = None
        if "turismo" in ur:
            organismo_principal = "turismo"
        elif "agricultura" in ur or "sagarpa" in ur:
            organismo_principal = "agricultura"
        elif "salud" in ur:
            organismo_principal = "salud"
        # ... etc

        # Verificar si las funciones mencionan el mismo organismo
        funciones = puesto_data.get("funciones", [])
        texto_funciones = " ".join([
            f.get("descripcion_completa", "") + " " +
            f.get("que_hace", "") + " " +
            f.get("para_que_lo_hace", "")
            for f in funciones
        ]).lower()

        # Validación simple: si encontramos el organismo en funciones, es coherente
        match = organismo_principal is None or organismo_principal in texto_funciones

        logger.info(
            f"[Criterio 2] Referencias institucionales: {'coinciden' if match else 'NO coinciden'}"
        )

        return Criterion2Result(
            result=ValidationResult.PASS if match else ValidationResult.FAIL,
            institutional_references_match=match,
            alignment_classification="ALIGNED" if match else "NOT_ALIGNED",
            alignment_confidence=0.85 if match else 0.30,
            reasoning=f"Referencias institucionales {'coinciden' if match else 'NO coinciden'}"
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
