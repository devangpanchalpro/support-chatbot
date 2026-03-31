"""
RAG Engine - Retrieval Augmented Generation without LLM
Uses TF-IDF similarity to find most relevant documents
"""

import json
import math
import re
from pathlib import Path


class RAGEngine:
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        self.documents = []
        self.tfidf_matrix = []
        self.vocabulary = {}
        self.idf_scores = {}
        self._load_knowledge_base(knowledge_base_path)
        self._build_tfidf_index()

    def _load_knowledge_base(self, path):
        kb_path = Path(__file__).parent / path
        with open(kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.documents = data["documents"]
        print(f"[RAG] Loaded {len(self.documents)} documents into knowledge base.")

    def _tokenize(self, text):
        """Lowercase and tokenize text"""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = text.split()
        # Remove very short tokens
        tokens = [t for t in tokens if len(t) > 1]
        return tokens

    def _build_tfidf_index(self):
        """Build TF-IDF index from all documents"""
        all_tokens = []
        doc_tokens = []

        for doc in self.documents:
            combined = doc["title"] + " " + doc["content"]
            tokens = self._tokenize(combined)
            doc_tokens.append(tokens)
            all_tokens.extend(tokens)

        # Build vocabulary
        unique_tokens = list(set(all_tokens))
        self.vocabulary = {token: idx for idx, token in enumerate(unique_tokens)}

        # Calculate IDF scores
        num_docs = len(self.documents)
        for token in unique_tokens:
            doc_count = sum(1 for tokens in doc_tokens if token in tokens)
            self.idf_scores[token] = math.log((num_docs + 1) / (doc_count + 1)) + 1

        # Calculate TF-IDF vectors for each document
        self.tfidf_matrix = []
        for tokens in doc_tokens:
            tf_counts = {}
            for token in tokens:
                tf_counts[token] = tf_counts.get(token, 0) + 1

            tfidf_vector = {}
            total_tokens = len(tokens)
            for token, count in tf_counts.items():
                tf = count / total_tokens
                idf = self.idf_scores.get(token, 1)
                tfidf_vector[token] = tf * idf

            self.tfidf_matrix.append(tfidf_vector)

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two TF-IDF vectors"""
        common_tokens = set(vec1.keys()) & set(vec2.keys())
        if not common_tokens:
            return 0.0

        dot_product = sum(vec1[t] * vec2[t] for t in common_tokens)
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def _query_to_tfidf(self, query):
        """Convert a query string to TF-IDF vector"""
        tokens = self._tokenize(query)
        tf_counts = {}
        for token in tokens:
            tf_counts[token] = tf_counts.get(token, 0) + 1

        tfidf_vector = {}
        total = len(tokens) if tokens else 1
        for token, count in tf_counts.items():
            tf = count / total
            idf = self.idf_scores.get(token, 1)
            tfidf_vector[token] = tf * idf

        return tfidf_vector

    def retrieve(self, query, top_k=3, category_filter=None):
        """Retrieve top-k most relevant documents for a query"""
        query_vector = self._query_to_tfidf(query)

        scored_docs = []
        for idx, (doc, doc_vector) in enumerate(zip(self.documents, self.tfidf_matrix)):
            if category_filter and doc["category"] != category_filter:
                continue
            score = self._cosine_similarity(query_vector, doc_vector)
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [(score, doc) for score, doc in scored_docs[:top_k] if score > 0]

        return top_docs

    def get_answer(self, query, top_k=2):
        """Get best answer content for a query"""
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return None, []

        answers = []
        for score, doc in results:
            answers.append({
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"],
                "score": round(score, 3)
            })

        return answers[0]["content"] if answers else None, answers