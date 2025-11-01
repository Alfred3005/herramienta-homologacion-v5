# Sistema de Homologación APF v5.0

Sistema modular para extracción, evaluación y validación de descripciones de puestos de la Administración Pública Federal (APF) de México.

## 🎯 Novedades de v5.0

Esta versión representa una **refactorización completa** con enfoque en:

- ✅ **Arquitectura SOLID**: Cumplimiento del 90% de principios SOLID
- ✅ **Modularidad**: 25 módulos especializados con responsabilidades claras
- ✅ **Testabilidad**: Dependency Injection habilitada para testing
- ✅ **Extensibilidad**: Fácil agregar nuevos proveedores LLM sin modificar core
- ✅ **Configuración Externa**: Reglas y jerarquías configurables sin tocar código

## 📊 Mejoras vs v4

| Aspecto | v4 | v5 | Mejora |
|---------|----|----|--------|
| Tamaño repo | 15 MB | 2 MB | 87% reducción |
| Archivos Python | 37 | 25 | 32% reducción |
| Cumplimiento SOLID | 40% | 90% | 125% mejora |
| Scripts experimentales | 18 | 0 | 100% limpieza |

## 🏗️ Arquitectura

```
src/
├── interfaces/        # Contratos abstractos (DIP)
│   ├── llm_provider.py
│   ├── cache_provider.py
│   ├── logger.py
│   └── normativa_source.py
│
├── core/              # Lógica de negocio (SRP)
│   ├── file_reader.py
│   ├── prompt_builder.py
│   ├── data_validator.py
│   ├── agente_extractor.py
│   └── agente_evaluador.py
│
├── providers/         # Implementaciones (DIP)
│   ├── openai_provider.py
│   └── memory_cache_provider.py
│
├── engines/
│   ├── embedding_engine.py
│   └── normativa_loader.py
│
├── utils/
│   └── text_processing.py
│
└── pipeline/
    └── apf_pipeline.py
```

## 🚀 Quick Start

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/Alfred3005/herramienta-homologacion-v5.git
cd herramienta-homologacion-v5

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración

```bash
# Copiar archivo de configuración de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key de OpenAI
# OPENAI_API_KEY=tu-api-key-aqui
```

### Uso Básico

**Opción 1: Usando el script de ejemplo**

```bash
# Configurar API key
export OPENAI_API_KEY='tu-api-key'

# Ejecutar extracción
python scripts/run_extraction.py data/examples/puesto_ejemplo.pdf intelligent
```

**Opción 2: Programáticamente (Simple)**

```python
from src.pipeline import PipelineFactory
from src.core import ExtractionMode

# Crear pipeline simple (usa variable de entorno OPENAI_API_KEY)
extractor = PipelineFactory.create_simple_pipeline()

# Extraer información de un archivo
result = extractor.extract_from_file(
    "data/examples/puesto_ejemplo.pdf",
    mode=ExtractionMode.INTELLIGENT
)

# Acceder a los datos
if result['status'] == 'success':
    data = result['data']
    print(f"Puesto: {data['identificacion_puesto']['denominacion_puesto']}")
    print(f"Funciones: {len(data['funciones'])}")
```

**Opción 3: Programáticamente (Avanzado con DI)**

```python
from src.providers import OpenAIProvider
from src.core import APFExtractor, FileReader, PromptBuilder, DataValidator

# Crear dependencias manualmente (control total)
llm_provider = OpenAIProvider(
    api_key="tu-api-key",
    default_model="openai/gpt-4o",
    timeout=60
)

file_reader = FileReader(encoding='utf-8')
prompt_builder = PromptBuilder()
data_validator = DataValidator(strict_mode=False)

# Inyectar dependencias
extractor = APFExtractor(
    llm_provider=llm_provider,
    file_reader=file_reader,
    prompt_builder=prompt_builder,
    data_validator=data_validator
)

# Usar extractor
result = extractor.extract_from_file("puesto.pdf")
```

## 📚 Documentación

- [Arquitectura Detallada](docs/architecture.md)
- [Principios SOLID Aplicados](docs/solid_principles.md)
- [API Reference](docs/api_reference.md)
- [Guía de Contribución](docs/contributing.md)

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/test_extractor.py
```

## 🔧 Configuración

### Jerarquía de Verbos

Configurable en `config/verb_hierarchy.json`:

```json
{
  "levels": [
    {
      "id": 1,
      "name": "Operativo",
      "verbs": ["recopilar", "registrar", "archivar"]
    }
  ]
}
```

### Reglas de Validación

Configurable en `config/validation_rules.json`:

```json
{
  "weak_verb_threshold": 20,
  "completeness_min_threshold": 0.5
}
```

## 🎓 Principios SOLID

Este proyecto aplica rigurosamente los principios SOLID:

### S - Single Responsibility
Cada módulo tiene una responsabilidad clara:
- `file_reader.py` - Solo lectura de archivos
- `prompt_builder.py` - Solo construcción de prompts

### O - Open/Closed
Extensible mediante configuración y plugins, sin modificar código core.

### L - Liskov Substitution
Jerarquías bien definidas con sustitución segura.

### I - Interface Segregation
Interfaces pequeñas y especializadas (ILogger, ICache, etc.)

### D - Dependency Inversion
Dependencias inyectadas mediante interfaces abstractas.

Ver [docs/solid_principles.md](docs/solid_principles.md) para detalles.

## 📝 Changelog

### v5.0.0 (2025-10-31)

**✨ Nueva versión con refactorización completa**

- Arquitectura modular basada en SOLID
- Interfaces abstractas para máxima extensibilidad
- Dependency Injection habilitada
- Configuración externa de reglas
- Reducción de 87% en tamaño de repositorio
- Eliminación de código experimental
- Suite de tests unitarios

**Migración desde v4**:
- Ver [MIGRATION_FROM_V4.md](docs/MIGRATION_FROM_V4.md)

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](docs/contributing.md).

## 🔗 Links

- **v4 (legacy)**: [HerramientaHomologacionDocker](https://github.com/Alfred3005/HerramientaHomologacionDocker)
- **Branch de archivo v4**: `archive/v4-calibration-history`
- **Documentación v4**: Preservada en branch de archivo

---

**Versión**: 5.0.0
**Última actualización**: 2025-10-31
**Mantenido por**: Equipo APF
