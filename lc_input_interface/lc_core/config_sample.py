# lc_core/config.py

# Add your OpenAI API Key and rename to config.py
OPENAI_API_KEY = "<INSERT_YOUR_API_KEY_HERE>"

# Default session ID (used when no session ID is provided at runtime)
DEFAULT_SESSION_ID = "test_session_01"

# Embedding model name (Hugging Face)
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"

# FAISS index path for optional persistence
FAISS_INDEX_PATH = "lc_core/vectorstore/index.faiss"
FAISS_DOCSTORE_PATH = "lc_core/vectorstore/docstore.pkl"
FAISS_INDEX_METADATA_PATH = "lc_core/vectorstore/index_metadata.pkl"

# Optional: Set to True to enable save/load of vectorstore
USE_DISK_PERSISTENCE = True


 