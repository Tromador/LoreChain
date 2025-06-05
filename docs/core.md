# 🧠 LC Core Module Documentation

This module provides a session-aware, GPU-accelerated LangChain interface that supports memory via FAISS vectorstore with disk persistence and Hugging Face embeddings. It acts as the processing engine behind the input relay layer, serving as the "brain" of your LangChain-based system.

---

## 📦 Module Structure

```
lc_core/
├── __init__.py              # Public API and singleton state
├── bge_embedding.py         # Embedding wrapper for HuggingFace BGE
├── chain_manager.py         # LangChain chain construction
├── config.py                # Settings (API key, session ID, file paths)
├── memory_manager.py        # Embedding + FAISS memory backend
└── vectorstore/             # Saved FAISS index + metadata (if disk persistence enabled)
```

---

## 🚀 Usage Overview

Import via the public interface:

```python
from lc_core import (
    process_input,
    get_embedding_model,
    get_vectorstore,
    get_memory_manager,
)
```

---

## 🔧 Configuration

Edit `lc_core/config.py` to control runtime behaviour.

| Setting                        | Description                                                           |
|-------------------------------|-----------------------------------------------------------------------|
| `OPENAI_API_KEY`              | Your OpenAI key (used by LangChain `ChatOpenAI`)                      |
| `SESSION_ID`                  | Logical session key for filtering vector memory                       |
| `USE_DISK_PERSISTENCE`        | If `True`, vectorstore will persist to disk                           |
| `FAISS_INDEX_PATH`            | Path to `.faiss` index file                                           |
| `FAISS_DOCSTORE_PATH`         | Path to document store pickle                                         |
| `FAISS_INDEX_METADATA_PATH`   | Path to index metadata pickle                                         |

---

## 🧩 Public Interface (`lc_core/__init__.py`)

### `process_input(user_input: str) -> str`
Processes user input using the current LangChain chain, with session-aware context memory.

- **Input:** plain text string
- **Output:** plain text string (completion)
- **Context retrieval:** based on `SESSION_ID` from config

---

### `get_embedding_model() -> Callable[[List[str]], List[List[float]]]`
Returns the singleton embedding model — callable on list of strings, returns list of embedding vectors.

- Backed by Hugging Face `bge-large-en-v1.5`
- GPU-accelerated via PyTorch + CUDA

---

### `get_vectorstore() -> langchain_community.vectorstores.FAISS`
Returns the shared FAISS vectorstore object (LangChain-compatible).

Supports:

```python
vectorstore.add_documents([Document(...)])

vectorstore.similarity_search(query_str, k=3, filter={"session_id": "..."})

vectorstore.delete(filter={"session_id": "..."})
```

---

### `get_memory_manager() -> VectorStoreMemory`
Returns the memory manager singleton, which encapsulates:

- Embedding model
- FAISS vectorstore
- Save/load lifecycle
- Session-specific filtering

---

## 💾 Persistence API

If `USE_DISK_PERSISTENCE = True` in config:

- Index and metadata are automatically loaded on startup (if present)
- You must explicitly call `get_memory_manager().save()` to persist current state

Example:

```python
from lc_core import get_memory_manager
get_memory_manager().save()
```

This saves the following to disk:

- FAISS index: `index.faiss`
- Docstore: `docstore.pkl`
- Metadata: `index_metadata.pkl`

---

## ⚙️ Chain Behaviour (`chain_manager.py`)

The current implementation builds a `RetrievalQA` chain using:

- `ChatOpenAI()` as the LLM
- LangChain FAISS vectorstore retriever
- `stuff` chain type (append all retrieved docs)
- Pass-through config from `config.py`

No summarisation or condensation yet — all retrieved context is included as-is.

---

## 🧠 Memory Behaviour

- All stored documents are tagged with `{"session_id": SESSION_ID}`
- Retrieval is automatically filtered to match session
- Allows multiple independent conversational contexts

---

## 🧪 Dev Notes

- Designed for Torch CUDA 12.8, `faiss-gpu` built with `numpy>=2`
- No external I/O or UI outside of relay
- Front-end (e.g., `app.py` or `input_form.html`) is responsible for capturing input and calling `process_input()`

---

## 🔐 Security Notes

FAISS disk load uses:

```python
FAISS.load_local(..., allow_dangerous_deserialization=True)
```

This is necessary due to LangChain’s recent pickle safety enforcement. Only use this setting for trusted, local vectorstores.

---

## 📡 Integration Pattern

```python
# From relay or frontend:
from lc_core import process_input

response = process_input("Tell me about the golden idol")
```

---

## 🏁 Summary

| Capability            | Status |
|-----------------------|--------|
| LangChain Chain       | ✅     |
| Hugging Face Embedding| ✅     |
| FAISS GPU Vectorstore | ✅     |
| Session Metadata      | ✅     |
| Disk Persistence      | ✅     |
| Front-end Compatible  | ✅     |
| Callable API Surface  | ✅     |

---
