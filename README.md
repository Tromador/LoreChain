# LoreChain

![Project Status](https://img.shields.io/badge/status-WIP-yellow)

By WIP I mean this readme is already at least somewhat wrong.

"Indentation-based syntax removes the freedom — and replaces it with fragility. Sure, it can look clean… but so does a plate of blancmange until you try to pick it up."
- ChatGPT talking about Python

**LangChain-based persistent memory layer for creative projects**  
Built for TTRPG lore, story development, and live session context retention — but adaptable to any domain where structured memory and semantic retrieval matter.

---

## 🧠 Why This Exists

Most LLM APIs — including OpenAI's — are stateless and short-term by design.  
When working with prewritten transcripts or running multi-hour sessions, you’ll eventually hit context overflow and semantic drift.

**LoreChain addresses this** by:
- Persisting long-term memory across sessions
- Retrieving only what’s relevant via semantic search
- Allowing workflows that depend on continuity, world state, or structured recall

It works equally well for:
- 📜 TTRPG campaigns
- 🛠 Project logs and AARs
- 🧾 Multi-user shared knowledgebases
- 🧑‍🏫 Courseware or onboarding systems

---

## 🧩 Project Overview

**LoreChain** provides:

- 🔁 A modular LangChain interface with vectorstore-based memory
- 🧠 Per-session context management using FAISS + HuggingFace embeddings
- 💾 Disk persistence and session filtering support
- 🌐 API integration with OpenAI (via `langchain-openai`)
- 🖥️ A lightweight Flask-based input UI for manual or automated entry

---

## 🚀 Requirements

- Python 3.10+ (tested in WSL Ubuntu)
- Working OpenAI API key (defined in config)
- A FAISS build compiled against **NumPy 2.x**
- Optionally: CUDA-enabled GPU for faster embedding

> This project was tested on a GPU-enabled system using large embedding models, but will run correctly on CPU with smaller models.  
> Embedding and vector search may be slower, but all functionality remains intact.

---

## ⚠️ NumPy & FAISS Compatibility

> You **must** use a version of FAISS that is compatible with **NumPy 2.x**

LangChain now requires NumPy 2. Default FAISS builds from PyPI are compiled against NumPy 1.x.  
Mixing the two will result in segmentation faults or undefined behaviour.

### ✅ Solution

Build FAISS from source against NumPy 2.x with GPU enabled (if desired):

```bash
-DFAISS_ENABLE_GPU=ON
```

Do **not** downgrade NumPy — LangChain will break.

---

## ⚙️ GPU Acceleration (Optional)

If running on a CUDA-capable GPU, LoreChain supports:
- HuggingFace `bge-large-en-v1.5` embeddings (via `sentence-transformers`)
- FAISS-GPU for fast vector similarity
- Parallel processing alongside other tools like Whisper

> On an RTX 5090, typical usage (embedding + transcript processing) uses under 40% GPU load.  
> CPU fallback is supported, just slower. You can downsize the model if needed.

---

## 📁 Project Structure

<details><summary><strong>Click to expand</strong></summary>

```
LoreChain/
├── README.md
├── docs/
│   ├── core.md
│   ├── input_interface.md
│   └── memory.md
├── lc_input_interface/
│   ├── app.py
│   ├── langchain_relay.py
│   ├── input_providers/
│   │   ├── __init__.py
│   │   ├── live.py
│   │   └── manual.py
│   ├── lc_core/
│   │   ├── __init__.py
│   │   ├── bge_embedding.py
│   │   ├── chain_manager.py
│   │   ├── config.py
│   │   ├── config_sample.py
│   │   ├── memory_manager.py
│   │   └── vectorstore/
│   │       ├── index.faiss
│   │       └── index.pkl
│   ├── lc_memory/
│   │   ├── __init__.py
│   │   ├── memory_store.py
│   │   └── session_manager.py
│   ├── static/
│   └── templates/
│       └── input_form.html
```

</details>

---

## 💬 Configuration

OpenAI API key and runtime parameters are defined in:

```python
# lc_core/config.py
OPENAI_API_KEY = "<your-key-here>"
```

This file is `.gitignore`d by default.

---

## ✅ Current Capabilities

| Module         | Status       | Notes                                       |
|----------------|--------------|---------------------------------------------|
| LangChain Core | ✅ Complete   | OpenAI + vectorstore memory                 |
| Memory Store   | ✅ Complete   | FAISS with per-session document tags        |
| Embeddings     | ✅ Complete   | HuggingFace BGE-large or custom model       |
| Input Web UI   | ✅ Working    | Manual and scripted input supported         |
| LlamaIndex     | 🚧 In Progress| Lore ingestion system (file-based preload)  |
| TTS / Output   | 🧪 Prototype  | TTS pipeline under evaluation               |

---

## 📢 Discord Input (Optional Integration)

You can optionally integrate LoreChain with the [**Discord-Transcription-Stack**](https://github.com/Tromador/Discord-Transcription-Stack), which captures diarised voice transcripts from Discord voice channels.

Currently, this stack uses Puppeteer to drive a ChatGPT session — but is designed to work with LoreChain via API relay in future revisions.

---

## ✨ Future Goals

- LlamaIndex-based lore ingestion and file management
- TTS (e.g. Bark, Coqui) for interactive playback
- Multi-user memory separation and switching
- Lore editing + AAR summarisation workflows

---

## 🤝 Attribution

Built by [Tromador](https://github.com/Tromador), a game master and engineer solving real continuity problems with LLMs — not prompt games.

No hype. No marketing. Just real tools, running on real infrastructure.

[![License](https://img.shields.io/github/license/Tromador/LoreChain)](https://github.com/Tromador/LoreChain/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/langchain-enabled-green)](https://github.com/hwchase17/langchain)
[![FAISS](https://img.shields.io/badge/FAISS-GPU--Optional-brightgreen)](https://github.com/facebookresearch/faiss)
[![Powered by OpenAI](https://img.shields.io/badge/powered%20by-OpenAI-000000?logo=openai&logoColor=white)](https://openai.com)
[![Hugging Face](https://img.shields.io/badge/embeddings-HuggingFace-orange?logo=huggingface&logoColor=white)](https://huggingface.co)

---

## 📜 License

BSD 3-Clause License — permissive use, **attribution required**.

---
