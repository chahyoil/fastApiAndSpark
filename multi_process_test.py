import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import threading

def send_request_sync(url, thread_id):
    thread_start_time = time.time()
    print(f"Thread {thread_id} started at {thread_start_time:.2f}")
    
    try:
        response = requests.get(url)
        result = response.json()
        thread_end_time = time.time()
        print(f"Thread {thread_id} completed in {thread_end_time - thread_start_time:.2f} seconds.")
        if 'session_id' in result:
            print(f"Thread {thread_id} Session ID: {result['session_id']}")
        else:
            print(f"Thread {thread_id} Session ID not found in response")

        print(f"Thread {thread_id} Ends at {thread_end_time:.2f}")
        return result, thread_id, thread_start_time, thread_end_time
    except requests.RequestException as e:
        print(f"Thread {thread_id} Request failed: {e}")
        return None, thread_id, thread_start_time, time.time()
    except json.JSONDecodeError as e:
        print(f"Thread {thread_id} JSON decode error: {e}")
        return None, thread_id, thread_start_time, time.time()

def test_sync():
    print("\n--- Testing Synchronous Version ---")
    url = "http://localhost:8000/api/sample/test_spark_session_sync"
    
    overall_start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_request_sync, url, i) for i in range(10)]
        results = [future.result() for future in futures]
    
    overall_end_time = time.time()
    
    print("\nResults summary:")
    for result, thread_id, start_time, end_time in results:
        if result:
            print(f"Thread {thread_id}:")
            print(f"  Started at: {start_time:.2f}")
            print(f"  Ended at: {end_time:.2f}")
            print(f"  Duration: {end_time - start_time:.2f} seconds")
            print(f"  Session ID: {result.get('session_id', 'Not found')}")
        else:
            print(f"Thread {thread_id}: Failed")
        print()
    
    print(f"Overall execution time: {overall_end_time - overall_start_time:.2f} seconds")

def main():
    test_sync()

if __name__ == "__main__":
    main()