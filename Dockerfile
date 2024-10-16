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
    vim \
    && rm -rf /var/lib/apt/lists/*

# Java 11 설치
RUN wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - \
    && echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list \
    && apt-get update \
    && apt-get install -y temurin-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Java 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/temurin-11-jdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# Python 3.10 설치
RUN wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz \
    && tar -xf Python-3.10.0.tgz \
    && cd Python-3.10.0 \
    && ./configure --enable-optimizations \
    && make -j $(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.10.0 Python-3.10.0.tgz

RUN ln -sf /usr/local/bin/python3.10 /usr/bin/python3.10

# pip 업그레이드
RUN python3.10 -m ensurepip \
    && python3.10 -m pip install --upgrade pip

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# 환경 변수 설정
ENV PYSPARK_PYTHON=/usr/bin/python3.10
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/python3.10
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH
ENV SPARK_PYTHON /usr/bin/python3.10

# Spark 설정 파일 수정
RUN echo "spark.pyspark.python /usr/bin/python3.10" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.pyspark.driver.python /usr/bin/python3.10" >> $SPARK_HOME/conf/spark-defaults.conf

# 애플리케이션 디렉토리 생성
WORKDIR /app
COPY ./app/ .

RUN mkdir -p /app/logs && chown -R 1001:1001 /app/logs

# FastAPI 서버 실행
CMD ["python3.10", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 포트 노출
EXPOSE 8000

# 사용자 전환
USER 1001
