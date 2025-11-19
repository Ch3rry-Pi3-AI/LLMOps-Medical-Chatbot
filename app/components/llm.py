"""
LLM Loader Component for the LLMOps Medical Chatbot.

This module is responsible for initialising a Groq-hosted Large Language Model
using the `ChatGroq` interface from the LangChain v1 ecosystem.

The loaded LLM is used during the final inference and response-generation stage
of the Medical Chatbot, enabling fast, low-latency medical question answering.

Public function:
    - load_llm(model_name, groq_api_key)  -> ChatGroq | None

This component includes:
    - Structured logging for traceability
    - NumPy-style documentation
    - Robust error handling via CustomException
"""

# =============================
# Imports
# =============================
from typing import Optional

from langchain_groq import ChatGroq

from app.config.config import GROQ_API_KEY
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# =============================
# Logger
# =============================
logger = get_logger(__name__)


# =============================
# Load Groq LLM
# =============================
def load_llm(
    model_name: str = "llama-3.1-8b-instant",
    groq_api_key: str = GROQ_API_KEY
) -> Optional[ChatGroq]:
    """
    Initialise a Groq-hosted LLM using the ChatGroq client.

    Parameters
    ----------
    model_name : str, optional
        The model identifier to load from Groq. Defaults to `"llama-3.1-8b-instant"`.
    groq_api_key : str, optional
        The API key used to authenticate with Groq. Loaded from `.env` by default.

    Returns
    -------
    ChatGroq or None
        An instance of the ChatGroq LLM if initialisation succeeds.
        Returns None if loading fails.

    Raises
    ------
    CustomException
        If Groq model initialisation fails.
    """
    try:
        # Inform the logs that we are beginning model initialisation
        logger.info("Loading LLM from Groq using LLaMA3 model...")

        # Instantiate the ChatGroq LLM wrapper
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=0.3,
            max_tokens=256,
        )

        # Confirm successful initialisation
        logger.info("LLM loaded successfully from Groq.")
        return llm

    except Exception as e:
        # Wrap and log the full error context
        error_message = CustomException("Failed to load an LLM from Groq", e)
        logger.error(str(error_message))
        return None
