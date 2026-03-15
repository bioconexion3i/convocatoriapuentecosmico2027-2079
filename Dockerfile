# ETAPA 1: Builder
FROM python:3.11-slim-bookworm AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc python3-dev libssl-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ETAPA 2: Runtime
FROM python:3.11-slim-bookworm
RUN groupadd -r b6user && useradd -r -g b6user b6user
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 && rm -rf /var/lib/apt/lists/*

# Copiamos con --chown para dar permisos al usuario b6user inmediatamente
COPY --from=builder --chown=b6user:b6user /root/.local /home/b6user/.local
COPY --chown=b6user:b6user . .

# Variables de entorno críticas para que Python encuentre Flask
ENV PATH=/home/b6user/.local/bin:$PATH
ENV PYTHONPATH=/home/b6user/.local/lib/python3.11/site-packages
USER b6user

CMD ["python", "main.py"]
