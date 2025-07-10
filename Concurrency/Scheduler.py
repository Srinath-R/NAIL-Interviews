"""
𝐂𝐨𝐧𝐜𝐮𝐫𝐫𝐞𝐧𝐜𝐲 + 𝐒𝐜𝐡𝐞𝐝𝐮𝐥𝐢𝐧𝐠

Problem Statement: You’re given access to a system of worker threads. Each worker can perform a task, but may fail randomly.
Implement a robust scheduler that:
    * Retries failed tasks
    * Ensures a task is only retried up to 3 times
    * Distributes tasks evenly across all threads
    * Tech Challenge:
    * Use non-blocking queues
    * Retry logic
    * Thread-safety considerations

"""
import threading
import queue
import random

MAX_RETRIES = 3

class Task:
    def __init__(self, func, retries=0):
        self.func = func
        self.retries = retries

    def run(self):
        try:
            self.func()
            return True
        except Exception as e:
            print(f"Task failed: {e}")
            return False

class Worker(threading.Thread):
    def __init__(self, task_queue, worker_id):
        super().__init__()
        self.task_queue = task_queue
        self.worker_id = worker_id
        self.daemon = True
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                task = self.task_queue.get(timeout=1)
                print(f"Worker-{self.worker_id} got a task")
                success = task.run()
                if not success and task.retries < MAX_RETRIES:
                    task.retries += 1
                    print(f"Retrying (attempt {task.retries})...")
                    self.task_queue.put(task)
                self.task_queue.task_done()
                print(f"Task {str(task.func)} completed by worker {self.worker_id}")
            except queue.Empty:
                continue

    def stop(self):
        self._stop_event.set()

class Scheduler:
    def __init__(self, num_workers):
        self.queues = [queue.Queue() for _ in range(num_workers)]
        self.workers = [Worker(self.queues[i], i) for i in range(num_workers)]
        self.index = 0  # Round-robin index
        self.lock = threading.Lock()

    def submit(self, func):
        with self.lock:
            task = Task(func)
            self.queues[self.index % len(self.queues)].put(task)
            self.index += 1

    def run(self):
        for worker in self.workers:
            worker.start()

    def shutdown(self):
        for q in self.queues:
            q.join()
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()

def flaky_task():
    if random.random() < 0.3:
        raise Exception("Random failure")
    print("Task succeeded")

def sort():
    a = sorted([5,45,45,9,2,7,12,785,12,98])
    print(f"Task succeeded: {a}")

scheduler = Scheduler(num_workers=4)

scheduler.submit(flaky_task)
scheduler.submit(sort)

scheduler.run()
scheduler.shutdown()
