# Użyj obrazu z GDAL (potrzebne dla rasterio)
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.0

# Ustaw workdir
WORKDIR /app

# Zainstaluj Python i pip
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj requirements
COPY requirements.txt .

# Zainstaluj zależności Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Skopiuj aplikację
COPY . .

# Expose port Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Uruchom Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
