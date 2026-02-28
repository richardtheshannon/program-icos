FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    jq \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22 (required for Claude Code CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user for security
RUN useradd -m -s /bin/bash developer
USER developer
WORKDIR /home/developer/project

# Python dependencies will be installed via requirements.txt at runtime
ENV PATH="/home/developer/.local/bin:$PATH"

CMD ["bash"]
