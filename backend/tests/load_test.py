import time
import threading
import requests
import json

API_URL = "http://localhost:8000/api/v1"
CONCURRENT_USERS = 50

def simulate_clock_in(user_id):
    # Simulate a user clocking in
    # In a real scenario, we'd need valid tokens. 
    # This script assumes we have a way to get tokens or hits a public endpoint for stress testing.
    try:
        start_time = time.time()
        # Hitting health/root for load testing if auth isn't mocked
        response = requests.get("http://localhost:8000/") 
        elapsed = time.time() - start_time
        print(f"User {user_id}: Status {response.status_code} - Time {elapsed:.2f}s")
    except Exception as e:
        print(f"User {user_id}: Failed - {e}")

def run_load_test():
    print(f"Starting load test with {CONCURRENT_USERS} concurrent users...")
    threads = []
    
    start_global = time.time()
    
    for i in range(CONCURRENT_USERS):
        t = threading.Thread(target=simulate_clock_in, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    end_global = time.time()
    print(f"Load test finished in {end_global - start_global:.2f}s")

if __name__ == "__main__":
    run_load_test()
