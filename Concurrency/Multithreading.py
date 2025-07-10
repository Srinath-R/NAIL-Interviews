import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

print("\n🔒 1. Lock Example (Mutual Exclusion)")
counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    for _ in range(10000):
        with lock:  # ensures only one thread modifies counter at a time
            counter += 1

threads = [threading.Thread(target=safe_increment) for _ in range(5)]
[t.start() for t in threads]
[t.join() for t in threads]
print(f"Final counter value: {counter}\n")  # Expected: 50000

print("🚦 2. Semaphore Example (Limit concurrent access)")
sem = threading.Semaphore(2)  # allow 2 threads at a time

def limited_resource(name):
    with sem:
        print(f"{name} entered critical section")
        time.sleep(1)
        print(f"{name} exiting")

for i in range(4):
    threading.Thread(target=limited_resource, args=(f"Thread-{i}",)).start()
time.sleep(2.5)

print("\n🚧 3. Barrier Example (Synchronize threads)")
barrier = threading.Barrier(3)

def barrier_task(n):
    print(f"Thread-{n} waiting at the barrier")
    barrier.wait()
    print(f"Thread-{n} passed the barrier")

for i in range(3):
    threading.Thread(target=barrier_task, args=(i,)).start()
time.sleep(1)

print("\n🔔 4. Event Example (Trigger threads to start)")
event = threading.Event()

def wait_for_event(name):
    print(f"{name} waiting for event...")
    event.wait()
    print(f"{name} received event!")

for i in range(2):
    threading.Thread(target=wait_for_event, args=(f"Worker-{i}",)).start()
time.sleep(2)
event.set()  # trigger the event

print("\n🗣️ 5. Condition Example (Producer-Consumer Coordination)")
condition = threading.Condition()
queue = []

def producer():
    with condition:
        print("Producer producing item...")
        queue.append("item")
        condition.notify()

def consumer():
    with condition:
        while not queue:
            print("Consumer waiting...")
            condition.wait()
        print(f"Consumer consumed {queue.pop()}")

threading.Thread(target=consumer).start()
time.sleep(1)
threading.Thread(target=producer).start()
time.sleep(1)

print("\n🤖 6. Future with ThreadPoolExecutor (Concurrent Tasks)")
def slow_add(x, y):
    time.sleep(1)
    return x + y

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(slow_add, i, i+1) for i in range(3)]
    for f in as_completed(futures):
        print(f"Result: {f.result()}")
