# 🖥️ **Flask Application Layer — LLMOps Medical Chatbot**

This branch introduces the **full Flask web application layer** for the LLMOps Medical Chatbot.
It connects the previously completed RAG retrieval system to a clean, modern, user-friendly browser interface using Flask, Jinja templates, and a fully styled CSS layout.

This is the first branch where the chatbot becomes a complete interactive web app.

## 🗂️ **Project Structure (Updated)**

```text
LLMOPS-MEDICAL-CHATBOT/
├── .venv/
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.py
│
├── data/
│   └── The_GALE_ENCYCLOPEDIA_OF_MEDICINE_SECOND.pdf
│
└── app/
    ├── application.py            # NEW: Full Flask app + routes + session logic
    │
    ├── common/
    │   ├── custom_exception.py
    │   └── logger.py
    │
    ├── config/
    │   └── config.py
    │
    ├── components/
    │   ├── pdf_loader.py
    │   ├── embeddings.py
    │   ├── vector_store.py
    │   ├── data_loader.py
    │   ├── llm.py
    │   └── retriever.py
    │
    ├── templates/
    │   └── index.html            # NEW: Jinja-based chat UI template
    │
    └── static/
        └── style.css             # NEW: Full custom CSS for the chat interface
```

## ⚙️ **What Was Implemented in This Branch**

### 🧠 1. **Completed `application.py` — the Flask Controller**

The Flask module now includes:

* A full HTTP route for chat interaction
* User message handling through Flask session storage
* Assistant replies generated via the RAG chain
* A safe `nl2br` Jinja filter for newline formatting
* Error handling with user-facing messages
* Clean message sanitisation
* Clear and documented helper functions

All functions include:

* NumPy-style docstrings
* Type hints
* Section headers
* Clean, intuitive inline comments

### 🖥️ 2. **Created `index.html` — the Chat UI Template**

The new HTML template provides:

* A fully structured chat interface
* User and assistant message display
* Online status indicator
* Clear error banners
* Textarea input panel
* Example prompts for empty state
* Auto-scrolling behaviour
* Medical disclaimer footer

The template is thoroughly documented and uses your preferred Jinja structure.

### 🎨 3. **Created `style.css` — the Chat Interface Styling**

A complete, modern UI theme was implemented:

* Centre-aligned card layout
* Gradient header with status indicator
* Scrollable chat container
* Message blocks with clean role labels
* Input panel with styled textarea and buttons
* Alerts, empty states, and footer design
* Accessibility helpers (e.g., `.sr-only`)

The file includes:

* A full NumPy-style docstring at the top
* Inline comments above each block
* Clear sectioning for readability

### 🔗 4. **Full Integration With RAG Pipeline**

The web interface now connects directly to the RAG retrieval chain created in earlier branches.
When users enter a question, the following pipeline executes:

* Flask receives the input
* `retriever.py` RAG chain is invoked
* Context-aware medical answer is generated
* Result is displayed in a structured UI

This marks the first fully interactive version of the chatbot.

## 🧪 **Application Status**

The Flask UI launches successfully and:

* Stores chat histories per session
* Renders messages cleanly
* Displays assistant responses correctly
* Handles errors gracefully
* Scrolls automatically to the newest message
* Supports clearing the conversation

The app is now fully functional for local testing.

## ✅ **Summary**

This branch delivers the **complete user-facing interface** of the LLMOps Medical Chatbot:

* Fully implemented Flask backend (`application.py`)
* Clean, modern HTML template (`index.html`)
* Beautifully styled CSS (`style.css`)
* Integration with the RAG retrieval system

This completes the transition from a backend-only RAG pipeline to a fully interactive web-based medical chatbot.
