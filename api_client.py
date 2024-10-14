import requests
import random
import time
import functools

BASE_URL = "http://localhost:8000"

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result
    return wrapper

def random_delay():
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)

@timing_decorator
def get_database_info():
    return requests.get(f"{BASE_URL}/api/sample/database-info")

@timing_decorator
def get_races(page=1, page_size=10):
    params = {"page": page, "page_size": page_size}
    return requests.get(f"{BASE_URL}/api/races/", params=params)

@timing_decorator
def get_race_details(race_id):
    return requests.get(f"{BASE_URL}/api/races/{race_id}")

def fetch_all_race_details():
    all_race_details = []
    page = 1
    while True:
        # 레이스 목록 가져오기
        races_response = get_races(page=page)
        if races_response.status_code != 200:
            print(f"Error fetching races on page {page}: {races_response.status_code}")
            break

        races_data = races_response.json()
        
        # 현재 페이지의 모든 레이스에 대한 상세 정보 가져오기
        for race in races_data['data']:
            race_id = race['race_id']
            random_delay()  # 랜덤 대기 시간 추가
            race_detail_response = get_race_details(race_id)
            if race_detail_response.status_code == 200:
                race_detail = race_detail_response.json()
                all_race_details.append(race_detail)
                print(f"Fetched details for race ID: {race_id}")
            else:
                print(f"Error fetching details for race ID {race_id}: {race_detail_response.status_code}")

        # 페이지네이션 확인
        if page >= races_data['total_pages']:
            break
        page += 1

    return all_race_details

@timing_decorator
def get_race_results(race_id):
    return requests.get(f"{BASE_URL}/api/races/{race_id}/results")

def get_fastest_laps(race_id):
    return requests.get(f"{BASE_URL}/api/races/{race_id}/fastest-laps")

def fetch_all_race_results():
    all_race_results = []
    page = 1
    while True:
        races_response = get_races(page=page)
        if races_response.status_code != 200:
            print(f"Error fetching races on page {page}: {races_response.status_code}")
            break

        races_data = races_response.json()
        
        for race in races_data['data']:
            race_id = race['race_id']
            random_delay()
            results_response = get_race_results(race_id)
            if results_response.status_code == 200:
                results = results_response.json()
                all_race_results.append({"race_id": race_id, "results": results})
                print(f"Fetched results for race ID: {race_id}")
            else:
                print(f"Error fetching results for race ID {race_id}: {results_response.status_code}")

        if page >= races_data['total_pages']:
            break
        page += 1
        random_delay()

    return all_race_results

def fetch_all_fastest_laps():
    all_fastest_laps = []
    page = 1
    while True:
        races_response = get_races(page=page)
        if races_response.status_code != 200:
            print(f"Error fetching races on page {page}: {races_response.status_code}")
            break

        races_data = races_response.json()
        
        for race in races_data['data']:
            race_id = race['race_id']
            random_delay()
            laps_response = get_fastest_laps(race_id)
            if laps_response.status_code == 200:
                laps = laps_response.json()
                all_fastest_laps.append({"race_id": race_id, "fastest_laps": laps})
                print(f"Fetched fastest laps for race ID: {race_id}")
            else:
                print(f"Error fetching fastest laps for race ID {race_id}: {laps_response.status_code}")

        if page >= races_data['total_pages']:
            break
        page += 1
        random_delay()

    return all_fastest_laps

@timing_decorator
def get_drivers(page=1, page_size=10):
    params = {"page": page, "page_size": page_size}
    return requests.get(f"{BASE_URL}/api/drivers/", params=params)

@timing_decorator
def get_driver_details(driver_id):
    return requests.get(f"{BASE_URL}/api/drivers/{driver_id}")

@timing_decorator
def get_driver_standings(driver_id):
    return requests.get(f"{BASE_URL}/api/drivers/{driver_id}/standings")

def fetch_all_driver_info():
    all_driver_info = []
    page = 1
    while True:
        random_delay()
        drivers_response = get_drivers(page=page)
        if drivers_response.status_code != 200:
            print(f"Error fetching drivers on page {page}: {drivers_response.status_code}")
            break

        drivers_data = drivers_response.json()
        
        for driver in drivers_data['data']:
            driver_id = driver['driver_id']
            driver_info = {"driver_id": driver_id, "basic_info": driver}

            # 드라이버 상세 정보 가져오기
            random_delay()
            details_response = get_driver_details(driver_id)
            if details_response.status_code == 200:
                driver_info["details"] = details_response.json()
                print(f"Fetched details for driver ID: {driver_id}")
            else:
                print(f"Error fetching details for driver ID {driver_id}: {details_response.status_code}")

            # 드라이버 순위 정보 가져오기
            random_delay()
            standings_response = get_driver_standings(driver_id)
            if standings_response.status_code == 200:
                driver_info["standings"] = standings_response.json()
                print(f"Fetched standings for driver ID: {driver_id}")
            else:
                print(f"Error fetching standings for driver ID {driver_id}: {standings_response.status_code}")

            all_driver_info.append(driver_info)

        if page >= drivers_data['total_pages']:
            break
        page += 1

    return all_driver_info

@timing_decorator
def get_constructor_standings(year: int):
    return requests.get(f"{BASE_URL}/api/constructors/standings?year={year}")

@timing_decorator
def get_constructor_results(constructor_id):
    return requests.get(f"{BASE_URL}/api/constructors/{constructor_id}/results")

@timing_decorator
def get_circuits(page=1, page_size=10):
    params = {"page": page, "page_size": page_size}
    return requests.get(f"{BASE_URL}/api/circuits/", params=params)

@timing_decorator
def get_circuit_info(circuit_id):
    return requests.get(f"{BASE_URL}/api/circuits/{circuit_id}")

@timing_decorator
def get_circuit_races(circuit_id):
    return requests.get(f"{BASE_URL}/api/circuits/{circuit_id}/races")

def fetch_all_circuit_info():
    all_circuit_info = []
    page = 1
    while True:
        random_delay()
        circuits_response = get_circuits(page=page)
        if circuits_response.status_code != 200:
            print(f"Error fetching circuits on page {page}: {circuits_response.status_code}")
            break

        circuits_data = circuits_response.json()
        
        for circuit in circuits_data['data']:
            circuit_id = circuit['circuit_id']
            circuit_info = {"circuit_id": circuit_id, "basic_info": circuit}

            # 서킷 상세 정보 가져오기
            random_delay()
            info_response = get_circuit_info(circuit_id)
            if info_response.status_code == 200:
                circuit_info["details"] = info_response.json()
                print(f"Fetched details for circuit ID: {circuit_id}")
            else:
                print(f"Error fetching details for circuit ID {circuit_id}: {info_response.status_code}")

            # 서킷 레이스 정보 가져오기
            random_delay()
            races_response = get_circuit_races(circuit_id)
            if races_response.status_code == 200:
                circuit_info["races"] = races_response.json()
                print(f"Fetched races for circuit ID: {circuit_id}")
            else:
                print(f"Error fetching races for circuit ID {circuit_id}: {races_response.status_code}")

            all_circuit_info.append(circuit_info)

        if page >= circuits_data['total_pages']:
            break
        page += 1

    return all_circuit_info

if __name__ == "__main__":
    fetch_all_race_details()
    fetch_all_race_results()
    fetch_all_fastest_laps()
    fetch_all_driver_info()
    fetch_all_circuit_info()