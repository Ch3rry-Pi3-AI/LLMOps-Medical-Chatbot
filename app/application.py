"""
application.py — Flask entrypoint for the LLMOps Medical Chatbot UI.

This module wires together the Flask web application, session-based
message history, and the Retrieval-Augmented Generation (RAG) QA chain.

High-level responsibilities
---------------------------
- Initialise the Flask app and secret key.
- Register a custom Jinja filter (`nl2br`) for rendering multi-line text.
- Maintain a simple in-session chat history as a list of messages.
- Call the `create_qa_chain` factory to build the RAG pipeline.
- Safely normalise the model output into plain text for display.
- Provide routes:
    * "/"      — main chat interface (GET/POST).
    * "/clear" — clears the current chat session.
"""

from flask import Flask, render_template, request, session, redirect, url_for
# Import core Flask objects for routing, templating, and sessions

from markupsafe import Markup
# Used to mark strings as safe HTML (for the nl2br filter)

from dotenv import load_dotenv
# Loads environment variables from a .env file

from app.components.retriever import create_qa_chain
# Factory that constructs the RAG question-answering chain

import os
# Standard library module for environment and OS-level operations

from typing import Any, List, Dict, Optional
# Type hints for better readability and tooling support


# ---------------------------------------------------------------------
# Environment & Flask setup
# ---------------------------------------------------------------------

load_dotenv()
# Load environment variables from a .env file into the process

HF_TOKEN: Optional[str] = os.environ.get("HF_TOKEN")
# Optional Hugging Face token (kept for compatibility if used elsewhere)

app: Flask = Flask(__name__)
# Create the Flask application instance

app.secret_key = os.urandom(24)
# Configure a random secret key for securely signing session cookies


# ---------------------------------------------------------------------
# Jinja filters
# ---------------------------------------------------------------------

def nl2br(value: Any) -> Markup:
    """
    Convert newlines to HTML `<br>` tags for safe template rendering.

    This helper makes sure that whatever is passed in is first converted
    to a string so that `.replace` is always available. It then wraps the
    result in `Markup` so Flask/Jinja treats it as safe HTML (only the
    `<br>` tags are injected, not arbitrary HTML).

    Parameters
    ----------
    value : Any
        Any Python object whose textual representation may contain
        newline characters (`\\n`).

    Returns
    -------
    Markup
        A Markup-safe string where each newline (`\\n`) has been replaced
        by `<br>` followed by a newline for readability.
    """
    if value is None:
        value = ""
    # Ensure we never call .replace on a None value

    if not isinstance(value, str):
        value = str(value)
    # Convert any non-string input to a string

    return Markup(value.replace("\n", "<br>\n"))
    # Replace newlines with <br> tags and mark as safe HTML


# Register the filter under the name "nl2br" for use inside Jinja templates
app.jinja_env.filters["nl2br"] = nl2br


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def ensure_messages() -> None:
    """
    Ensure that `session["messages"]` exists and is a list.

    This function is used as a small guard so that all parts of the
    application can safely assume that `session["messages"]` is
    initialised as a list that will hold the chat history.

    Notes
    -----
    The messages are expected to be a list of dictionaries with keys:
    `"role"` and `"content"`.
    """
    if "messages" not in session or not isinstance(session["messages"], list):
        session["messages"] = []
    # Initialise the messages list if it is missing or malformed


def normalise_answer(payload: Any) -> str:
    """
    Normalise the QA chain output into a plain text string.

    In the current setup, the chain ends with a `StrOutputParser`, so the
    returned `payload` will typically already be a string. This helper
    makes the code robust to future changes (e.g. returning dicts or
    message objects).

    Parameters
    ----------
    payload : Any
        Raw object returned from the QA chain. Can be a string, dict, or
        any object with a `.content` attribute in future variants.

    Returns
    -------
    str
        A human-readable string extracted from the payload.
    """
    if payload is None:
        return ""
    # If there is no content at all, return an empty string

    if isinstance(payload, str):
        return payload
    # Fast path: already a string

    if isinstance(payload, dict):
        # Try common keys used by various LLM / chain libraries
        for key in ("answer", "result", "output_text", "output", "content"):
            if key in payload:
                val: Any = payload[key]
                return val if isinstance(val, str) else str(val)
        # Fall back to string representation of the entire dict
        return str(payload)

    # Some LLM response objects have a `.content` attribute
    content: Any = getattr(payload, "content", None)
    if isinstance(content, str):
        return content
    # Use the content attribute if it is a proper string

    return str(payload)
    # Final fallback: use the generic string representation


