import random
import time
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor

# 동기 버전 요청 함수
def send_request_sync(url, sleep_time):
    start_time = time.time()
    try:
        response = requests.get(f"{url}?sleep_time={sleep_time}")
        result = response.json()
        end_time = time.time()
        print(f"Raw response: {result}")
        print(f"Request completed in {end_time - start_time:.2f} seconds.")
        if 'session_id' in result:
            print(f"Session ID: {result['session_id']}")
        else:
            print("Session ID not found in response")
        return result
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# 비동기 버전 요청 함수
async def send_request_async(session, url, sleep_time):
    start_time = time.time()
    try:
        async with session.get(f"{url}?sleep_time={sleep_time}") as response:
            result = await response.json()
            end_time = time.time()
            print(f"Raw response: {result}")
            print(f"Request completed in {end_time - start_time:.2f} seconds.")
            if 'session_id' in result:
                print(f"Session ID: {result['session_id']}")
            else:
                print("Session ID not found in response")
            return result
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None

# 동기 버전 테스트
def test_sync():
    print("\n--- Testing Synchronous Version ---")
    url = "http://localhost:8000/api/sample/test_spark_session_sync"
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: send_request_sync(url, random.randint(1, 5)), range(10)))
    
    session_ids = set(result.get('session_id') for result in results if result and 'session_id' in result)
    print(f"Number of unique session IDs used (sync): {len(session_ids)}")

# 비동기 버전 테스트
async def test_async():
    print("\n--- Testing Asynchronous Version ---")
    url = "http://localhost:8000/api/sample/test_spark_session_async"
    async with aiohttp.ClientSession() as session:
        tasks = [send_request_async(session, url, random.randint(1, 5)) for _ in range(10)]
        results = await asyncio.gather(*tasks)
    
    session_ids = set(result.get('session_id') for result in results if result and 'session_id' in result)
    print(f"Number of unique session IDs used (async): {len(session_ids)}")

# 메인 함수
async def main():
    # 동기 버전 테스트
    test_sync()
    
    # 비동기 버전 테스트
    # await test_async()

if __name__ == "__main__":
    asyncio.run(main())