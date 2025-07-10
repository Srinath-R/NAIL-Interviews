from multiprocessing import Process, Value, Lock as MP_Lock, Semaphore as MP_Semaphore
import asyncio
import time

print("\n============== MULTIPROCESSING ==============\n")

# Shared counter example with Lock
def mp_increment(counter, lock):
    for _ in range(10000):
        with lock:
            counter.value += 1

shared_counter = Value('i', 0)
mp_lock = MP_Lock()
procs = [Process(target=mp_increment, args=(shared_counter, mp_lock)) for _ in range(5)]

[p.start() for p in procs]
[p.join() for p in procs]
print(f"[Multiprocessing] Final counter: {shared_counter.value}")

# Semaphore with Multiprocessing
mp_sem = MP_Semaphore(2)

def mp_critical(name, sem):
    with sem:
        print(f"{name} entered")
        time.sleep(1)
        print(f"{name} exited")

for i in range(4):
    Process(target=mp_critical, args=(f"Proc-{i}", mp_sem)).start()
time.sleep(3)


print("\n============== ASYNCIO ==============\n")

async def async_semaphore_example():
    sem = asyncio.Semaphore(2)

    async def task(name):
        async with sem:
            print(f"{name} started")
            await asyncio.sleep(1)
            print(f"{name} finished")

    await asyncio.gather(*(task(f"Task-{i}") for i in range(4)))

async def async_event_example():
    event = asyncio.Event()

    async def waiter(name):
        print(f"{name} waiting...")
        await event.wait()
        print(f"{name} triggered!")

    asyncio.create_task(waiter("Async-Waiter-1"))
    asyncio.create_task(waiter("Async-Waiter-2"))

    await asyncio.sleep(2)
    print("Setting event")
    event.set()

async def main_async_examples():
    print("\n▶️ Running Asyncio Semaphore Example")
    await async_semaphore_example()
    print("\n▶️ Running Asyncio Event Example")
    await async_event_example()
    await asyncio.sleep(1)

asyncio.run(main_async_examples())