# 🏗️ **Initial Project Setup — LLMOps Medical Chatbot**

This branch establishes the foundational structure for the **LLMOps Medical Chatbot** project.
It introduces a clean modular application layout, secure environment configuration, and shared utility components for logging and exception handling.

These elements form the backbone for later branches involving medical-domain retrieval, LLM reasoning, and chatbot interfaces.

## 🗂️ **Project Structure**

```text
LLMOPS-MEDICAL-CHATBOT/
├── .venv/                                # Virtual environment
├── .env                                  # Environment variables (HF + Groq API keys)
├── .gitignore                            # Git ignore rules
├── .python-version                       # Python version pin
├── pyproject.toml                        # Project metadata and dependency configuration
├── README.md                             # Root project documentation
├── requirements.txt                      # Python dependencies
├── setup.py                              # Editable install configuration
│
├── data/
│   └── The_GALE_ENCYCLOPEDIA_OF_MEDICINE_SECOND.pdf   # Initial medical knowledge source
│
└── app/                                  # Application package
    ├── __init__.py                       # Marks app directory as a package
    │
    ├── common/                           # Shared utilities for reliability
    │   ├── __init__.py
    │   ├── custom_exception.py           # Context-rich exception handling
    │   ├── logger.py                     # Centralised logging configuration
    │   └── README.md                     # Documentation for common utilities
    │
    ├── config/                           # Configuration and environment loading
    │   ├── __init__.py
    │   ├── config.py                     # Loads environment vars and global settings
    │   └── README.md                     # Documentation for config management
    │
    ├── components/                       # Core chatbot components (to be implemented)
    │   └── __init__.py
    │
    └── templates/                        # HTML templates for the future UI (to be implemented)
```

> 💡 The `.env` file contains sensitive API keys (`HF_TOKEN`, `GROQ_API_KEY`) and must never be committed to version control.

## ⚙️ **What Was Done in This Branch**

1. **Created the base project structure**

   * Added the `app/` package with `common`, `config`, `components`, and `templates`.
   * Introduced initial module placeholders (`__init__.py`) for package cohesion.

2. **Environment and dependency setup**

   * Created a new virtual environment.
   * Added a base `requirements.txt` including LangChain v1 libraries, Groq integration, and supporting packages.

3. **Centralised configuration**

   * Added `.env` for API keys.
   * Implemented `app/config/config.py` to load environment variables and define global paths, model IDs, and chunking parameters.

4. **Reliability utilities**

   * Implemented `custom_exception.py` for structured, well-documented error handling.
   * Implemented `logger.py` for consistent logging across all chatbot modules.
   * Added a README for the `common/` folder documenting usage.

## ✅ **Summary**

This setup branch provides the essential foundation for the Medical Chatbot:

* Modular and scalable project layout
* Secure environment variable handling
* Shared logging and exception modules
* Initial data placed under `data/`
* Ready-made folders for future RAG pipeline, UI, and LLM logic
