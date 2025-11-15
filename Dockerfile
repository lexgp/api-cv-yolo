# syntax=docker/dockerfile:1.4

### STAGE 1 — builder #######################################
FROM python:3.10-slim AS builder
WORKDIR /app

COPY requirements.txt .

RUN pip config set global.timeout 120
RUN pip config set global.retries 20

# кэширование pip + сборка wheel
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

COPY . .

##############################################################

### STAGE 2 — runtime ########################################
FROM python:3.10-slim AS runtime
WORKDIR /app

# OpenCV deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

# установка зависимостей из wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
##############################################################

