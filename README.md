# 🧩 **Vector Store Component — LLMOps Medical Chatbot**

This branch introduces the **vector store component** for the LLMOps Medical Chatbot.
It enables the creation, saving, and loading of a FAISS vector store built from embedded medical text chunks, forming the foundation of the chatbot’s retrieval system.

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
    ├── __init__.py
    │
    ├── common/
    │   ├── __init__.py
    │   ├── custom_exception.py
    │   ├── logger.py
    │   └── README.md
    │
    ├── config/
    │   ├── __init__.py
    │   ├── config.py
    │   └── README.md
    │
    ├── components/
    │   ├── __init__.py
    │   ├── pdf_loader.py
    │   ├── embeddings.py
    │   └── vector_store.py              # NEW: Loads, creates, and saves the FAISS vector store
    │
    └── templates/
```

> 💡 The `.env` file must remain private, as it contains sensitive API keys required for model access.

## ⚙️ **What Was Done in This Branch**

1. **Added the `vector_store.py` component**

   * Implemented functions to load an existing FAISS vector store and to create/save a new one.
   * Integrated the component with the project’s embedding model loader.
   * Ensured robust error handling using `CustomException`.

2. **Implemented LangChain v1-compliant functionality**

   * Adopted `langchain-community` for FAISS vector store utilities.
   * Ensured compatibility with v1 ecosystem imports (`langchain_core.documents`, `langchain_huggingface`, etc.).

3. **Applied full project-wide formatting and structure**

   * File-level documentation
   * NumPy-style function docstrings
   * Type hints
   * Section comment blocks
   * Clear inline comments for readability

## ✅ **Summary**

This branch adds the Medical Chatbot’s vector store layer:

* FAISS vector store loading, saving, and creation
* Full compatibility with the LangChain v1 ecosystem
* Clean integration with the embeddings and PDF loader components
* Forms the third major functional component of the chatbot pipeline
