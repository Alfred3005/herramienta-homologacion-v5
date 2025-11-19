# -*- coding: utf-8 -*-
"""
CONTEXTUAL VERB VALIDATOR - Validación Inteligente de Verbos con LLM
Sistema de validación con dos modos: HÍBRIDO (rápido) y COMPLETO (detallado)

VERSIÓN 5.41 - Sistema Jerárquico de Herencia Normativa
Mejoras implementadas:
- Identificación inteligente de instituciones (sin hardcoding)
- Sistema de 4 niveles de alineación jerárquica con scores granulares
- Análisis función por función con distancia jerárquica
- Diferenciación entre herencia directa, del jefe directo, y lejana

NIVELES DE ALINEACIÓN:
- NIVEL 1: Alineación Directa (Score: 0.9) - Mismo grupo jerárquico
- NIVEL 2: Herencia del Jefe Directo (Score: 0.75) - Un nivel arriba
- NIVEL 3: Herencia Lejana en Organismo (Score: 0.55) - Varios niveles arriba
- NIVEL 4: No Alineado (Score: 0.0) - Fuera del marco del organismo

MODO HÍBRIDO:
- Validación de umbrales (cantidad de verbos débiles)
- 1 llamada LLM global que valida TODO el puesto vs normativa
- Análisis granular función por función
- Rápido y económico

MODO COMPLETO:
- Validación función por función con contexto normativo
- Validación de herencia jerárquica detallada
- Validación de apropiación de alcance por nivel
- Máxima precisión

Fecha: 2025-11-19
Versión: 5.41 - Sistema Jerárquico de Herencia Normativa
"""

import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

from src.validators.shared_utilities import (
    APFContext, robust_openai_call, VERB_HIERARCHY, WEAK_VERBS,
    LOGGING_CONFIG
)

# ==========================================
# CONFIGURACIÓN
# ==========================================

VALIDATION_CONFIG = {
    # Modo de validación: "HYBRID" o "COMPLETE"
    "validation_mode": "HYBRID",  # Cambiar a "COMPLETE" para modo detallado

    # Umbrales para modo híbrido
    "weak_verb_threshold": 20,  # Máximo de verbos débiles permitidos
    "completeness_min_threshold": 0.5,  # 50% mínimo de funciones esperadas
    "completeness_max_threshold": 2.0,  # 200% máximo (sobrecarga)

    # Configuración LLM
    "llm_temperature": 0.0,  # Determinístico
    "llm_max_tokens": 2000,  # Aumentado para respuesta más detallada
    "use_cache": True
}

# ==========================================
# NIVELES DE ALINEACIÓN JERÁRQUICA (v5.41)
# ==========================================

ALIGNMENT_LEVELS = {
    "NIVEL_1_ALINEACION_DIRECTA": {
        "score": 0.9,
        "descripcion": "Atribución encontrada EXPLÍCITAMENTE en la sección del MISMO grupo jerárquico",
        "distancia_jerarquica": 0,
        "tipo_herencia": "DIRECTA",
        "clasificacion": "STRONGLY_ALIGNED"
    },
    "NIVEL_2_HERENCIA_JEFE_DIRECTO": {
        "score": 0.75,
        "descripcion": "Atribución derivable del JEFE INMEDIATO SUPERIOR (un nivel arriba)",
        "distancia_jerarquica": 1,
        "tipo_herencia": "DIRECTA",
        "clasificacion": "ALIGNED"
    },
    "NIVEL_3_HERENCIA_LEJANA": {
        "score": 0.55,
        "descripcion": "Atribución dentro del MARCO general del organismo (varios niveles arriba)",
        "distancia_jerarquica": 2,  # 2 o más
        "tipo_herencia": "LEJANA",
        "clasificacion": "PARTIALLY_ALIGNED"
    },
    "NIVEL_4_NO_ALINEADO": {
        "score": 0.0,
        "descripcion": "Atribución fuera del marco del organismo",
        "distancia_jerarquica": None,
        "tipo_herencia": "NONE",
        "clasificacion": "NOT_ALIGNED"
    }
}

