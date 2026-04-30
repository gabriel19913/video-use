# 🎙️ Docker Whisper

Imagem Docker para executar o [OpenAI Whisper](https://github.com/openai/whisper) — transcrição de áudio com inteligência artificial.

## 📋 Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) (incluído no Docker Desktop)
- **(Opcional)** [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) para suporte a GPU

## 🚀 Início Rápido

### 1. Build da imagem

```bash
docker compose build
```

### 2. Criar pasta de áudios

```bash
mkdir -p data
```

Coloque seus arquivos de áudio (`.mp3`, `.wav`, `.flac`, etc.) dentro da pasta `data/`.

### 3. Transcrever um áudio

```bash
docker compose run --rm whisper /data/meu_audio.mp3 --model tiny --language Portuguese
```

## 📖 Exemplos de Uso

### Transcrição básica (modelo tiny — rápido)

```bash
docker compose run --rm whisper /data/audio.mp3 --model tiny
```

### Transcrição em Português

```bash
docker compose run --rm whisper /data/audio.mp3 --model small --language Portuguese
```

### Transcrição com alta qualidade (modelo turbo)

```bash
docker compose run --rm whisper /data/audio.mp3 --model turbo
```

### Traduzir áudio para Inglês

```bash
docker compose run --rm whisper /data/audio.mp3 --model medium --task translate
```

### Ver todas as opções disponíveis

```bash
docker compose run --rm whisper --help
```

## 🧠 Modelos Disponíveis

| Modelo     | Parâmetros | VRAM   | Velocidade |
|------------|-----------|--------|------------|
| `tiny`     | 39M       | ~1 GB  | ~10x       |
| `base`     | 74M       | ~1 GB  | ~7x        |
| `small`    | 244M      | ~2 GB  | ~4x        |
| `medium`   | 769M      | ~5 GB  | ~2x        |
| `large`    | 1550M     | ~10 GB | 1x         |
| `turbo`    | 809M      | ~6 GB  | ~8x        |

> Os modelos são baixados automaticamente na primeira execução e ficam em cache no volume `whisper-model-cache`.

## 🎮 Usando GPU (NVIDIA)

Para usar sua GPU NVIDIA, descomente a seção `deploy` no `docker-compose.yml`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

Pré-requisito: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) instalado.

## 🐍 Uso Interativo com Python

Para abrir um shell Python dentro do container:

```bash
docker compose run --rm --entrypoint python whisper
```

Dentro do Python:

```python
import whisper

model = whisper.load_model("tiny")
result = model.transcribe("/data/meu_audio.mp3")
print(result["text"])
```

## 📁 Estrutura do Projeto

```
docker-whisper/
├── Dockerfile           # Definição da imagem Docker
├── docker-compose.yml   # Configuração do Docker Compose
├── .dockerignore        # Arquivos ignorados no build
├── README.md            # Esta documentação
└── data/                # Monte seus arquivos de áudio aqui
```

## 🗑️ Limpeza

### Remover o container
```bash
docker compose down
```

### Remover a imagem e o cache de modelos
```bash
docker compose down -v --rmi all
```
