FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend/api:/app/ai-services/neural-network-explainer/src:/app/ai-services/cnn-feature-map-viewer/src:/app/ai-services/autoencoder-latent-space/src

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt \
    && useradd --create-home --uid 10001 axon

COPY --chown=axon:axon backend/api ./backend/api
COPY --chown=axon:axon ai-services/neural-network-explainer/src ./ai-services/neural-network-explainer/src
COPY --chown=axon:axon ai-services/cnn-feature-map-viewer/src ./ai-services/cnn-feature-map-viewer/src
COPY --chown=axon:axon ai-services/autoencoder-latent-space/src ./ai-services/autoencoder-latent-space/src
COPY --chown=axon:axon models ./models

USER axon

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["python", "-m", "uvicorn", "app.main:app", "--app-dir", "backend/api", "--host", "0.0.0.0", "--port", "8000"]
