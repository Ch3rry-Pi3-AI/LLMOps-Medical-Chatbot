"""
PDF Loader Component for the LLMOps Medical Chatbot.

This module is responsible for:
    - Loading PDF files from the configured data directory.
    - Converting them into LangChain `Document` objects.
    - Splitting those documents into smaller text chunks for downstream RAG.

The main public functions are:
    - load_pdf_files()      -> List[Document]
    - create_text_chunks()  -> List[Document]

Both functions use structured logging and CustomException to ensure
robust, transparent error handling throughout the ingestion pipeline.
"""

# =============================
# Imports
# =============================
import os
from typing import List

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

# =============================
# Logger
# =============================
logger = get_logger(__name__)


# =============================
# Load PDF Files
# =============================
def load_pdf_files() -> List[Document]:
    """
    Load all PDF files located in the project's data directory.

    Returns
    -------
    list of Document
        A list of LangChain `Document` objects created from the PDF files.
        Returns an empty list if no documents are found or if loading fails.

    Raises
    ------
    CustomException
        If the configured data directory does not exist.
    """
    try:
        # Ensure the data directory exists before attempting to load PDFs
        if not os.path.exists(DATA_PATH):
            raise CustomException("Data path does not exist")

        # Log the directory we are about to scan for PDF files
        logger.info(f"Loading PDF files from: {DATA_PATH}")

        # Create a DirectoryLoader to load all *.pdf files using PyPDFLoader
        loader = DirectoryLoader(
            DATA_PATH,
            glob="*.pdf",
            loader_cls=PyPDFLoader,
        )

        # Load documents from the directory
        documents: List[Document] = loader.load()

        # Log based on whether any documents were discovered
        if not documents:
            logger.warning("No PDF files were found in the data directory.")
        else:
            logger.info(f"Successfully loaded {len(documents)} PDF documents.")

        return documents

    except Exception as e:
        # Wrap any unexpected exception in CustomException and log it
        error_message = CustomException("Failed to load PDF files", e)
        logger.error(str(error_message))
        return []


# =============================
# Create Text Chunks
# =============================
def create_text_chunks(documents: List[Document]) -> List[Document]:
    """
    Split a list of LangChain `Document` objects into smaller text chunks.

    Parameters
    ----------
    documents : list of Document
        The documents produced by `load_pdf_files()` or a similar loader.

    Returns
    -------
    list of Document
        A list of `Document` objects representing smaller text chunks.
        Returns an empty list if chunking fails.

    Raises
    ------
    CustomException
        If the input `documents` list is empty.
    """
    try:
        # Ensure that at least one document was provided for splitting
        if not documents:
            raise CustomException("No documents were provided for chunking")

        # Log how many documents we are about to convert into chunks
        logger.info(f"Splitting {len(documents)} documents into text chunks")

        # Configure the text splitter with project-wide chunk parameters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        # Split the documents into smaller, overlapping chunks
        text_chunks: List[Document] = text_splitter.split_documents(documents)

        # Log the total number of generated chunks
        logger.info(f"Generated {len(text_chunks)} text chunks from input documents")

        return text_chunks

    except Exception as e:
        # Wrap and log any errors encountered during chunk generation
        error_message = CustomException("Failed to generate text chunks", e)
        logger.error(str(error_message))
        return []
