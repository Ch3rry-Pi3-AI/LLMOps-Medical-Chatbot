# 📁 **Components Folder Overview**

The `components` folder contains the core logic modules of the **LLMOps Medical Chatbot** application.

At present, this directory includes:

### **pdf_loader.py**

Responsible for loading medical PDF files from the `data/` directory and splitting them into text chunks for downstream processing.

### **embeddings.py**

Responsible for initialising the HuggingFace embedding model used to convert text chunks into vector representations for retrieval.

### **vector_store.py**

Responsible for loading an existing FAISS vector store from disk or creating and saving a new FAISS vector store using embedded text chunks.
