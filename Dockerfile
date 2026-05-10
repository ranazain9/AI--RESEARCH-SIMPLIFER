FROM python:3.11-slim

# Prevents Python from generating .pyc files and ensures logs are visible immediately
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installs basic tools needed for building some Python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installs your project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# Copies all project files into the container
COPY . .

# Sets up the upload directory with the right permissions
RUN mkdir -p temp_uploads && chmod 777 temp_uploads

# Exposes the backend port
EXPOSE 8000

# Starts the FastAPI server using uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
