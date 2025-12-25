import requests
import threading
import time
from collections import Counter

BASE_URL = "http://localhost:8080"
ENDPOINT = "/auth/login"

PAYLOAD = {
    "username": "iheba",
    "password": "secret123"
}

TOTAL_REQUESTS = 5
CONCURRENCY = 5
DELAY_BETWEEN_REQUESTS = 0.05

results = Counter()
lock = threading.Lock()

session = requests.Session()

def send_request():
    try:
        r = session.post(
            BASE_URL + ENDPOINT,
            json=PAYLOAD,  # ensures proper JSON encoding
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=5,
        )
        if results["printed"] == 0:
            print("\n--- First error response ---")
            print("Status:", r.status_code)
            print("Body:", r.text)
            results["printed"] += 1
        # IMPORTANT: print first error body so we know what’s happening
        if r.status_code >= 400:
            with lock:
                if results["printed"] == 0:
                    print("\n--- First error response ---")
                    print("Status:", r.status_code)
                    print("Body:", r.text)
                    results["printed"] += 1

        with lock:
            results[r.status_code] += 1

    except requests.exceptions.RequestException as e:
        with lock:
            results["error"] += 1

def worker(n):
    for _ in range(n):
        send_request()
        time.sleep(DELAY_BETWEEN_REQUESTS)

threads = []
per_thread = TOTAL_REQUESTS // CONCURRENCY

start = time.time()

for _ in range(CONCURRENCY):
    t = threading.Thread(target=worker, args=(per_thread,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

duration = time.time() - start

print("\n=== Load Test Results ===")
print(f"Total requests: {sum(results.values()) - results.get('printed', 0)}")
print(f"Duration: {duration:.2f}s")
print(f"Requests/sec: {(sum(results.values()) - results.get('printed', 0)) / duration:.2f}")
print("Status codes:")
for k, v in results.items():
    if k != "printed":
        print(f"  {k}: {v}")
