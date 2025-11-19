# 🧬 **Embedding Model Component — LLMOps Medical Chatbot**

This branch introduces the **embedding model component** for the LLMOps Medical Chatbot.
It adds support for generating text embeddings using a HuggingFace sentence-transformer model, which is required for building the vector store and enabling semantic search during medical question-answering.

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
    │   └── embeddings.py                # NEW: Initialises the HuggingFace embedding model
    │
    └── templates/
```

> 💡 The `.env` file must remain private, as it contains sensitive API keys required for model access.

## ⚙️ **What Was Done in This Branch**

1. **Added the `embeddings.py` component**

   * Implemented `get_embedding_model()` to load a HuggingFace transformer for embedding text chunks.
   * Integrated the component with the project’s logging and custom exception system.
   * Ensured the implementation follows the project’s formatting conventions:

     * File-level docstring
     * NumPy-style function docstrings
     * Type hints
     * Section comment blocks
     * Clear inline comments

2. **Updated imports to LangChain v1 standards**

   * Adopted `langchain-huggingface` for the embedding wrapper.
   * Ensured compatibility with the current LangChain v1 ecosystem.

3. **Prepared the embedding layer for downstream retrieval**

   * Output model instance is ready for use in vector store generation.
   * Forms the second major functional piece of the chatbot pipeline.

## ✅ **Summary**

This branch adds the Medical Chatbot’s embedding layer:

* HuggingFace embedding model initialisation
* Fully structured error handling and logging
* Modern, v1-compatible LangChain imports
* Seamless integration with the existing components folder
