# ==============================================================================
# OpenAI Whisper - Docker Image
# Transcrição de áudio usando o modelo Whisper da OpenAI
# ==============================================================================

FROM python:3.11-slim AS base

# Metadados
LABEL maintainer="docker-whisper"
LABEL description="OpenAI Whisper - Speech Recognition"

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive
# Diretório de cache dos modelos Whisper
ENV XDG_CACHE_HOME=/root/.cache

# ---------------------------------------------------------------------------
# 1. Dependências do sistema (ffmpeg + build tools)
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 2. Instalar openai-whisper
# ---------------------------------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir openai-whisper

# ---------------------------------------------------------------------------
# 3. Criar diretório de trabalho para arquivos de áudio
# ---------------------------------------------------------------------------
WORKDIR /data

# Volume para montar arquivos de áudio do host
VOLUME ["/data"]

# Volume para persistir modelos baixados entre execuções
VOLUME ["/root/.cache/whisper"]

# ---------------------------------------------------------------------------
# 4. Entrypoint padrão
# ---------------------------------------------------------------------------
ENTRYPOINT ["whisper"]
CMD ["--help"]
