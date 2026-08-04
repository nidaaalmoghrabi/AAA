# syntax=docker/dockerfile:1

# ---- Builder stage --------------------------------------------------------
FROM python:3.11-slim AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- Runtime stage ----------------------------------------------------------
FROM python:3.11-slim

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --shell /usr/sbin/nologin --create-home app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY app ./app
COPY frontend ./frontend

RUN chown -R app:app /app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
