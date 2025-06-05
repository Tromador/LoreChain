# lc_core/memory_manager.py

import os
import faiss
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from .bge_embedding import BGEEmbedding
from .config import (
    EMBEDDING_MODEL_NAME,
    FAISS_INDEX_PATH,
    USE_DISK_PERSISTENCE,
)

class VectorStoreMemory:
    def __init__(self):
        self.model = BGEEmbedding(EMBEDDING_MODEL_NAME)

        if USE_DISK_PERSISTENCE and os.path.exists(FAISS_INDEX_PATH):
            self.vectorstore = FAISS.load_local(
                folder_path=os.path.dirname(FAISS_INDEX_PATH),
                embeddings=self.model,
                index_name=os.path.basename(FAISS_INDEX_PATH).split(".")[0],
                allow_dangerous_deserialization=True
            )
        else:
            # Bootstrap vectorstore using dummy doc, then remove it by ID
            dummy_doc = Document(
                page_content="bootstrap",
                metadata={"session_id": "__bootstrap__"}
            )
            self.vectorstore = FAISS.from_documents([dummy_doc], embedding=self.model)
            ids = self.vectorstore.add_documents([dummy_doc])
            self.vectorstore.delete(ids)

    def add(self, texts, session_id: str):
        print(f"[+] Adding {len(texts)} texts to vectorstore for session: {session_id}")
        docs = [Document(page_content=text, metadata={"session_id": session_id}) for text in texts]
        self.vectorstore.add_documents(docs)
        print(f"[✓] Added to vectorstore. Current total: {self.vectorstore.index.ntotal}")


    def search(self, query: str, k: int, session_id: str):
        return self.vectorstore.similarity_search(query, k=k, filter={"session_id": session_id})

    def delete(self, session_id: str):
        # No-op until we wire in proper ID tracking
        # Can implement if/when we need to clear sessions programmatically
        pass

    def save(self):
        if not USE_DISK_PERSISTENCE:
            return
        print(f"[*] Vectorstore index size: {self.vectorstore.index.ntotal} entries")
        self.vectorstore.save_local(folder_path=os.path.dirname(FAISS_INDEX_PATH))
        print("[✓] Save complete.")
