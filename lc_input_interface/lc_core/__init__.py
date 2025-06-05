# lc_core/__init__.py

from .memory_manager import VectorStoreMemory
from .chain_manager import ChainManager
from .config import DEFAULT_SESSION_ID

from lc_memory import store_memory  # ← Sub-Task 3 injection

_memory_manager = VectorStoreMemory()
_chain_manager = ChainManager(_memory_manager)

def process_input(user_input: str, session_id: str = None) -> str:
    sid = session_id or DEFAULT_SESSION_ID

    # Search context
    context_docs = _memory_manager.search(user_input, k=5, session_id=sid)

    # Run input through chain
    result = _chain_manager.run(user_input)

    # Store conversation to memory (via Sub-Task 3)
    store_memory(
        sid,
        f"User: {user_input}\nAI: {result}",
        embedding_model=_memory_manager.model,
        vectorstore=_memory_manager.vectorstore
    )

    return result

def get_embedding_model():
    return _memory_manager.model

def get_vectorstore():
    return _memory_manager.vectorstore

def get_memory_manager():
    return _memory_manager

def save_memory():
    _memory_manager.save()

__all__ = [
    "process_input",
    "get_embedding_model",
    "get_vectorstore",
    "get_memory_manager",
    "save_memory"
]