# Jerarquía de alcance de verbos (de menor a mayor)
ALCANCE_VERBOS = {
    1: {"nivel": "Operativo", "verbos": ["recopilar", "registrar", "archivar", "transcribir"]},
    2: {"nivel": "Técnico", "verbos": ["elaborar", "preparar", "calcular", "procesar"]},
    3: {"nivel": "Supervisión", "verbos": ["verificar", "revisar", "controlar", "validar"]},
    4: {"nivel": "Analítico", "verbos": ["evaluar", "analizar", "diagnosticar", "investigar"]},
    5: {"nivel": "Asesoría", "verbos": ["proponer", "recomendar", "sugerir", "asesorar"]},
    6: {"nivel": "Coordinación", "verbos": ["coordinar", "gestionar", "organizar", "programar"]},
    7: {"nivel": "Gerencial", "verbos": ["administrar", "supervisar", "dirigir equipos", "implementar"]},
    8: {"nivel": "Decisión", "verbos": ["aprobar", "autorizar", "resolver", "decidir"]},
    9: {"nivel": "Estratégico", "verbos": ["dirigir", "establecer", "definir políticas", "planear"]},
    10: {"nivel": "Normativo", "verbos": ["sancionar", "expedir", "decretar", "legislar"]}
}

# Mapeo de niveles jerárquicos a alcances apropiados
NIVEL_TO_ALCANCE = {
    "G11": (7, 10),  # Secretario: Gerencial-Normativo
    "J31": (5, 8),   # Titular OAD: Asesoría-Decisión
    "M1": (4, 7),    # Director: Analítico-Gerencial
    "P3": (1, 5),    # Jefe Depto: Operativo-Asesoría
}

# ==========================================
# CLASES DE DATOS
# ==========================================

@dataclass
class GlobalValidationResult:
    """Resultado de validación global (modo híbrido)

    VERSIÓN 5.41: Incluye análisis detallado función por función con 4 niveles de herencia
    """
    is_aligned: bool  # ¿Está alineado con normativa?
    alignment_level: str  # "ALIGNED" | "PARTIALLY_ALIGNED" | "NOT_ALIGNED" | "STRONGLY_ALIGNED"
    confidence: float  # 0.0 - 1.0
    reasoning: str  # Justificación del LLM

    # Análisis de umbrales
    weak_verbs_count: int
    weak_verbs_threshold_passed: bool
    completeness_rate: Optional[float] = None
    completeness_threshold_passed: bool = True

    # Detección de problemas estructurales
    structural_issues: List[str] = field(default_factory=list)
    normativa_mismatches: List[str] = field(default_factory=list)

    # Validación de referencias institucionales (campos v4)
    institutional_references_match: bool = True  # ¿Referencias institucionales coinciden?
    has_hierarchical_backing: bool = False  # ¿Hay herencia jerárquica válida?

    # Análisis detallado (v5.41) - Incluye análisis función por función
    detailed_analysis: Optional[Dict[str, Any]] = None  # LLM result completo con analisis_funciones

    # Metadatos
    validation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class DetailedValidationResult:
    """Resultado de validación detallada (modo completo)"""
    # Campos requeridos (sin valor por defecto)
    function_number: int
    function_text: str
    verb: str
    normative_backed: bool
    backing_type: str  # "DIRECT" | "DERIVED" | "HIERARCHICAL" | "NOT_BACKED"
    appropriate_for_level: bool

    # Campos opcionales (con valor por defecto)
    normative_source: Optional[str] = None
    expected_alcance_range: Tuple[int, int] = (0, 0)
    actual_alcance: int = 0
    severity: str = "MINOR"  # "MINOR" | "MODERATE" | "CRITICAL"
    suggested_alternative: Optional[str] = None
    reasoning: str = ""
    confidence: float = 0.0

# ==========================================
# CLASE PRINCIPAL
# ==========================================

