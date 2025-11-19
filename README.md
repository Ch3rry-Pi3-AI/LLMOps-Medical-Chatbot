# 📄 **PDF Loader Component — LLMOps Medical Chatbot**

This branch introduces the **PDF ingestion component** for the LLMOps Medical Chatbot.
It adds functionality for loading medical PDF files and converting them into text chunks for downstream retrieval and LLM reasoning.

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
    │   └── pdf_loader.py                # NEW: Loads PDFs and creates text chunks
    │
    └── templates/
```

> 💡 The `.env` file holds sensitive API keys and should never be committed to version control.

## ⚙️ **What Was Done in This Branch**

1. **Introduced the `pdf_loader.py` component**

   * Implemented functionality to load PDFs from the `data/` directory.
   * Added text-chunking using LangChain v1’s `RecursiveCharacterTextSplitter`.
   * Integrated logging and custom exception handling for robust ingestion.

2. **Aligned imports with LangChain v1 ecosystem**

   * Updated all loaders, splitters, and document classes to their correct v1 locations.
   * Ensured compatibility with `langchain-community`, `langchain-text-splitters`, and `langchain-core`.

3. **Structured the file in the project style**

   * Included file-level documentation.
   * Added NumPy-style function docstrings.
   * Added type hints and intuitive inline comments.
   * Used section comment blocks for readability.

## ✅ **Summary**

This branch adds the first major functional component to the Medical Chatbot:

* PDF ingestion using modern LangChain v1 modules
* Robust logging and exception handling
* Clean, modular placement inside `app/components/`
* Fully prepared data chunks for future embedding and retrieval steps
