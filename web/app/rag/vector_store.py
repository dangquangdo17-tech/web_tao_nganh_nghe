import math
import re
from typing import List, Dict, Any, Tuple
import numpy as np
from .knowledge_base import MAJOR_KNOWLEDGE_DOCS
from .hyde_engine import HyDEEngine

class VectorStore:
    """
    Vector RAG Engine kết hợp HyDE và tính toán tương đồng Cosine Similarity
    để đối chiếu sở thích của học sinh với cơ sở tri thức ngành nghề.
    """
    def __init__(self):
        self.docs = MAJOR_KNOWLEDGE_DOCS
        self.vocabulary = set()
        self.doc_vectors = []
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        # Tách từ tiếng Việt đơn giản và chuẩn hóa
        text = text.lower()
        words = re.findall(r"[\w]+", text)
        return [w for w in words if len(w) > 1]

    def _build_index(self):
        # Tạo tập từ vựng (vocabulary) từ nội dung và từ khóa
        all_tokens_per_doc = []
        for doc in self.docs:
            full_text = f"{doc['name']} {doc['category']} {' '.join(doc['keywords'])} {doc['content']}"
            tokens = self._tokenize(full_text)
            all_tokens_per_doc.append(tokens)
            self.vocabulary.update(tokens)

        self.vocab_list = sorted(list(self.vocabulary))
        self.word2idx = {w: i for i, w in enumerate(self.vocab_list)}
        
        # Tính IDF
        N = len(self.docs)
        self.idf = np.zeros(len(self.vocab_list))
        for word, idx in self.word2idx.items():
            doc_freq = sum(1 for tokens in all_tokens_per_doc if word in tokens)
            self.idf[idx] = math.log((N + 1) / (doc_freq + 1)) + 1.0

        # Tạo vector TF-IDF cho từng tài liệu ngành nghề
        for tokens, doc in zip(all_tokens_per_doc, self.docs):
            vec = np.zeros(len(self.vocab_list))
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            
            for t, count in tf.items():
                if t in self.word2idx:
                    idx = self.word2idx[t]
                    # Thêm trọng số nếu từ khóa nằm trong keywords
                    weight = 2.5 if t in doc["keywords"] else 1.0
                    vec[idx] = (count / len(tokens)) * self.idf[idx] * weight

            # Chuẩn hóa vector L2
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            self.doc_vectors.append(vec)

        self.doc_vectors = np.array(self.doc_vectors)

    def _vectorize_query(self, text: str) -> np.ndarray:
        tokens = self._tokenize(text)
        vec = np.zeros(len(self.vocab_list))
        if not tokens:
            return vec
            
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
            
        for t, count in tf.items():
            if t in self.word2idx:
                idx = self.word2idx[t]
                vec[idx] = (count / len(tokens)) * self.idf[idx]
                
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def search_with_hyde(self, user_query: str, top_k: int = 27) -> Dict[str, Any]:
        """
        Thực hiện tìm kiếm Vector RAG kết hợp kỹ thuật HyDE:
        1. Sinh văn bản giả định HyDE
        2. Vectorize câu gốc và văn bản giả định (kết hợp theo trọng số)
        3. Tính Cosine Similarity và xếp hạng ngành nghề
        """
        hyde_result = HyDEEngine.generate_hypothetical_document(user_query)
        hypo_doc = hyde_result["hypothetical_document"]
        domain_detected = hyde_result.get("domain_detected", "custom_dynamic")

        neg_info = hyde_result.get("negative_constraints", {})

        # Nếu có từ phủ định, làm sạch query gốc trước khi vector hóa để không match nhầm từ khóa bị ghét
        clean_query = user_query
        if neg_info.get("has_negation"):
            clean_query = re.sub(
                r"(?:ghét|không thích|không muốn|sợ|tránh|dị ứng|ngán|chán|không mê|không có khiếu|không chịu được|không ưa|đừng)\s+[^,\.;\n]+",
                " ",
                user_query,
                flags=re.IGNORECASE
            )

        # Vectorize câu gốc (đã làm sạch) và văn bản giả định
        vec_query = self._vectorize_query(clean_query)
        vec_hypo = self._vectorize_query(hypo_doc)

        # Trọng số kết hợp: 40% câu hỏi gốc + 60% văn bản giả định HyDE
        combined_vec = 0.4 * vec_query + 0.6 * vec_hypo
        norm = np.linalg.norm(combined_vec)
        if norm > 0:
            combined_vec = combined_vec / norm

        # Tính độ tương đồng cosine
        similarities = np.dot(self.doc_vectors, combined_vec)

        # Áp dụng hình phạt nghiêm khắc đối với các ngành dính ràng buộc phủ định
        excluded_majors = set(neg_info.get("excluded_majors", []))
        if excluded_majors:
            for idx, doc in enumerate(self.docs):
                if doc["code"] in excluded_majors:
                    similarities[idx] = -0.5  # Đẩy xuống đáy bảng xếp hạng

        # Xếp hạng
        effective_k = min(top_k, len(self.docs))
        top_indices = np.argsort(similarities)[::-1][:effective_k]
        
        matches = []
        for idx in top_indices:
            score = float(similarities[idx])
            doc = self.docs[idx]
            matches.append({
                "major_code": doc["code"],
                "major_name": doc["name"],
                "category": doc["category"],
                "holland": doc["holland"],
                "similarity_score": round(score, 4),
                "summary": doc["content"][:160] + "...",
                "keywords": doc["keywords"]
            })

        return {
            "user_query": user_query,
            "domain_detected": domain_detected,
            "hypothetical_document": hypo_doc,
            "negative_constraints": neg_info,
            "top_matches": matches
        }

# Khởi tạo singleton instance
vector_store_instance = VectorStore()
