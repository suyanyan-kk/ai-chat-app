FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libgomp1 \
    || (apt-get update --fix-missing \
        && apt-get install -y --no-install-recommends \
            build-essential \
            curl \
            git \
            libgomp1) \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

RUN uv pip compile pyproject.toml --no-cache -o requirements.txt \
    && uv pip install --system --no-cache-dir -r requirements.txt

COPY app ./app

RUN mkdir -p /app/data/chroma_db
RUN mkdir -p /app/data/uploads
RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]