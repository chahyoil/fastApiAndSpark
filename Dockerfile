FROM bitnami/spark:3.1.3

USER root

# 필요한 도구 설치
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 3.10 설치
RUN wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz \
    && tar -xf Python-3.10.0.tgz \
    && cd Python-3.10.0 \
    && ./configure --enable-optimizations \
    && make -j $(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.10.0 Python-3.10.0.tgz

# pip 업그레이드
RUN python3.10 -m ensurepip \
    && python3.10 -m pip install --upgrade pip

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# 애플리케이션 디렉토리 생성
WORKDIR /app

RUN mkdir -p /tmp/f1db && chown 1001:1001 /tmp/f1db
RUN mkdir -p /app/logs && chown 1001:1001 /app/logs

# 애플리케이션 코드 복사
COPY ./app/ .

# FastAPI 서버 실행
CMD ["python3.10", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 포트 노출
EXPOSE 8000

USER 1001