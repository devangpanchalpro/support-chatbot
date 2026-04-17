"""
RAG Engine - Retrieval Augmented Generation without LLM
Uses TF-IDF similarity to find most relevant documents
"""

import json
import math
import re
from pathlib import Path


class RAGEngine:
    def __init__(self, knowledge_base_path="knowledge_base.json", use_multiple_files=True):
        """
        Initialize RAG Engine
        
        Args:
            knowledge_base_path: Path to knowledge base file/folder
            use_multiple_files: If True, load from folder with multiple JSON files
                               If False, load from single JSON file
        """
        self.documents = []
        self.tfidf_matrix = []
        self.vocabulary = {}
        self.idf_scores = {}
        
        if use_multiple_files:
            self._load_knowledge_base_folder(knowledge_base_path)
        else:
            self._load_knowledge_base_single(knowledge_base_path)
        
        self._build_tfidf_index()

    def _load_knowledge_base_single(self, path):
        """Load knowledge base from a single JSON file"""
        kb_path = Path(__file__).parent / path
        with open(kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.documents = data["documents"]
        print(f"[RAG] Loaded {len(self.documents)} documents from single file: {path}")

    def _load_knowledge_base_folder(self, folder_path):
        """Load knowledge base from multiple JSON files in a folder"""
        kb_folder = Path(__file__).parent / folder_path
        
        # If folder doesn't exist, try loading as single file
        if not kb_folder.is_dir():
            print(f"[RAG] Folder not found: {kb_folder}. Trying as single file...")
            self._load_knowledge_base_single(folder_path)
            return
        
        # Load all *_base.json files
        self.documents = []
        loaded_files = 0
        
        for json_file in sorted(kb_folder.glob("*_base.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "documents" in data:
                        self.documents.extend(data["documents"])
                        loaded_files += 1
                        print(f"[RAG] Loaded {len(data['documents'])} docs from {json_file.name}")
            except Exception as e:
                print(f"[RAG] Error loading {json_file.name}: {e}")
        
        if loaded_files == 0:
            raise FileNotFoundError(f"No *_base.json files found in {kb_folder}")
        
        print(f"[RAG] Total {len(self.documents)} documents loaded from {loaded_files} files")

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
            if "keywords" in doc:
                combined += " " + doc["keywords"]
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

    def _keyword_filter(self, query, min_keyword_match=1):
        """Filter documents that contain at least min_keyword_match keywords"""
        query_tokens = set(self._tokenize(query))
        filtered_indices = []
        
        for idx, doc in enumerate(self.documents):
            doc_text = (doc["title"] + " " + doc["content"]).lower()
            if "keywords" in doc:
                doc_text += " " + doc["keywords"].lower()
            doc_tokens = set(self._tokenize(doc_text))
            
            # Count matching keywords
            matching_keywords = len(query_tokens & doc_tokens)
            
            if matching_keywords >= min_keyword_match:
                filtered_indices.append(idx)
        
        return filtered_indices

    def retrieve(self, query, top_k=3, category_filter=None, use_keyword_filter=False):
        """Retrieve top-k most relevant documents for a query
        
        Args:
            query: User's search query
            top_k: Number of top results to return
            category_filter: Optional category to filter by
            use_keyword_filter: If True, pre-filter documents using keyword matching
        """
        query_vector = self._query_to_tfidf(query)

        # STEP 1: Pre-filter by keywords (if enabled)
        if use_keyword_filter:
            filtered_indices = self._keyword_filter(query)
            if not filtered_indices:
                # If no keyword match, fall back to TF-IDF only
                filtered_indices = list(range(len(self.documents)))
        else:
            filtered_indices = list(range(len(self.documents)))

        # STEP 2: Score filtered documents with TF-IDF
        scored_docs = []
        for idx in filtered_indices:
            doc = self.documents[idx]
            doc_vector = self.tfidf_matrix[idx]
            
            if category_filter and doc["category"] != category_filter:
                continue
            
            score = self._cosine_similarity(query_vector, doc_vector)
            scored_docs.append((score, doc))

        # STEP 3: Sort and return top results
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

    def get_all_documents_by_category(self, category):
        """Get all document titles for a specific category"""
        return [doc for doc in self.documents if doc.get("category") == category]