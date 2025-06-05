# LC Input Interface Module (Revised)

## 📖 Overview
A modular input interface for LangChain Supervisor, designed to:
- Accept **freeform text** or **file uploads** (.txt/.jsonl/.md).
- Validate and pass input to **LangChain Core** via a clean, pluggable relay interface.
- Display LangChain Core output in plain text, scrollable and refreshable.

---

## 🏗 Folder Structure
```
lc_input_interface/
├── app.py                        # Flask app with input form and relay integration
├── input_providers/
│   ├── __init__.py               # Marks input_providers as a package
│   ├── base.py                   # InputProvider interface
│   ├── manual.py                 # ManualInputProvider (text/file)
│   └── live.py                   # LiveInputProvider (stub)
├── langchain_relay.py            # Modular relay to LangChain Core (dummy logic)
├── templates/
│   └── input_form.html           # Web form with scrollable output and error display
├── static/                       # (optional) static files (currently unused)
└── README.md                     # This documentation
```

---

## 🚀 Usage Instructions

### 1️⃣ Setup Environment
```bash
cd ~/API_Injector/lc_input_interface
python3 -m venv .venv
source .venv/bin/activate
pip install Flask
```

### 2️⃣ Run the Flask App
```bash
python3 app.py --mode text
```

### 3️⃣ Access the Interface
Open `http://127.0.0.1:5000/` in your browser.

---

## 📦 Input Modes

### 🔹 Manual Input (Web Form)
- Enter text directly or upload `.txt`, `.jsonl`, or `.md` files.
- Output displayed with scrolling support.

### 🔹 Live Input (Stub)
- `LiveInputProvider` placeholder for pseudo-realtime log input.
- Currently not implemented.

---

## 🔗 Relay Module (`langchain_relay.py`)

### Interface:
- **process_input(input_text) -> str**  
  Accepts input text and returns output.  
- **get_output() -> str or None**  
  Optional retrieval of last processed output.

### Dummy Implementation:
For now:
```
LangChain Core not yet implemented.
Received input:
<your input>
```

Replace with real LangChain Core logic when ready.

---

## 🎨 Features
- Input validation: non-empty, max size 1MB, supported formats.
- Error handling: clear messages for bad input.
- Scrollable output display for large responses.
- Modular relay design, easily swappable.

---

## 🚨 Constraints
- No LangChain Core logic implemented here.
- Minimal UI/UX—focused on functionality and modularity.

---

## 🔧 Next Steps
- Replace `langchain_relay.py` logic with real LangChain Core integration.
- Decide on API or direct function call for processing.
- Optional: Enhance live input and input sanitization.

---

