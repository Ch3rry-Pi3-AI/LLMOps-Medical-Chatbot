"""
Vector Store Pipeline Orchestrator for the LLMOps Medical Chatbot.

This module provides a high-level pipeline that:
    - Loads medical PDF documents.
    - Splits them into text chunks.
    - Generates and saves a FAISS vector store.

It ties together the core components:
    - pdf_loader.py
    - embeddings.py
    - vector_store.py

Running this file directly will trigger the full ingestion → chunking →
vector store creation flow, making it a convenient entry point for building
or rebuilding the vector store used by the chatbot.
"""

# =============================
# Imports
# =============================
import os

from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.components.vector_store import save_vector_store
from app.config.config import DB_FAISS_PATH

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# =============================
# Logger
# =============================
logger = get_logger(__name__)


# =============================
# Main Vector Store Pipeline
# =============================
def process_and_store_pdfs() -> None:
    """
    End-to-end pipeline for generating the FAISS vector store.

    The pipeline performs:
        1. Loading PDF documents from the data directory
        2. Splitting documents into smaller text chunks
        3. Embedding chunks and creating a FAISS vector store
        4. Saving the vector store to the configured path

    Raises
    ------
    CustomException
        If any stage of the pipeline fails.
    """
    try:
        # Begin the process of generating a new vector store
        logger.info("Starting vector store creation pipeline")

        # Load PDF documents
        documents = load_pdf_files()

        # Split loaded documents into text chunks
        text_chunks = create_text_chunks(documents)

        # Save the vector store generated from the text chunks
        save_vector_store(text_chunks)

        # Log successful completion
        logger.info("Vector store created successfully")

    except Exception as e:
        # Wrap and log detailed error information
        error_message = CustomException("Failed to create vector store", e)
        logger.error(str(error_message))


# =============================
# Execution Entry Point
# =============================
if __name__ == "__main__":
    # Run the full vector store generation pipeline
    process_and_store_pdfs()
