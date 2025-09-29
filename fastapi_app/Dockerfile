# Use a lightweight base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install FastAPI and Uvicorn
RUN pip install --no-cache-dir fastapi uvicorn numpy scikit-learn pandas mlflow apache-airflow==2.7.2

# (Optional) Expose port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]

