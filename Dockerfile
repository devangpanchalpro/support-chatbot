# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy folders
COPY bot/ bot/
COPY data/ data/
COPY .env ./

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "bot.main:app", "--host", "0.0.0.0", "--port", "8000"]
