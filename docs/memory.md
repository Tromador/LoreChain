# Sub-Task 3: Session-Based Semantic Memory (LangChain + FAISS)

This module provides a session-scoped semantic memory interface using vector embeddings and FAISS-backed retrieval via LangChain.

It is designed for integration with a modular LLM pipeline (e.g., `lc_core`), but operates independently and expects injected dependencies to avoid circular imports.

---

## 📁 Module Layout

```
lc_memory/
├── __init__.py            # Public API entrypoints
├── memory_store.py        # Handles storage and retrieval of memory vectors
├── session_manager.py     # Manages session-level memory deletion
```

---

## 🔌 Public API

### `store_memory(session_id: str, text: str, *, embedding_model, vectorstore) -> None`

Stores a text chunk into the vectorstore, embedding it and tagging with the session ID.

#### Parameters:
- `session_id`: A string used to tag the memory for future retrieval/deletion
- `text`: The memory content (e.g., a concatenated prompt/response pair)
- `embedding_model`: A callable embedding function `[str] -> [vector]`
- `vectorstore`: A LangChain `FAISS` object (not raw `faiss.Index`)

#### Example:
```python
store_memory("chat-123", "User: Hi\nAI: Hello!", embedding_model=model, vectorstore=vs)
```

---

### `retrieve_context(session_id: str, query_text: str, k: int = 4, *, embedding_model, vectorstore) -> List[str]`

Returns the top-k semantically similar memory entries for a given query, filtered to the specified session.

#### Parameters:
- `session_id`: Only documents tagged with this ID are considered
- `query_text`: The query to search for semantically similar memories
- `k`: The number of top matches to return (default: 4)
- `embedding_model`: Same model used to store vectors
- `vectorstore`: Shared FAISS vectorstore instance

#### Returns:
- `List[str]`: A list of `page_content` strings (most relevant first)

#### Example:
```python
results = retrieve_context("chat-123", "How does LangChain work?", k=3, embedding_model=model, vectorstore=vs)
```

---

### `reset_session(session_id: str) -> None`

Deletes all documents from the vectorstore tagged with the given `session_id`.

#### Parameters:
- `session_id`: The session tag to delete

#### Notes:
- If no matching documents are found, this is treated as a no-op.
- Requires that stored documents were inserted with unique IDs (handled automatically by `store_memory()`)

#### Example:
```python
reset_session("chat-123")
```

---

## 🧱 Integration Contract

You **must provide**:

- A **callable embedding model** (e.g., from Hugging Face or `sentence-transformers`)
- A **LangChain-compatible FAISS vectorstore**, created like this:
```python
from langchain_community.vectorstores import FAISS
vectorstore = FAISS(embedding_function=model, index=faiss.IndexFlatL2(d))
```

The memory module **must not import from lc_core** directly.  
Instead, `lc_core` is expected to inject dependencies by calling:

```python
from lc_memory import store_memory

store_memory(session_id, text, embedding_model=model, vectorstore=vs)
```

---

## 🧪 Testing & Diagnostics

A test script (`test_sb3.py`) can be used to verify:

- `reset_session()` clears memory
- `store_memory()` inserts correctly
- `retrieve_context()` returns semantically correct matches

Ensure that documents are stored with `id=str(uuid.uuid4())` to allow deletion via metadata.

---

## 🧠 Behaviour Summary

| Capability         | Supported |
|--------------------|-----------|
| Session Isolation  | ✅         |
| Vector Embedding   | ✅         |
| Semantic Retrieval | ✅         |
| Metadata Filtering | ✅         |
| Memory Deletion    | ✅         |
| Disk Persistence   | Delegated to core (optional) |

---

## 🔐 Constraints

- Memory is **session-scoped** via `"session_id"` in document metadata
- No assumptions about prompt format — store raw strings
- No disk persistence logic is implemented in this module; handled externally

---

## 🧼 Future Improvements

- Add token-count estimation for retrieved context
- Return similarity scores for diagnostics
- CLI: `inspect_session(session_id)`, `list_sessions()`, `prune_sessions(...)`

---

## 📎 Dependencies

- `langchain-community`
- `faiss-gpu`
- `transformers` or `sentence-transformers`
- Python ≥ 3.8

