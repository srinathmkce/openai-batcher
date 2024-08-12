# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /workspace

# Install dependencies
RUN apt-get update && apt-get install -y curl git

# Install PDM
COPY pyproject.toml pdm.lock ./

RUN pip install --no-cache-dir pdm 

# Add PDM to PATH
# ENV PATH="/root/.local/bin:$PATH"

# Copy the PDM configuration file (pyproject.toml)

# Setup virtual environment
# RUN pdm venv create .venv

# # Set PDM to use the created virtual environment
# RUN pdm use .venv

# # Set the path to the Python interpreter in the virtual environment
# ENV VIRTUAL_ENV="/workspace/.venv"
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"


