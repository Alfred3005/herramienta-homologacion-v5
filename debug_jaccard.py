#!/usr/bin/env python3
"""
Debug: Por qué Jaccard no encuentra fragmentos
"""
import sys
sys.path.insert(0, '/home/alfred/herramienta-homologacion-v5')

from src.validators.in_memory_normativa_adapter import create_loader_from_fragments
from src.validators.shared_utilities import APFContext

normativa_text = """
Artículo 6. Corresponde a la persona titular de la Secretaría:

I. Elaborar y conducir las políticas públicas competencia de la Secretaría en materia de fiscalización, control interno, auditoría y anticorrupción;

II. Emitir las normas que regulen el ejercicio de las funciones de control interno, auditoría, vigilancia y evaluación de la gestión pública;
"""

fragmentos = [p.strip() for p in normativa_text.split('\n\n') if p.strip()]
print(f"Fragmentos: {len(fragmentos)}\n")
for i, f in enumerate(fragmentos, 1):
    print(f"{i}. [{len(f)} chars] {f[:80]}...")

context = APFContext()
loader = create_loader_from_fragments(
    text_fragments=fragmentos,
    document_title="Reglamento SABG",
    use_embeddings=False,
    context=context
)

# Inspeccionar el loader
print(f"\n=== LOADER STATE ===")
print(f"Documents: {len(loader.documents)}")
for doc_id, doc in loader.documents.items():
    print(f"\nDoc ID: {doc_id}")
    print(f"Content length: {len(doc.content)}")
    print(f"Word count: {doc.word_count}")
    print(f"Content preview: {doc.content[:200]}...")

# Inspeccionar el índice global
print(f"\n=== GLOBAL INDEX ===")
print(f"Keywords in index: {len(loader.global_keyword_index)}")
if len(loader.global_keyword_index) > 0:
    sample_keys = list(loader.global_keyword_index.keys())[:10]
    print(f"Sample keywords: {sample_keys}")
else:
    print("⚠️ El índice está VACÍO")

# Probar búsqueda con diferentes queries
queries = [
    "emitir",
    "políticas",
    "elaborar",
    "artículo 6"
]

print(f"\n=== TESTING QUERIES ===")
for query in queries:
    results = loader.semantic_search(query, max_results=3)
    print(f"\nQuery: '{query}' → {len(results)} resultados")
    if results:
        for r in results[:2]:
            print(f"  - Score: {r.score:.2f}, Fragment: {r.fragment[:60]}...")
