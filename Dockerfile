FROM python:3.11-slim

# Install security updates and curl for health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -m -g appuser appuser

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app

# Copy project configuration with proper ownership
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Switch to non-root user before installing dependencies
USER appuser

# Create virtual environment and sync dependencies
RUN uv sync --frozen

# Switch back to root to copy application code
USER root

# Copy application code with proper ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user for runtime
USER appuser

# Expose port
EXPOSE 8000

# Set environment variables
ENV ENVIRONMENT=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application using uv
CMD ["uv", "run", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
