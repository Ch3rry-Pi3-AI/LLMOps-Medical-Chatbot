"""
Embedding Model Component for the LLMOps Medical Chatbot.

This module is responsible for initialising the HuggingFace embedding model
used throughout the chatbot’s retrieval pipeline. The embeddings produced by
this model convert text chunks into dense vector representations, enabling
semantic search within the vector store.

The primary function exposed is:
    - get_embedding_model()  -> HuggingFaceEmbeddings

This module uses structured logging and CustomException to ensure clear,
consistent error handling during model initialisation.
"""

# =============================
# Imports
# =============================
from typing import Any
from langchain_huggingface import HuggingFaceEmbeddings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# =============================
# Logger
# =============================
logger = get_logger(__name__)


# =============================
# Load HuggingFace Embedding Model
# =============================
def get_embedding_model() -> Any:
    """
    Initialise the HuggingFace embedding model used for text vectorisation.

    Returns
    -------
    HuggingFaceEmbeddings
        A loaded embedding model instance ready for generating text embeddings.

    Raises
    ------
    CustomException
        If the model fails to load or an internal error occurs.
    """
    try:
        # Inform the logs that embedding model initialisation is starting
        logger.info("Initialising HuggingFace embedding model")

        # Load a compact, high-performance sentence transformer model
        model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Log successful initialisation
        logger.info("HuggingFace embedding model loaded successfully")

        return model

    except Exception as e:
        # Wrap errors in CustomException and log with full diagnostic details
        error_message = CustomException(
            "Error occurred while loading embedding model", e
        )
        logger.error(str(error_message))
        raise error_message
