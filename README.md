# 🧩 **LLM Loader Component — LLMOps Medical Chatbot**

This branch introduces the **LLM loader component** for the LLMOps Medical Chatbot.
It adds the ability to initialise a Groq-hosted LLM using the `ChatGroq` interface, enabling fast, low-latency inference for medical question-answering using models such as **LLaMA 3.1**.

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
    │   ├── vector_store.py
    │   ├── data_loader.py
    │   └── llm.py                # NEW: Loads Groq-hosted LLMs for inference
    │
    └── templates/
```

> 💡 The `.env` file must remain private, as it contains the `GROQ_API_KEY` used to authenticate with Groq's LLM API.

## ⚙️ **What Was Done in This Branch**

1. **Added the `llm.py` component**

   * Implemented `load_llm()` to initialise a Groq-backed LLM via the LangChain v1 `ChatGroq` wrapper.
   * Configured sensible defaults (`llama-3.1-8b-instant`, `temperature=0.3`, `max_tokens=256`).
   * Integrated logging for full visibility into model loading steps.
   * Added robust exception handling using `CustomException`.

2. **Aligned all imports with the LangChain v1 ecosystem**

   * Adopted the `langchain_groq` package for Groq model loading.
   * Ensured compatibility with the project's existing LangChain v1 components.

3. **Applied full project-wide formatting**

   * File-level documentation
   * NumPy-style docstrings
   * Type hints
   * Section comment blocks
   * Clear explanatory inline comments

4. **Integrated seamlessly with the pipeline**

   * The loaded LLM will be used in the next stage: constructing a retrieval-augmented query answering module.

## 🧪 **LLM Loader Status**

This component is now fully implemented and ready for use during the query-answering stage of the chatbot.
Model loading is logged clearly and includes error tracing through the custom exception system.

No runtime output is included here because the `llm.py` component does not execute a pipeline—its behaviour depends on downstream usage.

## ✅ **Summary**

This branch introduces the Medical Chatbot’s inference layer:

* Groq-hosted LLM loading via LangChain v1
* Clean, modular component ready for integration
* Robust logging and exception management
* Completes the core components needed before building the retrieval + LLM answer generation pipeline
