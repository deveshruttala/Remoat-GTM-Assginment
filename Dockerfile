FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    wget unzip curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriver (auto handled via WebDriverManager)

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]