import faiss
import numpy as np
# from backend.resume_extractor import preprocess_resume
from .embeddings import EmbeddingModel
from .profile_loader import load_profile, profile_to_chunks 
from .logger import setup_run_logger
from .resume_extractor import preprocess_resume

class ResumeFAISS:
    """
    Builds a FAISS index over resume chunks once
    and allows semantic search over them.
    """

    def __init__(self, resume_pdf: str=None, logger=None):
        if logger is None:
            class DummyLogger:
                def info(self, *args, **kwargs): pass
            logger = DummyLogger()
        # 1. Extract & preprocess resume
        logger.info("\nRESUME PREPROCESSING STARTED\n")
        logger.info(f"Preprocessing resume: {resume_pdf}")
        
        if(not resume_pdf):
            profile_path = "data/profile.json"
            profile = load_profile(profile_path)   # now passing JSON path
            chunks = profile_to_chunks(profile)
            
        else:
            chunks = preprocess_resume(pdf_path = resume_pdf, logger=logger)

        if not chunks:
            chunks = [{"text":"srkljtgbkrebhg"}] #garbage value to create FAISS index still and not break the system
            
        # 2. Load embedding model
        self.embedder = EmbeddingModel()
        
        # 3. embedding only the text
        texts = [c['text'] for c in chunks]
        embeddings = self.embedder.encode(texts)
        logger.info(f"Generated embeddings for {len(texts)} resume chunks.")


        # 4. Build FAISS index
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # 5. Store raw text
        self.text_store = chunks
        logger.info("FAISS index built successfully.\n")
        return 

    def search(self, topic_objects: list[dict], top_k: int = 5,
        threshold: float = 0.55, resume_path: str = None, logger=None):

        if logger is None:
            class DummyLogger:
                def info(self, *args, **kwargs): pass
            logger = DummyLogger()

        logger.info("\nRESUME SEARCH STARTED INSIDE SEARCH FUNCTION\n")

        if not topic_objects:
            return []

        # --- build queries ---
        queries = [
            topic["topic"] + " " + " ".join(topic.get("keywords", []))
            for topic in topic_objects
        ]

        query_with_prefix = [
            f"search for relevant passages using the keywords: {q}"
            for q in queries
        ]

        logger.info("Generated semantic queries.")
        logger.info(f"Queries:\n{query_with_prefix}")

        # --- embed queries ---
        query_emb = self.embedder.encode(query_with_prefix)
        faiss.normalize_L2(query_emb)

        # --- FAISS search ---
        scores, indices = self.index.search(query_emb, top_k)
        logger.info(f"scores: {scores}\n indices: {indices}")

        results = []

        # iterate topic-wise
        for topic, q_scores, q_indices in zip(topic_objects, scores, indices):

            section_groups = {}
            topic_keywords = [k.lower() for k in topic.get("keywords", [])]

            for score, idx in zip(q_scores, q_indices):

                if idx == -1:
                    continue

                chunk = self.text_store[idx]

                text = chunk["text"]    
                text_lower = text.lower()

                # --- keyword bonus ---
                keyword_bonus = 0
                for kw in topic_keywords:
                    if kw in text_lower:
                        keyword_bonus += 0.05

                final_score = score + keyword_bonus

                if final_score < threshold:
                    continue

                section = chunk.get("section", "GENERAL").upper()
                context = chunk.get("context") or "General"

                if section not in section_groups:
                    section_groups[section] = {}

                if context not in section_groups[section]:
                    section_groups[section][context] = []

                section_groups[section][context].append(text)

            evidence_parts = []

            for section, contexts in section_groups.items():

                section_text = [f"{section.title()}:"]
                counter = 1

                for context, sentences in contexts.items():
                    section_text.append(f"{counter}. {context}")

                    for s in sentences:
                        section_text.append(f"- {s}")

                    counter += 1

                evidence_parts.append("\n".join(section_text))

            if not evidence_parts:
                results.append(["No strong evidence found."])
            else:
                results.append(["\n\n".join(evidence_parts)])

        return results
        
# local test 
if __name__ == "__main__":
    import logging

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    logger = logging.getLogger(__name__)
    
    print("Building FAISS index...")
    faiss_service = ResumeFAISS(logger = logger)
    print("Index ready.\n")
    topic_objects = [
        {
        "topic": "model deployment",
        "keywords": ["deployed","model serving","fastapi","docker","production pipeline"]
        },
        {
        "topic": "feature engineering",
        "keywords": ["feature engineering","feature selection","feature extraction","data preprocessing","feature transformation"]
        }
        ]
    evidence = faiss_service.search(topic_objects = topic_objects, top_k=6, threshold=0.55, logger = logger)
    for priority, ev in zip(topic_objects, evidence):
        print(f"JD Priority: {priority}")
        if ev:
            for i, e in enumerate(ev, 1):
                print(f"{e}")
        else:
            print("  No strong evidence found.")
        print()