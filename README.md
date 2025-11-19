# 🧩 **Vector Store Pipeline — LLMOps Medical Chatbot**

This branch introduces the **full vector store pipeline** for the LLMOps Medical Chatbot.
It connects all previously implemented components—PDF loading, text chunking, embeddings, and vector store creation—into a complete end-to-end process for building the FAISS vector index used during medical question-answering.

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
    │   └── data_loader.py                    # NEW: End-to-end vector store generation workflow
    │
    └── templates/
```

> 💡 The `.env` file must remain private, as it contains sensitive API keys required for model access.

## ⚙️ **What Was Done in This Branch**

1. **Added the `data_loader.py` component**

   * Introduced a unified function `process_and_store_pdfs()` that orchestrates:

     * PDF loading
     * Text chunking
     * Embedding model initialisation
     * FAISS vector store creation and saving
   * Added logging at every stage for full transparency and easier debugging.

2. **Ensured full compatibility with the LangChain v1 ecosystem**

   * Uses `langchain_community.vectorstores.FAISS`
   * Uses `langchain_huggingface` for embeddings
   * Uses `langchain_text_splitters` and `langchain_core.documents`

3. **Implemented consistent project-wide formatting**

   * File-level documentation
   * NumPy-style function docstrings
   * Type hints
   * Section comment blocks
   * Intuitive inline comments

4. **Integrated with existing components**

   * Reuses `pdf_loader.py`, `embeddings.py`, and `vector_store.py` cleanly.
   * Pipeline is modular and can be triggered from CLI or scripts.

## 🧪 **Pipeline Execution Output**

Running:

```
python app/components/data_loader.py
```

Produced the following log output:

```
2025-11-19 11:18:42,416 - INFO - Starting vector store creation pipeline
2025-11-19 11:18:42,416 - INFO - Loading PDF files from: data/
2025-11-19 11:19:00,799 - INFO - Successfully loaded 759 PDF documents.
2025-11-19 11:19:00,799 - INFO - Splitting 759 documents into text chunks
2025-11-19 11:19:01,028 - INFO - Generated 7080 text chunks from input documents
2025-11-19 11:19:01,030 - INFO - Generating a new FAISS vector store from text chunks
2025-11-19 11:19:01,030 - INFO - Initialising HuggingFace embedding model
2025-11-19 11:19:03,324 - INFO - HuggingFace embedding model loaded successfully
2025-11-19 11:21:14,924 - INFO - Saving FAISS vector store to disk
2025-11-19 11:21:14,987 - INFO - FAISS vector store saved successfully.
2025-11-19 11:21:14,992 - INFO - Vector store created successfully
```

## ✅ **Summary**

This branch completes the ingestion and vectorisation stage of the Medical Chatbot:

* Fully automated pipeline for building the FAISS vector store
* Modular integration of all previously implemented components
* Clear logging and robust exception handling
* 759 documents processed → 7080 chunks embedded → FAISS index created successfully

With the vector store now complete, the next stage will focus on **query retrieval and LLM-based medical question answering**.
