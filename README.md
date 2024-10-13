이해했습니다. README.md를 그에 맞게 수정하겠습니다. Docker 사용이 필수적인 부분을 강조하고, 실행 방법을 더 자세히 설명하겠습니다.

# F1 Race Data API

이 프로젝트는 F1 레이스 데이터에 접근할 수 있는 FastAPI 기반의 RESTful API를 제공한다. Docker를 사용하여 애플리케이션을 실행한다.

## 프로젝트 구조

```
fastApiAndSpark/
├── app/
│   ├── dto/
│   ├── middleware/
│   ├── routes/
│   ├── sql/
│   ├── tests/
│   ├── utils/
│   ├── initialize_f1_data.py
│   └── main.py
├── Dockerfile
├── requirements.txt
├── run_tests.sh
└── run.sh
```

## 주요 컴포넌트

- **dto/**: Pydantic 모델을 사용한 데이터 전송 객체
- **middleware/**: CORS, XSS 보호, 인증 등의 미들웨어
- **routes/**: API 엔드포인트 정의
- **sql/**: Jinja2 템플릿을 사용한 SQL 쿼리
- **utils/**: 유틸리티 함수 (Spark 세션 관리, 오류 처리 등)
- **main.py**: FastAPI 애플리케이션의 진입점

## 기능

- F1 레이스, 드라이버, 컨스트럭터, 서킷 데이터 조회
- 사용자 인증 및 관리자 기능
- Spark를 이용한 대용량 데이터 처리

## 설치 및 실행

1. Docker가 시스템에 설치되어 있어야 한다.

2. 프로젝트 클론:
   ```
   git clone [repository_url]
   cd fastApiAndSpark
   ```

3. 애플리케이션 실행:
   ```
   ./run.sh
   ```
   이 스크립트는 Docker 이미지를 빌드하고 컨테이너를 실행한다.

4. 테스트 실행:
   ```
   ./run_tests.sh
   ```
   이 스크립트는 테스트를 위한 Docker 컨테이너를 실행한다.

## API 문서

애플리케이션이 실행된 후:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 개발 환경

- python == 3.10
- pyspark == 3.3.2
- spark == 3.1.3
- Docker

## 참고사항

- 데이터 초기화는 애플리케이션 시작 시 `initialize_f1_data()` 함수를 통해 수행된다.
- Spark 세션은 애플리케이션 생명주기에 맞춰 관리된다.
- 모든 의존성은 Docker 컨테이너 내에서 관리되므로, 로컬 환경에 추가 설치가 필요 없다.

