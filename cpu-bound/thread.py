import time
from threading import Thread
from queue import Queue

from lib import generate_valid_urls, get_dir_name
from runner import program_runner


def count_urls_char_bytes(url_count: int, q:Queue):
    char_bytes = 0
    for url in generate_valid_urls(url_count):
        for char in url:
            char_bytes += len(char.encode())
    q.put(char_bytes)

def main(thread_count=4):
    url_total = 1_00_000
    threads = []
    q = Queue()
    total_bytes = 0

    for _ in range(thread_count):
        t = Thread(
                target=count_urls_char_bytes, 
                args=(url_total//thread_count, q)
        )
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    while not q.empty():
        total_bytes += q.get()

    return total_bytes


if __name__ == "__main__":
    for i in range(2, 11, 2):
        program_runner(
            main,
            f"{i}_threads_data",
            get_dir_name(__file__),
            descr=f"Cpu bound execution with {i} Threads. The experiment count bytes per characteres for 1_00_000 generated urls. The returned_value represents the total bytes of the operation.",
            thread_count=i
        )
        time.sleep(0.8)


