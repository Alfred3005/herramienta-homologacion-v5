#!/usr/bin/env python3
"""
Debug: Verificar si semantic_chunks se crean correctamente
"""
import sys
sys.path.insert(0, '/home/alfred/herramienta-homologacion-v5')

from src.validators.in_memory_normativa_adapter import create_loader_from_fragments
from src.validators.shared_utilities import APFContext

normativa_text = """
Artículo 6. Corresponde a la persona titular de la Secretaría:

I. Elaborar y conducir las políticas públicas competencia de la Secretaría;

II. Emitir las normas que regulen el ejercicio de las funciones de control interno;
"""

fragmentos = [p.strip() for p in normativa_text.split('\n\n') if p.strip()]

context = APFContext()
loader = create_loader_from_fragments(
    text_fragments=fragmentos,
    document_title="Reglamento SABG",
    use_embeddings=False,
    context=context
)

# Inspeccionar chunks
for doc_id, doc in loader.documents.items():
    print(f"Document ID: {doc_id}")
    print(f"Content length: {len(doc.content)}")
    print(f"semantic_chunks count: {len(doc.semantic_chunks)}")
    print(f"article_index count: {len(doc.article_index)}")

    print("\nPrimeros 3 semantic_chunks:")
    for i, chunk in enumerate(doc.semantic_chunks[:3], 1):
        print(f"\n{i}. [{len(chunk)} chars]")
        print(f"   {chunk[:100]}...")

    print("\narticle_index:")
    for art_id, content in list(doc.article_index.items())[:3]:
        print(f"\n  {art_id}: {content[:80]}...")
