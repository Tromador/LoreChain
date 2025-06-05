# LoreChain

![Project Status](https://img.shields.io/badge/status-WIP-yellow)

**LangChain-based persistent memory layer for creative projects**  
Built for TTRPG lore, story development, and live session context retention — but adaptable to any domain where structured memory and semantic retrieval matter.

---

## 🧩 Project Overview

**LoreChain** provides:

- 🔁 A modular LangChain interface with vectorstore-based memory
- 🧠 Per-session context management using FAISS + HuggingFace embeddings
- ⚡️ Full GPU acceleration via PyTorch + FAISS-GPU
- 🌐 API interaction with OpenAI (GPT-4.1 or later) using `langchain-openai`
- 🖥️ Web-based input interface (manually typed or programmatically streamed)

Designed for tasks that require long-term knowledge retention, such as:

- 🗺️ Worldbuilding & TTRPG adventure writing
- ✍️ Multi-turn lore development
- 🤖 Assistant-driven live narrative tools

---

## 🚀 Requirements

- Python 3.10+ (tested in WSL Ubuntu)
- Working OpenAI API key (set via config)
- CUDA 12.8+ GPU with PyTorch support (optional but recommended)

---

## ⚠️ NumPy & FAISS Compatibility Warning

> You **must** use a version of FAISS that is compatible with **NumPy 2.x**

### Why?

- LangChain **requires NumPy 2.x**
- Default FAISS builds from PyPI **are compiled against NumPy 1.x**
- Mixing the two will **break your runtime immediately** (segfaults, memory issues, undefined behaviour)

### ✅ Solution

This project assumes a **custom build of `faiss-gpu` compiled from source with NumPy 2.x support**.

We do **not** include a FAISS build — you’ll need to:

- ✅ [Build FAISS from source](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md) with:
  ```bash
  -DFAISS_ENABLE_GPU=ON
  ```
  …and ensure it links against the **same** Python environment where NumPy 2.x is installed.

> ❌ Do **not** downgrade to NumPy 1.x — LangChain will break.

---

## ⚙️ GPU Acceleration

The system is designed to exploit modern GPU hardware:

- HuggingFace `bge-large-en-v1.5` embeddings (very large model)
- FAISS-GPU for vector similarity
- Transcription + embedding can comfortably run in parallel

> On an RTX 5090, we routinely hit <40% GPU load with both Whisper and embedding active.

If you’re running on lower-spec gear, swap in smaller embedding models or use CPU FAISS instead (with appropriate compile flags).

---

## 📁 Project Structure.

<details> <summary><strong> Click to expand </strong></summary>

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
│   │   ├── base.py
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
│   ├── static/              # Reserved for CSS or JS (empty)
│   └── templates/
│       └── input_form.html

```
</details>

---

## 💬 Configuration

Your OpenAI API key is stored here:

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
| Memory Store   | ✅ Complete   | FAISS-GPU with per-session document tags    |
| Embeddings     | ✅ Complete   | HuggingFace BGE-large on GPU                |
| Input Web UI   | ✅ Working    | Manual and scripted input supported         |
| LlamaIndex     | 🚧 Planned    | Lore preloading system (future enhancement) |
| TTS / Output   | 🧪 Prototype  | TTS not yet looped back into LC             |

---

## 📢 Input Source: Discord Chat

You can integrate LoreChain with [**Discord-Transcription-Stack**](https://github.com/Tromador/Discord-Transcription-Stack), which captures clean, diarised chat logs from live Discord voice channels.

That stack is currently using Puppeteer to drive a ChatGPT web session, but will be adapted to use LoreChain directly via API injection in the next dev cycle.

---

## ✨ Future Goals

- LlamaIndex-based lore preload with smart retrieval
- TTS module integration (e.g., Bark or Coqui)
- Multi-user session context handling
- Session switching, tagging, history management

---

## 🤝 Attribution

Built by [Tromador](https://github.com/Tromador), an engineer/game master solving actual problems with LLMs instead of playing prompt-jockey games.

No fluff. No magic. Just real tools, running on real iron.

[![License](https://img.shields.io/github/license/Tromador/LoreChain)](https://github.com/Tromador/LoreChain/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/langchain-enabled-green)](https://github.com/hwchase17/langchain)
[![FAISS](https://img.shields.io/badge/FAISS-GPU--Enabled-brightgreen)](https://github.com/facebookresearch/faiss)
[![Powered by OpenAI](https://img.shields.io/badge/powered%20by-OpenAI-000000?logo=openai&logoColor=white)](https://openai.com)
[![Hugging Face](https://img.shields.io/badge/embeddings-HuggingFace-orange?logo=huggingface&logoColor=white)](https://huggingface.co)

---

## 📜 License
BSD 3-Clause License — Permissive use, with **attribution required**.  

---
