FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn httpx
COPY bridge.py .
EXPOSE 8082
CMD ["uvicorn", "bridge:app", "--host", "0.0.0.0", "--port", "8082"]
