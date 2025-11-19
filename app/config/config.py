import os

"""
Configuration file for the LLMOps Medical Chatbot project.

Environment variables:
    HF_TOKEN
    GROQ_API_KEY

Static configuration values:
    HUGGINGFACE_REPO_ID
    DB_FAISS_PATH
    DATA_PATH
    CHUNK_SIZE
    CHUNK_OVERLAP
"""

# -----------------------------
# Environment Variables
# -----------------------------
HF_TOKEN = os.environ.get("HF_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# -----------------------------
# Model and Embedding Settings
# -----------------------------
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# -----------------------------
# Paths
# -----------------------------
DB_FAISS_PATH = "vectorstore/db_faiss"
DATA_PATH = "data/"

# -----------------------------
# Text Chunking Parameters
# -----------------------------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
