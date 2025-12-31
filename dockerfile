FROM python:3.11-slim-bookworm

# Zmienne środowiskowe
ENV PYTHONUNBUFFERED=1 \
    PYTHONWRITEBYTECODE=1

# Instalacja narzędzi systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Katalog roboczy
WORKDIR /app

# Klonowanie repozytorium InvisTerra z GitHuba
RUN git clone https://github.com/vGiacomov/INVISTERRA.git . && \
    ls -la

# Instalacja zależności Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Uruchomienie aplikacji InvisTerra
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
