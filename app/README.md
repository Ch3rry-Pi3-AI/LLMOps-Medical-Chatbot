# 📁 `app/` Folder — Core Application Overview

The `app/` directory contains the backend logic, retrieval pipeline components, configuration modules, utility tools, and front-end assets for the AI Medical Chatbot. It represents the entire Flask application layer, including the RAG system, templates, static files, and support modules. This folder is the operational core of the project.

## 📦 Folder Structure

```
app/
├── application.py
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
│   └── index.html
│
└── static/
    └── style.css
```

## 🧠 `application.py` — Main Flask Module

This is the central entrypoint for the chatbot’s web interface.
It handles:

* Creating the Flask application
* Managing sessions and message history
* Applying Jinja filters
* Rendering templates
* Invoking the RAG question-answering chain
* Handling errors and clearing chats

All HTTP routes originate here.

## 🧰 `common/` — Shared Utilities

### `custom_exception.py`

Defines a unified exception class used across modules. It attaches helpful context such as file name, line number, and traceback details, making debugging clearer and more structured.

### `logger.py`

Provides the project's centralised logging setup. Ensures consistent logging behaviour for all components including ingestion, vector store operations, and the LLM pipeline.

## ⚙️ `config/` — Configuration Management

### `config.py`

Holds configuration values including environment variables, API keys, model identifiers, vector store directories, and project constants. Separates configuration from application logic for maintainability.

## 🧩 `components/` — RAG Pipeline Modules

These modules form the core intelligence of the chatbot. They build the embedding pipeline, vector store, document ingestion, large language model, and retrieval chain.

### `pdf_loader.py`

Loads PDFs, extracts text, splits content, and prepares documents for embedding.

### `embeddings.py`

Initialises the embedding model used for vector representations of text.

### `vector_store.py`

Creates, loads, and manages the vector database (FAISS, Chroma, etc.), enabling similarity search for retrieval.

### `data_loader.py`

Runs the end-to-end ingestion workflow, combining loaders, embeddings, and vector store creation.

### `llm.py`

Initialises the LLM model (Groq, LLaMA, etc.). Configures generation parameters such as temperature, token limits, and API credentials.

### `retriever.py`

Builds the complete retrieval-augmented generation chain using LangChain modules. Combines prompts, retriever, LLM, and output parsing into a callable QA pipeline.

## 🎨 `templates/` — HTML Templates

Contains the rendered HTML interfaces for the chatbot.
Currently includes:

* `index.html` which defines the layout and dynamic rendering of chat messages, errors, input fields, and disclaimers.

## 🎨 `static/` — Front-End Assets

Contains resources served directly to the browser.
Includes:

* `style.css` for full visual styling of the interface
* Any future images, icons, or client-side scripts

## Summary

The `app/` directory brings together the entire stack for the AI Medical Chatbot.
It contains:

* Flask web server
* Full RAG retrieval pipeline
* Utilities for logging and exception handling
* Configuration management
* HTML templates and CSS styling

Everything the application needs—from ingestion to retrieval to UI rendering—is organised within this folder.