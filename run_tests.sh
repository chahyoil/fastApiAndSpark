#!/bin/bash

# 변수 설정
CONTAINER_NAME="f1-race-data-api-container"
APP_PORT=8000

# 앱이 실행 중인지 확인
echo "Checking if the application is running..."
if ! curl -s http://localhost:$APP_PORT > /dev/null
then
    echo "Error: Application is not running on port $APP_PORT"
    exit 1
fi
echo "Application is up and running."

# 컨테이너 내부에서 테스트 실행
echo "Running tests..."
docker exec $CONTAINER_NAME python3.10 -m pytest /app/tests

# 테스트 실행 결과 저장
TEST_EXIT_CODE=$?

# 테스트 결과에 따라 스크립트 종료
if [ $TEST_EXIT_CODE -eq 0 ]
then
    echo "All tests passed successfully."
    exit 0
else
    echo "Some tests failed. Please check the test output above."
    exit 1
fi
