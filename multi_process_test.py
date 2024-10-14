import random
import time
from multiprocessing import Process
from api_client import (
    fetch_all_race_details,
    fetch_all_race_results,
    fetch_all_fastest_laps,
    fetch_all_driver_info,
    fetch_all_circuit_info
)

def random_function():
    functions = [
        fetch_all_race_details,
        fetch_all_race_results,
        fetch_all_fastest_laps,
        fetch_all_driver_info,
        fetch_all_circuit_info
    ]
    chosen_function = random.choice(functions)
    print(f"Executing: {chosen_function.__name__}")
    chosen_function()

def worker_process():
    while True:
        random_function()
        time.sleep(random.uniform(1, 5))  # 각 함수 실행 사이에 1~5초 대기

if __name__ == "__main__":
    num_processes = 5  # 동시에 실행할 프로세스 수
    processes = []

    for _ in range(num_processes):
        p = Process(target=worker_process)
        p.start()
        processes.append(p)

    try:
        # 메인 프로세스가 계속 실행되도록 함
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all processes...")
        for p in processes:
            p.terminate()
            p.join()

    print("All processes stopped.")