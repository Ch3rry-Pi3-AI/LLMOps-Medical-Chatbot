# 🖥️ **Flask Application Layer — LLMOps Medical Chatbot**

This branch introduces the **complete Flask web application layer** for the LLMOps Medical Chatbot.
It transforms the backend RAG pipeline into a fully interactive browser-based chat interface with a clean layout, user-friendly controls, and full integration with the retrieval system.

<p align="center">
  <img src="img/flask/flask_app.gif" alt="Flask Chatbot Demo" width="100%">
</p>

This is the branch where the project becomes a functional medical chatbot that users can interact with directly through the web.

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
    ├── application.py            # NEW: Flask routes, session logic, RAG invocation
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
    │   └── index.html            # NEW: Jinja HTML template for chat UI
    │
    └── static/
        └── style.css             # NEW: Full UI stylesheet
```

## ⚙️ **What Was Implemented in This Branch**

### 🧠 1. `application.py` — Complete Flask Controller

This module now handles:

* Flask app creation
* Session-based message history
* The `nl2br` Jinja filter
* Direct invocation of the RAG retrieval chain
* Error handling and user-facing notifications
* Clean message sanitisation
* GET + POST handling for full chat interaction
* Clear chat functionality

All functions follow your documentation standards:

* NumPy-style docstrings
* Type hints
* Section-level comment blocks
* Intuitive inline explanations

### 🖥️ 2. `index.html` — Full Chat Interface Template

The new HTML template includes:

* Title, subtitle, and online status indicator
* Structured display of user and assistant messages
* Error banners when backend issues occur
* Empty-state instructional messages
* Textarea input with Send and Clear buttons
* Medical disclaimer footer
* Auto-scroll JavaScript for usability

The template is fully documented with clear, readable comments.

### 🎨 3. `style.css` — Complete UI Styling

The stylesheet defines the entire look and feel of the chatbot:

* Centre-aligned card layout
* Gradient header design
* Scrollable chat panel with custom scrollbar
* User and assistant message blocks
* Button styling and hover transitions
* Empty-state styling
* Footer with legal disclaimers
* Accessibility helpers (e.g., `.sr-only`)

It includes a full NumPy-style documentation block and consistent inline comments above each section.

### 🔗 4. Integration With RAG Retrieval Pipeline

This branch successfully attaches the Flask UI to the underlying LCEL RAG chain.
When users submit a medical question:

* The RAG retriever fetches context
* The LLM generates a grounded answer
* The assistant response appears instantly in the chat UI

This brings the entire system together into a cohesive user experience.

## 🧪 **Application Status**

The chatbot now:

* Loads correctly in the browser
* Displays messages cleanly
* Accepts user input
* Generates responses via the RAG chain
* Handles and displays errors gracefully
* Scrolls chat to the most recent message
* Allows the user to clear the conversation at any time

It is fully functional for local usage.

## ✅ **Summary**

This branch delivers the **complete front-end application** of the LLMOps Medical Chatbot:

* Flask backend with well-structured routes
* Fully documented HTML template
* Fully documented CSS stylesheet
* Interactive chat UI
* Working integration with the retrieval-augmented medical answer engine

The project now operates as a full web-based medical chatbot.