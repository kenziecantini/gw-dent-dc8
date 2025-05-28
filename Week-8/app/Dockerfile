FROM python:3.11-slim

# Install system dependencies for xmlsec and general build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port (adjust if needed)
EXPOSE 5000

# Default command to run the app (adjust if your main file is different)
CMD ["python", "main.py"]
