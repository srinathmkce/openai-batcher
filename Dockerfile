# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /workspace

# Install dependencies
RUN apt-get update && apt-get install -y curl git

# Install PDM
COPY pyproject.toml pdm.lock ./

RUN pip install --no-cache-dir pdm 



