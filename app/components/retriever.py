"""
Retriever / RAG Chain Component for the LLMOps Medical Chatbot.

This module builds the **Retrieval-Augmented Generation (RAG)** pipeline that powers
the medical question-answering behaviour.

The pipeline:

1. Loads the FAISS vector store and exposes it as a retriever.
2. Loads the Groq-hosted LLM (LLaMA 3.1) via `ChatGroq`.
3. Uses a custom medical prompt that:
   - Injects retrieved context.
   - Restricts answers to 2–3 lines.
   - Instructs the model not to hallucinate beyond the provided context.
4. Assembles everything into a LangChain Expression Language (LCEL) **Runnable**
   using `RunnablePassthrough` and a dictionary-based composition instead of the
   deprecated `langchain.chains` APIs (v1-compliant).

Public interface
----------------
set_custom_prompt() -> ChatPromptTemplate
create_qa_chain()   -> Runnable | None

The returned `Runnable` can be invoked as:

    chain = create_qa_chain()
    if chain is not None:
        answer = chain.invoke("What is hypertension?")
"""

# =============================
# Imports
# =============================
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


# =============================
# Logger
# =============================
logger = get_logger(__name__)


# =============================
# Prompt Template
# =============================
CUSTOM_PROMPT_TEMPLATE = """
You are a medical assistant. Answer the following medical question in **2–3 lines maximum**
using only the information provided in the context. If the answer is not contained in
the context, say that you do not know and do not invent or guess.

Context:
{context}

Question:
{question}

Answer:
"""


# =============================
# Prompt Factory
# =============================
def set_custom_prompt() -> ChatPromptTemplate:
    """
    Create the ChatPromptTemplate used for the medical RAG pipeline.

    The prompt:
    - Takes two variables: `context` and `question`.
    - Instructs the model to answer concisely (2–3 lines).
    - Explicitly forbids hallucinating beyond the provided context.

    Returns
    -------
    ChatPromptTemplate
        Configured prompt template for medical QA.
    """
    # Build the chat prompt from the template string
    return ChatPromptTemplate.from_template(CUSTOM_PROMPT_TEMPLATE)


# =============================
# RAG / QA Chain Factory
# =============================
def create_qa_chain() -> Optional[Runnable]:
    """
    Build the LangChain v1-compliant RAG chain for the Medical Chatbot.

    This function wires together:

    - FAISS vector store → retriever
    - Groq-hosted LLM
    - Custom medical prompt
    - LCEL Runnable pipeline with `RunnablePassthrough`

    The chain follows the standard LCEL RAG pattern:

        chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

    When invoked with a plain string question, the pipeline:

    1. Sends the question to the retriever to obtain relevant context.
    2. Fills the `context` and `question` slots of the prompt.
    3. Calls the LLM with the formatted prompt.
    4. Parses the LLM response into a plain string.

    Returns
    -------
    Runnable or None
        A RAG `Runnable` that accepts a question string and returns an answer string,
        or `None` if any component (vector store or LLM) fails to initialise.
    """
    try:
        # -------------------------
        # Load vector store / retriever
        # -------------------------
        logger.info("Loading vector store for RAG retriever")
        db = load_vector_store()

        # Guard against missing or failed vector store
        if db is None:
            raise CustomException("Vector store not present or failed to load")

        # Convert FAISS store to a retriever (semantic search backend)
        retriever = db.as_retriever(search_kwargs={"k": 1})

        # -------------------------
        # Load LLM
        # -------------------------
        logger.info("Loading Groq LLM for QA chain")
        llm = load_llm()

        # Guard against failed LLM loading
        if llm is None:
            raise CustomException("LLM not loaded from Groq")

        # -------------------------
        # Build prompt and LCEL chain
        # -------------------------
        prompt = set_custom_prompt()

        # LCEL RAG chain:
        # - "context": sends the input question into the retriever
        # - "question": passes the raw question unchanged via RunnablePassthrough
        # - prompt: formats context + question
        # - llm: generates answer
        # - StrOutputParser: converts model output to a plain string
        qa_chain: Runnable = (
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        logger.info("Successfully created LCEL-based QA RAG chain")
        return qa_chain

    except Exception as e:
        # Wrap and log any errors during chain construction
        error_message = CustomException("Failed to create QA RAG chain", e)
        logger.error(str(error_message))
        return None
