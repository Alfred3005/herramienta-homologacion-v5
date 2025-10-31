"""
Módulos core del sistema de homologación APF v5.0

Contiene la lógica de negocio principal:
- file_reader: Lectura de archivos de puestos
- prompt_builder: Construcción de prompts para LLM
- data_validator: Validación de esquemas y datos
- agente_extractor: Extracción de información de puestos
- agente_evaluador: Evaluación de puestos contra normativa
- contextual_validator: Validación contextual inteligente
- verb_analyzer: Análisis semántico de verbos
- llm_evaluator: Evaluación mediante LLM

Todos los módulos siguen el principio de Single Responsibility.
"""

__version__ = '5.0.0'
