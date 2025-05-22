# great_expectations/Dockerfile

FROM python:3.11-slim

LABEL maintainer="LayerDynamics <layerdynamics@proton.me>"
LABEL description="Docker image for running Great Expectations CLI and data docs server"

# Prevents Python from writing .pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GE_HOME=/app/great_expectations

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR ${GE_HOME}

# Install Great Expectations
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir great_expectations

# Copy GE configuration files (assumed to exist in bind mount)
COPY . ${GE_HOME}

# Expose the Data Docs port
EXPOSE 4000

# Entrypoint options:
# - serve data docs (default)
# - run CLI commands (docker exec)
CMD ["great_expectations", "docs", "build"]
