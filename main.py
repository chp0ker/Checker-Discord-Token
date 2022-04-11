import queue
import threading
import time

import requests
num_worker_threads = 100
start_time = time.time()

tokens = open("all-tokens.txt", "r", encoding="utf-8").read().splitlines()
good = open(f"good-tokens.txt", "a")
bad = open(f"bad-tokens.txt", "a")

def main(token):
    headers = {"authorization": token}
    response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        good.write(f"{token}\n")
    else:
        bad.write(f"{token}\n")


def worker():
    while True:
        items = q.get()
        if items is None:
            break
        main(items)
        q.task_done()


q = queue.Queue()

threads = []

for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in tokens:
    q.put(item)

q.join()

for i in range(num_worker_threads):
    q.put(None)

for t in threads:
    t.join()

print("--- %s seconds ---" % (time.time() - start_time))
