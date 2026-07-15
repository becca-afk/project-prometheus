FROM mcr.microsoft.com/devcontainers/python:0-3.10-bullseye

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y python3-pip python3-venv git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir pip setuptools wheel

# Set working directory
WORKDIR /workspace

# Install OpenCV dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Install global Python packages
RUN pip3 install --no-cache-dir black flake8 pytest pytest-asyncio

# Set default shell
SHELL ["/bin/bash", "-c"]
