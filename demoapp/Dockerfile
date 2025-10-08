# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install only prometheus-client (minimal dependencies)
RUN pip install --no-cache-dir prometheus-client==0.17.1

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["python", "run_server.py"]