class ContextualVerbValidator:
    """
    Validador contextual de verbos con dos modos de operación
    """

    def __init__(self, normativa_loader=None, context: APFContext = None):
        self.normativa_loader = normativa_loader
        self.context = context or APFContext()
        self.validation_mode = VALIDATION_CONFIG["validation_mode"]

    def set_validation_mode(self, mode: str):
        """Cambia el modo de validación"""
        if mode not in ["HYBRID", "COMPLETE"]:
            raise ValueError(f"Modo inválido: {mode}. Usar 'HYBRID' o 'COMPLETE'")
        self.validation_mode = mode
        VALIDATION_CONFIG["validation_mode"] = mode

    # ==========================================
    # MODO HÍBRIDO (Rápido + LLM Global)
    # ==========================================

    def validate_global(
        self,
        puesto_nombre: str,
        objetivo_general: str,
        funciones: List[Dict[str, Any]],
        nivel_jerarquico: str,
        weak_verbs_detected: List[str]
    ) -> GlobalValidationResult:
        """
        Validación global del puesto completo (modo híbrido)

        Pasos:
        1. Validar umbrales (verbos débiles, completitud)
        2. Llamar LLM para validación semántica global
        3. Retornar resultado consolidado
        """

        # PASO 1: Validación de umbrales
        weak_verbs_count = len(weak_verbs_detected)
        weak_threshold = VALIDATION_CONFIG["weak_verb_threshold"]
        weak_verbs_pass = weak_verbs_count <= weak_threshold

        # Validar completitud de funciones
        completeness_rate = None
        completeness_pass = True

        if self.normativa_loader:
            expected_functions = self._estimate_expected_functions_count()
            if expected_functions > 0:
                completeness_rate = len(funciones) / expected_functions
                min_thresh = VALIDATION_CONFIG["completeness_min_threshold"]
                max_thresh = VALIDATION_CONFIG["completeness_max_threshold"]
                completeness_pass = min_thresh <= completeness_rate <= max_thresh

        # Si falla umbrales, retornar FAIL inmediato
        structural_issues = []
        if not weak_verbs_pass:
            structural_issues.append(
                f"Exceso de verbos débiles: {weak_verbs_count} > {weak_threshold}"
            )
        if not completeness_pass and completeness_rate is not None:
            if completeness_rate < VALIDATION_CONFIG["completeness_min_threshold"]:
                structural_issues.append(
                    f"Funciones insuficientes: {completeness_rate:.1%} < 50%"
                )
            else:
                structural_issues.append(
                    f"Sobrecarga de funciones: {completeness_rate:.1%} > 200%"
                )

        # PASO 2: Validación LLM Global
        llm_result = self._validate_with_llm_global(
            puesto_nombre=puesto_nombre,
            objetivo_general=objetivo_general,
            funciones=funciones,
            nivel_jerarquico=nivel_jerarquico
        )

        # PASO 3: Consolidar resultado con validación estricta (v5.41)

        # Extraer datos del nuevo formato con resumen_alineacion
        resumen = llm_result.get("resumen_alineacion", {})
        institutional_match = llm_result.get("instituciones_coinciden", True)
        has_hierarchical_backing = llm_result.get("has_hierarchical_backing", False)

        # Usar clasificacion_global del resumen (calculado por LLM basado en scores de funciones)
        clasificacion_global = resumen.get("clasificacion_global", llm_result.get("alignment_level", "NOT_ALIGNED"))
        score_promedio = resumen.get("score_promedio", 0.0)
        confianza = resumen.get("confianza", llm_result.get("confidence", 0.5))

        # Si falla umbrales O instituciones no coinciden O clasificacion es NOT_ALIGNED → NOT_ALIGNED
        if structural_issues or not institutional_match or clasificacion_global == "NOT_ALIGNED":
            alignment_level = "NOT_ALIGNED"
            is_aligned = False

            # Añadir contexto si fue por falta de coincidencia institucional
            if not institutional_match and "reasoning" in llm_result:
                llm_result["reasoning"] += " [RECHAZADO: Organismos no coinciden]"

        # PARTIALLY_ALIGNED: Aprobar con observaciones
        elif clasificacion_global == "PARTIALLY_ALIGNED":
            alignment_level = "PARTIALLY_ALIGNED"
            is_aligned = True  # Pasa con observaciones (score_promedio >= 0.55)

        # ALIGNED o STRONGLY_ALIGNED
        else:
            alignment_level = clasificacion_global  # Puede ser "ALIGNED" o "STRONGLY_ALIGNED"
            is_aligned = True

        return GlobalValidationResult(
            is_aligned=is_aligned,
            alignment_level=alignment_level,
            confidence=confianza,
            reasoning=llm_result.get("reasoning", "Sin razonamiento disponible"),
            weak_verbs_count=weak_verbs_count,
            weak_verbs_threshold_passed=weak_verbs_pass,
            completeness_rate=completeness_rate,
            completeness_threshold_passed=completeness_pass,
            structural_issues=structural_issues,
            normativa_mismatches=llm_result.get("normativa_mismatches", []),
            institutional_references_match=institutional_match,
            has_hierarchical_backing=has_hierarchical_backing,
            detailed_analysis=llm_result  # v5.41: Incluir análisis completo con analisis_funciones
        )

    def _validate_with_llm_global(
        self,
        puesto_nombre: str,
        objetivo_general: str,
        funciones: List[Dict[str, Any]],
        nivel_jerarquico: str
    ) -> Dict[str, Any]:
        """
        Llamada LLM para validación semántica global del puesto
        """

        # Construir texto de funciones
        funciones_text = "\n".join([
            f"{i}. {f.get('verbo_accion', '')} - {f.get('descripcion_completa', '')[:150]}"
            for i, f in enumerate(funciones, 1)
        ])

        # Crear query de búsqueda con objetivo general + funciones principales
        search_query = f"{objetivo_general} {' '.join([f.get('descripcion_completa', '')[:100] for f in funciones[:5]])}"

        # Obtener contexto normativo relevante con búsqueda semántica
        normativa_context = self._get_normativa_context_summary(search_query=search_query)

        prompt = f"""Eres un experto en análisis de descripciones de puestos de la Administración Pública Federal (APF).

VERSIÓN 5.41 - Sistema Jerárquico de Herencia Normativa
Tu tarea es evaluar CADA FUNCIÓN individualmente usando un sistema de 4 niveles de alineación jerárquica.

═══════════════════════════════════════════════════════════════
PUESTO A EVALUAR:
═══════════════════════════════════════════════════════════════
- NOMBRE: {puesto_nombre}
- NIVEL JERÁRQUICO: {nivel_jerarquico}
- OBJETIVO GENERAL: {objetivo_general}

FUNCIONES A EVALUAR ({len(funciones)} total):
{funciones_text}

═══════════════════════════════════════════════════════════════
NORMATIVA APLICABLE:
═══════════════════════════════════════════════════════════════
{normativa_context}

═══════════════════════════════════════════════════════════════
INSTRUCCIONES DE EVALUACIÓN - SISTEMA DE 4 NIVELES
═══════════════════════════════════════════════════════════════

PASO 1 - IDENTIFICACIÓN INTELIGENTE DE ORGANISMOS:
─────────────────────────────────────────────────────────────
A) IDENTIFICAR ORGANISMO DEL PUESTO:
   - Analiza el NOMBRE del puesto
   - Analiza OBJETIVO GENERAL y FUNCIONES
   - Extrae el nombre completo del organismo/dependencia
   - Extrae siglas si están presentes
   - Ejemplos: "Secretaría de...", "Comisión Nacional de...", "Instituto de..."

B) IDENTIFICAR ORGANISMO DE LA NORMATIVA:
   - Analiza títulos de documentos normativos
   - Analiza primeros artículos (objeto, ámbito)
   - Extrae el nombre completo del organismo
   - Extrae siglas si están presentes

C) VALIDACIÓN DE COINCIDENCIA:
   ✅ SI COINCIDEN → Continuar con análisis de funciones
   ❌ SI NO COINCIDEN → Resultado automático: NOT_ALIGNED

PASO 2 - IDENTIFICACIÓN DEL GRUPO JERÁRQUICO DEL PUESTO:
─────────────────────────────────────────────────────────────
Identifica el GRUPO JERÁRQUICO específico del puesto:
- Ejemplos: "Secretario", "Subsecretario", "Director General", "Director de Área",
  "Subdirector de Área", "Jefe de Departamento", "Enlace", etc.
- Busca en la normativa la sección de atribuciones de este grupo específico

PASO 3 - ANÁLISIS FUNCIÓN POR FUNCIÓN CON 4 NIVELES:
─────────────────────────────────────────────────────────────
Evalúa CADA función individualmente y clasifícala en uno de estos 4 niveles:

┌─────────────────────────────────────────────────────────────┐
│ NIVEL 1: ALINEACIÓN DIRECTA (Score: 0.9)                   │
├─────────────────────────────────────────────────────────────┤
│ Criterio: La función está EXPLÍCITAMENTE en la sección     │
│          del MISMO grupo jerárquico del puesto             │
│                                                             │
│ Ejemplo: Puesto "Subdirector de Área"                      │
│          Normativa: "Artículo 25. Los Subdirectores de     │
│                     Área tendrán las atribuciones..."      │
│          Coincidencia: EXACTA en mismo grupo               │
│                                                             │
│ Campos JSON:                                                │
│   - nivel: "NIVEL_1_ALINEACION_DIRECTA"                    │
│   - clasificacion: "STRONGLY_ALIGNED"                       │
│   - score: 0.9                                              │
│   - distancia_jerarquica: 0                                │
│   - tipo_herencia: "DIRECTA"                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NIVEL 2: HERENCIA DEL JEFE DIRECTO (Score: 0.75)          │
├─────────────────────────────────────────────────────────────┤
│ Criterio: La función es DERIVABLE de atribuciones del      │
│          JEFE INMEDIATO SUPERIOR (un nivel arriba)         │
│                                                             │
│ Ejemplo: Puesto "Subdirector de Área"                      │
│          Normativa: "Artículo 23. Los Directores de Área   │
│                     tendrán la atribución de coordinar..." │
│          La función del Subdirector "elaborar programas"   │
│          es operativa/técnica que APOYA la "coordinación"  │
│          estratégica del Director (su jefe directo)        │
│                                                             │
│ Validación:                                                 │
│   - Hay relación funcional jefe→subordinado                │
│   - La función subordinada es más operativa/técnica        │
│   - La función superior es más estratégica/directiva       │
│                                                             │
│ Campos JSON:                                                │
│   - nivel: "NIVEL_2_HERENCIA_JEFE_DIRECTO"                 │
│   - clasificacion: "ALIGNED"                                │
│   - score: 0.75                                             │
│   - distancia_jerarquica: 1                                │
│   - tipo_herencia: "DIRECTA"                               │
│   - grupo_encontrado: "Director de Área" (el jefe)        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NIVEL 3: HERENCIA LEJANA EN ORGANISMO (Score: 0.55)       │
├─────────────────────────────────────────────────────────────┤
│ Criterio: La función está en el MARCO GENERAL del          │
│          organismo pero sin cadena directa de herencia     │
│          (2 o más niveles de distancia)                    │
│                                                             │
│ Ejemplo: Puesto "Subdirector de Área"                      │
│          Normativa: "Artículo 5. El Secretario tiene la    │
│                     atribución de establecer políticas..." │
│          La función del Subdirector "proponer indicadores" │
│          está relacionada con políticas pero hay 3 niveles │
│          de distancia (Subdirector→Director→Subsecretario  │
│          →Secretario)                                      │
│                                                             │
│ Validación:                                                 │
│   - Función dentro del ámbito del organismo                │
│   - NO hay cadena clara jefe→subordinado                   │
│   - Distancia jerárquica: 2 o más niveles                  │
│                                                             │
│ Campos JSON:                                                │
│   - nivel: "NIVEL_3_HERENCIA_LEJANA"                       │
│   - clasificacion: "PARTIALLY_ALIGNED"                      │
│   - score: 0.55                                             │
│   - distancia_jerarquica: 2 (o más)                       │
│   - tipo_herencia: "LEJANA"                                │
│   - grupo_encontrado: "Secretario" (lejano en jerarquía)  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NIVEL 4: NO ALINEADO (Score: 0.0)                         │
├─────────────────────────────────────────────────────────────┤
│ Criterio: La función está FUERA del marco del organismo    │
│                                                             │
│ Ejemplos:                                                   │
│   - Función de un ámbito completamente diferente           │
│   - No aparece en ningún nivel de la estructura            │
│   - Contradice atribuciones del organismo                  │
│                                                             │
│ Campos JSON:                                                │
│   - nivel: "NIVEL_4_NO_ALINEADO"                           │
│   - clasificacion: "NOT_ALIGNED"                            │
│   - score: 0.0                                              │
│   - distancia_jerarquica: null                             │
│   - tipo_herencia: "NONE"                                  │
│   - grupo_encontrado: null                                 │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
RESPUESTA REQUERIDA - FORMATO JSON:
═══════════════════════════════════════════════════════════════

{{
  "organismo_puesto": {{
    "nombre": "Nombre completo del organismo del puesto",
    "siglas": "SIGLAS o null",
    "confianza": 0.0-1.0,
    "fuente_identificacion": "De dónde se extrajo (nombre/objetivo/funciones)"
  }},

  "organismo_normativa": {{
    "nombre": "Nombre completo del organismo de la normativa",
    "siglas": "SIGLAS o null",
    "confianza": 0.0-1.0,
    "fuente_identificacion": "De dónde se extrajo (título/artículos)"
  }},

  "instituciones_coinciden": true/false,

  "grupo_jerarquico_puesto": {{
    "nivel": "Subdirector de Área, Director de Área, etc.",
    "tipo": "Mando Medio/Alto/Operativo",
    "confianza": 0.0-1.0
  }},

  "analisis_funciones": [
    {{
      "funcion_id": "F001",
      "descripcion": "Texto completo de la función",

      "alineacion": {{
        "nivel": "NIVEL_1_ALINEACION_DIRECTA" | "NIVEL_2_HERENCIA_JEFE_DIRECTO" | "NIVEL_3_HERENCIA_LEJANA" | "NIVEL_4_NO_ALINEADO",
        "clasificacion": "STRONGLY_ALIGNED" | "ALIGNED" | "PARTIALLY_ALIGNED" | "NOT_ALIGNED",
        "score": 0.9 | 0.75 | 0.55 | 0.0,

        "evidencia_normativa": {{
          "grupo_encontrado": "Nombre del grupo jerárquico donde se encontró la atribución",
          "articulo": "Art. X, fracción Y",
          "texto": "Fragmento relevante de normativa (máx 200 chars)",
          "distancia_jerarquica": 0-5,
          "tipo_herencia": "DIRECTA" | "LEJANA" | "NONE"
        }},

        "razonamiento": "Explicación clara de por qué se asignó este nivel (2-3 oraciones)"
      }}
    }}
  ],

  "resumen_alineacion": {{
    "total_funciones": {len(funciones)},
    "nivel_1_directas": 0,
    "nivel_2_jefe_directo": 0,
    "nivel_3_lejanas": 0,
    "nivel_4_no_alineadas": 0,
    "score_promedio": 0.0-1.0,
    "clasificacion_global": "ALIGNED" | "PARTIALLY_ALIGNED" | "NOT_ALIGNED",
    "confianza": 0.0-1.0
  }},

  "reasoning": "Resumen ejecutivo de la evaluación completa (3-4 oraciones)",
  "institutional_references_match": true/false,
  "has_hierarchical_backing": true/false,
  "normativa_mismatches": []
}}

IMPORTANTE: Evalúa TODAS las {len(funciones)} funciones individualmente.
"""

        try:
            response = robust_openai_call(
                prompt=prompt,
                model="openai/gpt-4o-mini",  # Migrado a GPT-4o-mini (ahorro 94.6%)
                max_tokens=VALIDATION_CONFIG["llm_max_tokens"],
                temperature=VALIDATION_CONFIG["llm_temperature"],
                context=self.context
            )

            # Verificar respuesta exitosa
            if response.get("status") == "success":
                result = response["data"]
                return result
            else:
                # Error en llamada LLM - RECHAZAR por seguridad
                error_msg = response.get("error", "Error desconocido")
                print(f"⚠️ Error en validación LLM global: {error_msg}")
                return {
                    "alignment_level": "NOT_ALIGNED",
                    "confidence": 0.3,
                    "reasoning": f"Error en validación LLM: {error_msg}. Por seguridad se rechaza el puesto.",
                    "institutional_references_match": False,
                    "references_found_in_puesto": [],
                    "references_found_in_normativa": [],
                    "has_hierarchical_backing": False,
                    "hierarchical_reasoning": "",
                    "normativa_mismatches": ["Error técnico en validación"],
                    "strengths": [],
                    "improvement_areas": []
                }

        except Exception as e:
            print(f"⚠️ Error inesperado en validación LLM global: {e}")
            # Fallback seguro - RECHAZAR por seguridad
            return {
                "alignment_level": "NOT_ALIGNED",
                "confidence": 0.3,
                "reasoning": f"Error inesperado: {str(e)}. Por seguridad se rechaza el puesto.",
                "institutional_references_match": False,
                "references_found_in_puesto": [],
                "references_found_in_normativa": [],
                "has_hierarchical_backing": False,
                "hierarchical_reasoning": "",
                "normativa_mismatches": ["Error técnico en validación"],
                "strengths": [],
                "improvement_areas": []
            }

    # ==========================================
    # MODO COMPLETO (LLM Contextual Detallado)
    # ==========================================

    def validate_detailed(
        self,
        function_text: str,
        verb: str,
        nivel_jerarquico: str,
        function_number: int
    ) -> DetailedValidationResult:
        """
        Validación detallada de una función individual (modo completo)

        Valida:
        1. Respaldo normativo (DIRECTO / DERIVADO / JERÁRQUICO / NO_RESPALDADO)
        2. Apropiación de verbo para el nivel
        3. Alcance apropiado
        """

        # Obtener chunks relevantes de normativa para esta función
        relevant_chunks = self._get_relevant_normativa_chunks(function_text)

        prompt = f"""Eres un experto en análisis de descripciones de puestos de la APF.

FUNCIÓN A EVALUAR:
- Número: {function_number}
- Verbo: "{verb}"
- Descripción completa: "{function_text}"
- Nivel del puesto: {nivel_jerarquico}

NORMATIVA RELEVANTE:
{relevant_chunks}

JERARQUÍA DE VERBOS POR NIVEL:
- G11 (Secretario): dirigir, establecer, autorizar, aprobar, sancionar (alcance 7-10)
- J31 (Titular OAD): coordinar, supervisar, administrar, evaluar (alcance 5-8)
- M1 (Director): administrar, gestionar, implementar, supervisar (alcance 4-7)
- P3 (Jefe Depto): ejecutar, implementar, recopilar, elaborar (alcance 1-5)

ESCALA DE ALCANCE:
1. Operativo: recopilar, registrar
2. Técnico: elaborar, preparar
3. Supervisión: verificar, revisar
4. Analítico: evaluar, analizar
5. Asesoría: proponer, recomendar
6. Coordinación: coordinar, gestionar
7. Gerencial: administrar, supervisar
8. Decisión: aprobar, autorizar
9. Estratégico: dirigir, establecer
10. Normativo: sancionar, expedir

TAREA:
Evalúa si esta función está RESPALDADA por la normativa considerando:

1. RESPALDO DIRECTO: ¿La función está explícitamente en la normativa?
2. RESPALDO DERIVADO: ¿Es una derivación lógica de una función superior?
3. RESPALDO JERÁRQUICO: ¿El verbo es apropiado para el nivel del puesto?

RESPONDE EN JSON:
{{
  "normative_backed": true/false,
  "backing_type": "DIRECT" | "DERIVED" | "HIERARCHICAL" | "NOT_BACKED",
  "normative_source": "cita textual de normativa si aplica",
  "appropriate_for_level": true/false,
  "actual_alcance": 1-10,
  "severity": "MINOR" | "MODERATE" | "CRITICAL",
  "suggested_alternative": "verbo alternativo si aplica",
  "reasoning": "justificación clara (2-3 oraciones)",
  "confidence": 0.0-1.0
}}
"""

        try:
            response = robust_openai_call(
                prompt=prompt,
                model="openai/gpt-4o-mini",  # Migrado a GPT-4o-mini (ahorro 94.6%)
                max_tokens=VALIDATION_CONFIG["llm_max_tokens"],
                temperature=VALIDATION_CONFIG["llm_temperature"],
                context=self.context
            )

            # Verificar respuesta exitosa
            if response.get("status") != "success":
                error_msg = response.get("error", "Error desconocido")
                print(f"⚠️ Error en validación LLM detallada: {error_msg}")
                # Fallback a resultado de error
                expected_range = NIVEL_TO_ALCANCE.get(nivel_jerarquico, (1, 10))
                return DetailedValidationResult(
                    function_number=function_number,
                    function_text=function_text,
                    verb=verb,
                    normative_backed=False,
                    backing_type="NOT_BACKED",
                    appropriate_for_level=False,
                    expected_alcance_range=expected_range,
                    severity="CRITICAL",
                    reasoning=f"Error en validación: {error_msg}",
                    confidence=0.3
                )

            # Parsear respuesta exitosa
            llm_result = response["data"]

            # Determinar alcance esperado para el nivel
            expected_range = NIVEL_TO_ALCANCE.get(nivel_jerarquico, (1, 10))

            return DetailedValidationResult(
                function_number=function_number,
                function_text=function_text,
                verb=verb,
                normative_backed=llm_result.get("normative_backed", False),
                backing_type=llm_result.get("backing_type", "NOT_BACKED"),
                normative_source=llm_result.get("normative_source"),
                appropriate_for_level=llm_result.get("appropriate_for_level", False),
                expected_alcance_range=expected_range,
                actual_alcance=llm_result.get("actual_alcance", 0),
                severity=llm_result.get("severity", "CRITICAL"),
                suggested_alternative=llm_result.get("suggested_alternative"),
                reasoning=llm_result.get("reasoning", ""),
                confidence=llm_result.get("confidence", 0.5)
            )

        except Exception as e:
            print(f"⚠️ Error inesperado en validación LLM detallada: {e}")
            # Fallback seguro
            return DetailedValidationResult(
                function_number=function_number,
                function_text=function_text,
                verb=verb,
                normative_backed=False,
                backing_type="NOT_BACKED",
                appropriate_for_level=False,
                severity="CRITICAL",
                reasoning=f"Error en validación: {str(e)}",
                confidence=0.3
            )

    # ==========================================
    # MÉTODOS AUXILIARES
    # ==========================================

    def _get_normativa_context_summary(self, search_query: str = "") -> str:
        """Obtiene resumen del contexto normativo con contenido relevante

        Args:
            search_query: Query para búsqueda semántica de chunks relevantes

        Returns:
            Texto con metadata y chunks de normativa
        """
        if not self.normativa_loader or not hasattr(self.normativa_loader, 'documents'):
            return "No hay normativa cargada"

        summaries = []

        # Primero: metadata de documentos
        for doc_id, doc in self.normativa_loader.documents.items():
            doc_title = getattr(doc, 'title', 'Documento normativo')
            doc_type = getattr(doc, 'document_type', 'Reglamento')
            word_count = getattr(doc, 'word_count', 0)
            summaries.append(f"- {doc_title} ({doc_type}, {word_count} palabras)")

        metadata = "\n".join(summaries[:3])

        # Segundo: contenido relevante mediante búsqueda semántica
        content_chunks = []
        if search_query:
            # Buscar chunks relevantes usando semantic search
            try:
                search_results = self.normativa_loader.semantic_search(
                    query=search_query,
                    max_results=15,  # Traer top 15 chunks más relevantes (más contenido)
                    use_cache=True
                )

                for i, match in enumerate(search_results, 1):
                    # Obtener contenido completo del chunk, no solo snippet
                    doc = self.normativa_loader.documents.get(match.document_id)
                    if doc and hasattr(doc, 'semantic_chunks'):
                        chunk_idx = match.position_info.get('chunk_index', 0)
                        if chunk_idx < len(doc.semantic_chunks):
                            full_chunk = doc.semantic_chunks[chunk_idx]
                            content_chunks.append(
                                f"[Fragmento {i} - Similitud: {match.confidence_score:.2f}]\n{full_chunk[:1500]}"
                            )
            except Exception as e:
                print(f"⚠️ Error en búsqueda semántica de contexto: {e}")
                # Fallback mejorado: tomar múltiples chunks iniciales de cada documento
                for doc_id, doc in list(self.normativa_loader.documents.items())[:2]:
                    if hasattr(doc, 'semantic_chunks') and doc.semantic_chunks:
                        # Tomar los primeros 5 chunks de cada documento
                        for i, chunk in enumerate(doc.semantic_chunks[:5], 1):
                            content_chunks.append(f"[Chunk inicial {i}]\n{chunk[:1200]}")

        # Construir resumen completo
        result = f"DOCUMENTOS NORMATIVOS CARGADOS:\n{metadata}\n\n"

        if content_chunks:
            result += "CONTENIDO NORMATIVO RELEVANTE:\n"
            result += "\n\n".join(content_chunks)
        else:
            result += "No se encontraron fragmentos relevantes específicos."

        return result

    def _get_relevant_normativa_chunks(self, function_text: str, max_chunks: int = 3) -> str:
        """Obtiene chunks de normativa relevantes para una función"""
        if not self.normativa_loader or not hasattr(self.normativa_loader, 'documents'):
            return "No hay normativa cargada"

        # TODO: Implementar búsqueda semántica con embeddings
        # Por ahora, retornar primeros chunks de cada documento
        chunks_text = []
        for doc_id, doc in list(self.normativa_loader.documents.items())[:2]:
            if hasattr(doc, 'chunks') and doc.chunks:
                chunk = doc.chunks[0]
                content = getattr(chunk, 'content', '')
                chunks_text.append(content[:300] + "...")

        return "\n\n".join(chunks_text) if chunks_text else "No hay chunks disponibles"

    def _estimate_expected_functions_count(self) -> int:
        """Estima cantidad esperada de funciones basada en normativa"""
        if not self.normativa_loader or not hasattr(self.normativa_loader, 'documents'):
            return 0

        # Buscar menciones de "función" o "atribución" en la normativa
        # Por ahora, retornar un estimado conservador
        # TODO: Parsear funciones de la normativa de forma estructurada
        return 20  # Placeholder

    def get_validation_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del validador"""
        return {
            "validation_mode": self.validation_mode,
            "weak_verb_threshold": VALIDATION_CONFIG["weak_verb_threshold"],
            "completeness_thresholds": {
                "min": VALIDATION_CONFIG["completeness_min_threshold"],
                "max": VALIDATION_CONFIG["completeness_max_threshold"]
            },
            "normativa_loaded": self.normativa_loader is not None
        }


# ==========================================
# FUNCIÓN FACTORY
# ==========================================

def create_contextual_validator(normativa_loader=None, context: APFContext = None, mode: str = "HYBRID"):
    """Crea un validador contextual con el modo especificado"""
    validator = ContextualVerbValidator(normativa_loader, context)
    validator.set_validation_mode(mode)
    return validator


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":
    print("🧪 CONTEXTUAL VERB VALIDATOR - Test")
    print("=" * 60)

    validator = create_contextual_validator(mode="HYBRID")
    print(f"✅ Validador creado en modo: {validator.validation_mode}")
    print(json.dumps(validator.get_validation_summary(), indent=2))
