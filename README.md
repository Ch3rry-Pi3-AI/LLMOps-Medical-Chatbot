# 🔍 **RAG Retriever Component — LLMOps Medical Chatbot**

This branch introduces the **retriever component** for the LLMOps Medical Chatbot.
It implements the complete Retrieval-Augmented Generation (RAG) chain using the **LangChain v1 Expression Language (LCEL)**, replacing all deprecated `langchain.chains` APIs with modern runnable-based composition.

The RAG chain ties together the FAISS vector store retriever, the Groq-hosted LLM, and a custom medical safety-focused prompt to produce concise, context-grounded medical answers.

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
    │   ├── llm.py
    │   └── retriever.py            # NEW: Builds the LCEL RAG retrieval + LLM pipeline
    │
    └── templates/
```

> 💡 The `.env` file must remain private, as it contains the `GROQ_API_KEY` used to authenticate with Groq’s LLM API.

## ⚙️ **What Was Done in This Branch**

1. **Added the `retriever.py` component**

   * Implemented a fully LangChain v1-compliant RAG pipeline.
   * Replaced all deprecated `langchain.chains` functionality with:

     * `RunnablePassthrough`
     * LCEL dictionary routing
     * `ChatPromptTemplate`
     * `StrOutputParser`
   * Constructed a clean LCEL pipeline:

     ```
     {
         "context": retriever,
         "question": RunnablePassthrough(),
     }
     | prompt
     | llm
     | StrOutputParser()
     ```

2. **Created a custom medical prompt**

   * Ensures context-grounding only.
   * Limits answers to 2–3 lines.
   * Instructs the model not to hallucinate.

3. **Integrated all core components**

   * Loads FAISS vector store via `vector_store.py`
   * Loads Groq LLM via `llm.py`
   * Produces a reusable, callable RAG chain for downstream inference.

4. **Applied full project-standard formatting**

   * File-level documentation
   * NumPy-style function docstrings
   * Type hints
   * Section comment blocks
   * Clear, intuitive inline comments

## 🧪 **RAG Chain Status**

The LCEL RAG chain builds successfully and returns a runnable that accepts a user question and outputs a final, parsed medical answer.

All deprecated `langchain.chains` imports have been fully removed.

## ✅ **Summary**

This branch completes the Medical Chatbot’s retrieval-and-reasoning layer:

* Full LangChain v1 LCEL RAG chain
* Safe, concise, context-only medical prompt
* Integration of retriever + LLM into a unified runnable
* Foundation for the final UI or API-based chatbot interface
