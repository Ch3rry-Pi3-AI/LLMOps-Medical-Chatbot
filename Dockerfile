# =============================================================================
# Dockerfile — LLMOps Medical Chatbot (Flask Web Application)
#
# Description
# -----------
# This Dockerfile builds a lightweight Python 3.12 container for the
# AI Medical Chatbot. It sets up the execution environment, installs system
# dependencies, copies project files, installs Python requirements using the
# project’s editable installation, and finally runs the Flask application.
#
# Features
# --------
# - Uses python:3.12-slim as the minimal base image
# - Disables bytecode generation and enables unbuffered logging
# - Installs required system build tools
# - Copies entire project into /app
# - Installs dependencies via pip with cache disabled
# - Exposes port 5000 for the Flask web server
# - Launches the application via `python app/application.py`
#
# Notes
# -----
# - Ensure a proper pyproject.toml or setup.py exists for editable installs
# - For production deployments, consider adding a non-root user
# - Keep .env files out of the build context
# =============================================================================


# Use Python 3.12 slim as the lightweight base image
FROM python:3.12-slim


# Set essential environment variables
# Prevent Python from writing .pyc files and ensure stdout/stderr flush immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# Create and set the working directory inside the container
WORKDIR /app


# Install required system packages (build tools, curl, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Copy the entire project into the container's working directory
COPY . .


# Install Python dependencies in editable mode (-e .)
# "--no-cache-dir" avoids storing pip cache layers in the image
RUN pip install --no-cache-dir -e .


# Expose the port used by the Flask application
EXPOSE 5000


# Launch the Flask app when the container starts
CMD ["python", "app/application.py"]