def get_sanitised_messages() -> List[Dict[str, str]]:
    """
    Sanitize `session["messages"]` for safe rendering in the template.

    This function transforms whatever is stored in `session["messages"]`
    into a list of dictionaries of the form:

    `{"role": <str>, "content": <str>}`

    Any non-string content is converted to a string to avoid errors in
    the `nl2br` filter or in the template.

    Returns
    -------
    list of dict
        A list of message dictionaries with both `"role"` and `"content"`
        guaranteed to be strings.
    """
    raw_messages: Any = session.get("messages", [])
    # Retrieve whatever is currently stored under "messages" in the session

    sanitised: List[Dict[str, str]] = []
    # Initialise the list that will hold the cleaned messages

    if not isinstance(raw_messages, list):
        return []
    # If the stored value is not a list, treat it as invalid and return empty

    for message in raw_messages:
        # Iterate over each stored message and normalise structure
        if isinstance(message, dict):
            role: Any = message.get("role", "assistant")
            content: Any = message.get("content", "")
        else:
            # If the entry is not a dict, treat it as content from the assistant
            role = "assistant"
            content = message

        if not isinstance(content, str):
            content = str(content)
        # Ensure content is always a string

        sanitised.append({"role": str(role), "content": content})
        # Append the cleaned message to the sanitised list

    return sanitised
    # Return the fully normalised message list


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main chat route: renders the UI and processes user questions.

    On GET
    ------
    - Ensures the message history is initialised.
    - Renders the chat template with any existing messages.

    On POST
    -------
    - Reads the user input from the form (`prompt` field).
    - Appends the user message to the session history.
    - Builds the QA chain via `create_qa_chain`.
    - Invokes the chain with the user's question.
    - Normalises the model output and appends it as an assistant message.
    - Renders the template with updated messages and any error message.

    Returns
    -------
    Response
        Flask response object produced by `render_template` (for GET and
        POST) or by the underlying Flask machinery.
    """
    ensure_messages()
    # Make sure that session["messages"] exists and is a list

    error_msg: Optional[str] = None
    # Placeholder for any error message that might be displayed in the UI

    if request.method == "POST":
        # Handle form submission (user asking a question)
        user_input: str = request.form.get("prompt", "").strip()
        # Retrieve the user prompt from the form and strip whitespace

        if user_input:
            # Only proceed if the user actually typed something
            messages: List[Dict[str, str]] = session["messages"]
            # Get the existing message history from the session

            messages.append({"role": "user", "content": user_input})
            # Add the new user message to the history

            session["messages"] = messages
            # Persist the updated history back into the session

            try:
                qa_chain: Any = create_qa_chain()
                # Attempt to create the question-answering chain

                if qa_chain is None:
                    raise RuntimeError(
                        "QA chain could not be created (LLM or VectorStore issue)."
                    )
                # Guard against a missing or failed QA chain

                # In the current design, the chain accepts a plain question string
                response: Any = qa_chain.invoke(user_input)
                # Invoke the RAG pipeline with the user's question

                print("QA chain raw response:", repr(response))
                # Debug print so you can inspect the raw response in the console

                assistant_text: str = normalise_answer(response)
                # Convert the raw response to plain text

                messages.append({"role": "assistant", "content": assistant_text})
                # Append the assistant's answer to the message history

                session["messages"] = messages
                # Save the updated message history into the session

            except Exception as exc:
                # Capture any exception arising from chain creation or invocation
                error_msg = f"Error : {str(exc)}"
                # Store an informative error message for display in the UI

        # For POST requests, render the page immediately so that any error
        # and the new assistant response are visible without redirect
        return render_template(
            "index.html",
            messages=get_sanitised_messages(),
            error=error_msg,
        )

    # If the request method is GET, simply render the current state of the chat
    return render_template(
        "index.html",
        messages=get_sanitised_messages(),
        error=error_msg,
    )


@app.route("/clear", methods=["GET"])
def clear():
    """
    Clear the current chat history stored in the session.

    This route removes the `"messages"` key from the session and then
    redirects the user back to the main index page, effectively giving
    them a fresh chat window.

    Returns
    -------
    Response
        A redirect response to the main index route.
    """
    session.pop("messages", None)
    # Remove the messages list from the session if it exists

    return redirect(url_for("index"))
    # Redirect to the main chat page after clearing history


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    # Only run the development server if this file is executed directly
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,  # Avoid double-loading under the Flask reloader
    )
