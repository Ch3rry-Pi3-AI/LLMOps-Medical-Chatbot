# 🐳 **Dockerisation Layer — LLMOps Medical Chatbot**

This branch introduces **Docker containerisation** for the LLMOps Medical Chatbot.
It packages the entire Flask application, RAG pipeline, and supporting modules into a lightweight Python 3.12 container, enabling consistent deployment across all environments including local development, servers, and Kubernetes.

By completing this step, the chatbot is now fully portable and can run anywhere Docker is supported.

## 🗂️ **Project Structure (Updated)**

```text
LLMOPS-MEDICAL-CHATBOT/
├── Dockerfile                 # NEW: Fully documented Python 3.12 Dockerfile
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── setup.py
├── data/
│   └── The_GALE_ENCYCLOPEDIA_OF_MEDICINE_SECOND.pdf
└── app/
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

## ⚙️ **What Was Implemented in This Branch**

### 🐍 1. Switched Base Image to `python:3.12-slim`

The project now uses a lightweight, secure Python 3.12 environment.
The base image was updated from 3.10 to 3.12 to match your current local environment and to ensure long-term support.

### ⚡ 2. Added Full Dockerfile With Documentation

A fully documented production-ready Dockerfile was created featuring:

* Python 3.12-slim parent image
* Disabled `.pyc` bytecode generation
* Unbuffered Python output for clean logs
* Build tools installation (`build-essential`, `curl`)
* Project copied into `/app`
* `pip install -e .` for editable installs
* Port 5000 exposed for Flask
* Launch command:

  ```
  CMD ["python", "app/application.py"]
  ```

All instructions follow best practices and include concise inline comments and a NumPy-style header documentation block.

### 📦 3. Project Prepared for Containerised Execution

The entire application can now run inside Docker with a single command:

```
docker build -t medical-chatbot .
docker run -p 5000:5000 medical-chatbot
```

This ensures:

* Identical environments across development and deployment
* Isolation from system Python configurations
* Easy compatibility with CI/CD pipelines and platforms like Kubernetes

### 🧹 4. Clean Build Context and Stable Layering

The Dockerfile minimises image layers, cleans up APT cache, and avoids storing pip cache to keep the container small and efficient.

## 🧪 **Dockerisation Status**

The container builds correctly and runs the chatbot with full UI functionality:

* Flask app starts up normally
* RAG chain loads as expected
* Message history works
* Web UI is served on port 5000
* No bytecode or pip cache clutter in the image

The image is stable and suitable for use in later deployment branches.

## ✅ **Summary**

This branch introduces complete Docker support for the LLMOps Medical Chatbot:

* Fully documented Python 3.12 Dockerfile
* Portable, reproducible execution environment
* Works seamlessly with Flask, LangChain, embeddings, and vector store
* Prepares the project for CI/CD and deployment pipelines

The chatbot can now be run anywhere — locally, in the cloud, or inside Kubernetes — using a single container.