# lc_memory/memory_store.py

from typing import List
from langchain.schema import Document
import uuid

def store_memory(session_id: str, text: str, embedding_model=None, vectorstore=None) -> None:
    """
    Embed `text` and store it in the FAISS vectorstore with session_id metadata.
    Assigns a unique document ID to allow future deletion by session filter.
    """
    if embedding_model is None or vectorstore is None:
        raise ValueError("embedding_model and vectorstore must be passed explicitly to avoid circular import")

    doc = Document(
        page_content=text,
        metadata={"session_id": session_id},
        id=str(uuid.uuid4())  # Critical for delete(filter=...) to work
    )
    vectorstore.add_documents([doc], embedding=embedding_model)

def retrieve_context(session_id: str, query_text: str, k: int = 4, embedding_model=None, vectorstore=None) -> List[str]:
    if embedding_model is None or vectorstore is None:
        raise ValueError("embedding_model and vectorstore must be passed explicitly to avoid circular import")

    results = vectorstore.similarity_search(
        query=query_text,
        k=k,
        filter={"session_id": session_id}
        # ← REMOVE embedding=... (it's not valid here)
    )

    return [doc.page_content for doc in results]

