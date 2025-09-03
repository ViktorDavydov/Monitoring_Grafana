#!/usr/bin/env python3

import os
import random
import time
import threading
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


# List of available endpoints
ENDPOINTS = [
    "/code-2xx",
    "/code-4xx", 
    "/code-5xx",
    "/ms-200",
    "/ms-500",
    "/ms-1000",
]

# Global requests counter
requests_count = {}


def get_max_requests_count():
    """Get maximum request counts from environment variables."""
    max_successful_requests = 15
    max_error_requests = 5
    
    max_successful_str = os.getenv("HTTP_REQUESTS_SUCCESSFUL_MAX")
    if max_successful_str:
        try:
            max_successful_requests = int(max_successful_str)
        except ValueError:
            pass
    
    max_error_str = os.getenv("HTTP_REQUESTS_ERROR_MAX")
    if max_error_str:
        try:
            max_error_requests = int(max_error_str)
        except ValueError:
            pass
    
    return max_successful_requests, max_error_requests


def randomize_endpoints():
    """Shuffle the endpoints list randomly."""
    random.shuffle(ENDPOINTS)


def make_request(endpoint):
    """Make HTTP request to the specified endpoint."""
    try:
        url = f"http://localhost:8080{endpoint}"
        with urlopen(url, timeout=5) as response:
            return response.getcode()
    except HTTPError as e:
        # HTTP errors (4xx, 5xx) are expected for some endpoints
        return e.code
    except URLError as e:
        print(f"Request error for {endpoint}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for {endpoint}: {e}")
        return None


def worker_thread(endpoint, request_count, results_lock, completed_count):
    """Worker thread to make requests to a specific endpoint."""
    for i in range(request_count):
        status_code = make_request(endpoint)
        
        with results_lock:
            completed_count[0] += 1
            if completed_count[0] % 10 == 0:
                print(f"Completed {completed_count[0]} requests")


def main():
    """Main load generator loop."""
    max_successful_requests, max_error_requests = get_max_requests_count()
    
    # Set random seed
    random.seed(int(time.time()))
    
    print("Load generator starting...")
    print(f"Max successful requests per endpoint: {max_successful_requests}")
    print(f"Max error requests per endpoint: {max_error_requests}")
    
    while True:
        total_requests_count = 0
        
        # Randomize endpoint order
        randomize_endpoints()
        
        # Calculate requests per endpoint
        for endpoint in ENDPOINTS:
            requests_to_endpoint = 0
            
            # Determine request count based on endpoint type
            if endpoint == "/code-200" or endpoint.startswith("/ms-"):
                requests_to_endpoint = random.randint(0, max_successful_requests)
            else:
                requests_to_endpoint = random.randint(0, max_error_requests)
            
            requests_count[endpoint] = requests_to_endpoint
            total_requests_count += requests_to_endpoint
        
        print(f"\nStarting batch with {total_requests_count} total requests")
        
        # Create threads for concurrent requests
        threads = []
        results_lock = threading.Lock()
        completed_count = [0]  # Use list to make it mutable in nested scope
        
        for endpoint, count in requests_count.items():
            if count > 0:
                print(f"  {endpoint}: {count} requests")
                thread = threading.Thread(
                    target=worker_thread,
                    args=(endpoint, count, results_lock, completed_count)
                )
                threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        elapsed_time = time.time() - start_time
        print(f"Batch completed: {total_requests_count} requests in {elapsed_time:.2f} seconds")
        
        # Small delay between batches
        time.sleep(1)


if __name__ == '__main__':
    main()



