FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_HTTP_TIMEOUT=120
ENV PIP_DEFAULT_TIMEOUT=120

ENV HF_ENDPOINT=https://hf-mirror.com
ENV HF_HOME=/opt/huggingface
ENV TRANSFORMERS_CACHE=/opt/huggingface/transformers
ENV SENTENCE_TRANSFORMERS_HOME=/opt/huggingface/sentence-transformers
ENV HF_HUB_DISABLE_XET=1

RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's|http://deb.debian.org/debian|http://mirrors.tencentyun.com/debian|g' /etc/apt/sources.list.d/debian.sources; \
        sed -i 's|http://deb.debian.org/debian-security|http://mirrors.tencentyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources; \
    fi; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libgomp1; \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple uv

COPY pyproject.toml ./

RUN uv pip compile pyproject.toml --no-cache -o requirements.txt \
    && grep -viE '^(torch==|torch |nvidia-|cuda-|triton==)' requirements.txt > requirements.cpu.txt \
    && pip install --no-cache-dir --no-deps \
        --index-url https://download.pytorch.org/whl/cpu \
        "torch==2.5.1+cpu" \
    && pip install --no-cache-dir --no-deps \
        -i https://pypi.tuna.tsinghua.edu.cn/simple \
        -r requirements.cpu.txt

# 只预下载 embedding 模型
RUN python - <<'PY'
from sentence_transformers import SentenceTransformer

print("Downloading embedding model: BAAI/bge-small-zh-v1.5")
SentenceTransformer("BAAI/bge-small-zh-v1.5")
print("Embedding model downloaded successfully")
PY

ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1

COPY app ./app

RUN mkdir -p /app/data/chroma_db
RUN mkdir -p /app/data/uploads
RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
