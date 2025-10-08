import os
import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

endpoints = [
    "/code-2xx",
    "/code-4xx", 
    "/code-5xx",
    "/ms-200",
    "/ms-500",
    "/ms-1000",
]

def get_max_requests_count() -> tuple[int, int]:
    max_successful_requests = 15
    max_error_requests = 5

    max_successful_requests_string = os.getenv("HTTP_REQUESTS_SUCCESSFUL_MAX")
    if max_successful_requests_string:
        try:
            max_successful_requests = int(max_successful_requests_string)
        except ValueError:
            pass

    max_error_requests_string = os.getenv("HTTP_REQUESTS_ERROR_MAX")
    if max_error_requests_string:
        try:
            max_error_requests = int(max_error_requests_string)
        except ValueError:
            pass

    return max_successful_requests, max_error_requests

def randomize_endpoints():
    random.shuffle(endpoints)

def make_request(endpoint: str):
    try:
        response = requests.get(f"http://localhost:8080{endpoint}", timeout=30)
        return f"Request to {endpoint}: Status {response.status_code}"
    except Exception as e:
        return f"Error making request to {endpoint}: {e}"

def main():
    max_successful_requests, max_error_requests = get_max_requests_count()
    
    while True:
        requests_dict = {}
        total_requests_count = 0

        randomize_endpoints()

        # Распределяем запросы по эндпоинтам
        for endpoint in endpoints:
            if endpoint == "/code-2xx" or endpoint.startswith("/ms-"):
                requests_to_endpoint = random.randint(0, max_successful_requests)
            else:
                requests_to_endpoint = random.randint(0, max_error_requests)

            requests_dict[endpoint] = requests_to_endpoint
            total_requests_count += requests_to_endpoint

        print(f"Total requests in this iteration: {total_requests_count}")
        print(f"Requests distribution: {requests_dict}")

        # Используем ThreadPoolExecutor для управления потоками
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Создаем задачи для всех запросов
            futures = []
            for endpoint, requests_count in requests_dict.items():
                for i in range(requests_count):
                    future = executor.submit(make_request, endpoint)
                    futures.append(future)

            # Ожидаем завершения и выводим результаты
            for future in as_completed(futures):
                try:
                    result = future.result()
                    print(result)
                except Exception as e:
                    print(f"Future error: {e}")

        print("Iteration completed. Starting next iteration...")
        time.sleep(1)

if __name__ == "__main__":
    main()
