FROM python:3.10-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip install --no-cache-dir \
    pyyaml \
    requests

# Keep container alive or run main
CMD ["python3", "src/main.py"]
