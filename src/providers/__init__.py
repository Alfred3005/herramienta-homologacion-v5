"""
Providers - Implementaciones concretas de interfaces

Implementa el principio de Dependency Inversion (DIP):
- Los módulos core dependen de interfaces abstractas
- Estos providers implementan esas interfaces
- Fácil agregar nuevos providers sin modificar core

Providers disponibles:
- openai_provider: Implementación para OpenAI (GPT-4, GPT-3.5)
- memory_cache_provider: Cache en memoria
- file_logger: Logger basado en archivos
"""

__version__ = '5.0.0'
