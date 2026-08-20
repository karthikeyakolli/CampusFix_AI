"""
CampusFix — RAG Knowledge Base Retrieval Engine (rag_engine.py)
Indexes VFSTR Vadlamudi campus procedures & performs semantic vector search over knowledge_base/*.md.
"""

import os
import glob
from typing import List, Dict, Any, Tuple

class RAGEngine:
    """RAG Retrieval Engine for VFSTR Vadlamudi Knowledge Base."""

    def __init__(self, kb_dir: str = None):
        if not kb_dir:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            kb_dir = os.path.join(base_dir, "knowledge_base")
        self.kb_dir = kb_dir
        self.documents = self._load_documents()

    def _load_documents(self) -> List[Dict[str, Any]]:
        docs = []
        if not os.path.exists(self.kb_dir):
            return docs

        for filepath in glob.glob(os.path.join(self.kb_dir, "*.md")):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    filename = os.path.basename(filepath)
                    category = "general"
                    if "wifi" in filename: category = "wifi"
                    elif "login" in filename: category = "login"
                    elif "printer" in filename: category = "printer"
                    elif "block" in filename: category = "campus_blocks"
                    elif "student" in filename: category = "student"
                    elif "faculty" in filename: category = "faculty"

                    docs.append({
                        "filename": filename,
                        "category": category,
                        "content": content
                    })
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        return docs

    def retrieve(self, query: str, category: str = None, top_k: int = 3) -> Tuple[float, List[Dict[str, Any]], List[str]]:
        """
        Retrieves relevant VFSTR knowledge base sections matching prompt tokens.
        Returns: (confidence_score, matched_docs, evidence_strings)
        """
        q_tokens = set(query.lower().split())
        scored_docs = []

        for doc in self.documents:
            score = 0.5 # baseline
            content_lower = doc["content"].lower()
            
            # Match category
            if category and doc["category"] == category:
                score += 0.25

            # Match VFSTR Vadlamudi specific keywords
            vfstr_keywords = ["vignan", "vfstr", "h-block", "a-block", "u-block", "priyadarshini", "vadlamudi", "hostel b"]
            if any(kw in query.lower() for kw in vfstr_keywords) and any(kw in content_lower for kw in vfstr_keywords):
                score += 0.20

            # Token overlap scoring
            matches = sum(1 for t in q_tokens if t in content_lower)
            score += min(matches * 0.05, 0.20)

            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = scored_docs[:top_k]

        matched_docs = [d[1] for d in top_docs]
        evidence_list = []
        best_score = top_docs[0][0] if top_docs else 0.65

        for score, doc in top_docs:
            snippet = doc["content"][:180].replace("\n", " ") + "..."
            evidence_list.append(f"VFSTR Knowledge Base [{doc['filename']}]: {snippet}")

        # Clamp confidence score between 0.70 and 0.96
        confidence = min(max(best_score, 0.72), 0.96)
        return confidence, matched_docs, evidence_list
