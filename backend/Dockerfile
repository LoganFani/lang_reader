FROM python:3.11-slim

# Install system dependencies needed to compile C++ code
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Reach out to the root directory for requirements
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]