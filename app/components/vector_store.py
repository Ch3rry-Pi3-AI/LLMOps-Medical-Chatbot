"""
Vector Store Component for the LLMOps Medical Chatbot.

This module is responsible for:
    - Loading an existing FAISS vector store from disk.
    - Creating and saving a new FAISS vector store from text chunks.

It integrates with:
    - `get_embedding_model()` from `app.components.embeddings`
    - Project-wide logging via `app.common.logger`
    - Structured error handling via `app.common.custom_exception.CustomException`

Public functions:
    - load_vector_store() -> Optional[FAISS]
    - save_vector_store(text_chunks) -> Optional[FAISS]
"""

# =============================
# Imports
# =============================
import os
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.components.embeddings import get_embedding_model
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DB_FAISS_PATH

# =============================
# Logger
# =============================
logger = get_logger(__name__)


# =============================
# Load Existing Vector Store
# =============================
def load_vector_store() -> Optional[FAISS]:
    """
    Load an existing FAISS vector store from the configured path.

    Returns
    -------
    Optional[FAISS]
        The loaded FAISS vector store instance if it exists.
        Returns None if no vector store is found or an error occurs.
    """
    try:
        # Initialise the embedding model used by the vector store
        embedding_model = get_embedding_model()

        # Check if a persisted FAISS index already exists on disk
        if os.path.exists(DB_FAISS_PATH):
            logger.info("Loading existing FAISS vector store...")

            # Load the FAISS index from the local directory
            vector_store = FAISS.load_local(
                DB_FAISS_PATH,
                embedding_model,
                allow_dangerous_deserialization=True,
            )

            logger.info("FAISS vector store loaded successfully.")
            return vector_store
        else:
            # Inform the user that no persisted index was found
            logger.warning("No FAISS vector store found on disk.")
            return None

    except Exception as e:
        # Wrap any exception with CustomException and log full details
        error_message = CustomException("Failed to load FAISS vector store", e)
        logger.error(str(error_message))
        return None


# =============================
# Create and Save New Vector Store
# =============================
def save_vector_store(text_chunks: List[Document]) -> Optional[FAISS]:
    """
    Create and persist a new FAISS vector store from text chunks.

    Parameters
    ----------
    text_chunks : list of Document
        A list of `Document` objects (typically produced by the PDF loader)
        that will be embedded and stored in FAISS.

    Returns
    -------
    Optional[FAISS]
        The created FAISS vector store instance if successful.
        Returns None if an error occurs.

    Raises
    ------
    CustomException
        If `text_chunks` is empty or None.
    """
    try:
        # Ensure there is data to index before building the vector store
        if not text_chunks:
            raise CustomException("No text chunks were provided to build the vector store")

        # Log the start of the vector store generation process
        logger.info("Generating a new FAISS vector store from text chunks")

        # Initialise the embedding model for converting text into vectors
        embedding_model = get_embedding_model()

        # Build a new FAISS vector store directly from the documents
        db = FAISS.from_documents(text_chunks, embedding_model)

        # Persist the vector store to the configured directory
        logger.info("Saving FAISS vector store to disk")
        db.save_local(DB_FAISS_PATH)

        logger.info("FAISS vector store saved successfully.")
        return db

    except Exception as e:
        # Wrap and log detailed error information
        error_message = CustomException("Failed to create and save FAISS vector store", e)
        logger.error(str(error_message))
        return None
