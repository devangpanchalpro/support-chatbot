# Build stage
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies required for compiling some Python packages
RUN apk add --no-cache build-base libffi-dev

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-alpine

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy application files
COPY bot/ bot/
COPY data/ data/
COPY .env ./

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "bot.main:app", "--host", "0.0.0.0", "--port", "8000"]
