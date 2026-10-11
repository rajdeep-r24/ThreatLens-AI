FROM python:3.12-slim

WORKDIR /app

# Install system utilities needed for file inspection & build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and models
COPY app ./app
COPY tests ./tests
COPY models /models
COPY static_analysis /static_analysis

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
