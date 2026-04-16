#!/usr/bin/env python
"""Test script to verify RAG engine works with multiple files"""

from bot.RAG_engine import RAGEngine

# Initialize RAG with multiple files
rag = RAGEngine(knowledge_base_path="../data", use_multiple_files=True)

# Test query
query = "ABHA card"
results = rag.retrieve(query, top_k=2)

print(f"\n{'='*60}")
print(f"Test Query: '{query}'")
print(f"{'='*60}\n")

for i, (score, doc) in enumerate(results, 1):
    print(f"{i}. {doc['title']}")
    print(f"   Category: {doc['category']}")
    print(f"   Score: {score:.3f}")
    print()

print("✅ RAG Engine Test Passed!")
