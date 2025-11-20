# =============================================================================
# Dockerfile — Jenkins with Docker (DinD-Style Support via docker.io)
#
# Description
# -----------
# This Dockerfile builds a Jenkins controller image with Docker installed
# inside the container. It enables Jenkins pipelines to:
# - Build Docker images
# - Run Docker containers
# - Push images to registries (DockerHub, GCR, ECR, etc.)
#
# Use Cases
# ---------
# - CI/CD pipelines that need to build and push container images
# - Docker-in-Docker style workflows (with appropriate runtime flags)
# - Pipelines that run containerised integration or system tests
#
# Key Features
# ------------
# - Based on the official `jenkins/jenkins:lts` image
# - Installs Docker from the Debian `docker.io` package
# - Adds the Jenkins user to the `docker` group
# - Creates `/var/lib/docker` as a volume for Docker runtime storage
# - Keeps Jenkins running as a non-root user for better security
#
# Notes
# -----
# - For true DinD behaviour, run the container with:
#     * `--privileged`   OR
#     * a mounted Docker socket: `-v /var/run/docker.sock:/var/run/docker.sock`
# - On Linux hosts, ensure the host `docker` group permissions align with
#   how you run this container, especially if mounting `/var/run/docker.sock`.
# - For production-grade separation, you may prefer an external Docker daemon
#   and let Jenkins talk to it via the socket or TCP.
# =============================================================================


# Base: official Jenkins LTS (Debian trixie-based)
FROM jenkins/jenkins:lts

# Switch to root to install system packages
USER root

# Install Docker and minimal dependencies
RUN apt-get update -y && \
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        docker.io \
    && \
    # Clean up package lists to keep image small
    apt-get clean

# Ensure the docker group exists and add the Jenkins user to it
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create Docker storage directory and mark it as a volume (for DinD-style usage)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to Jenkins user for normal operation
USER jenkins
