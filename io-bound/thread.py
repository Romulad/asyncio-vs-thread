import os
import tempfile
from threading import Thread, Lock
import time
from typing import BinaryIO
from queue import Queue, Empty

import requests

from lib import (
    generate_valid_urls, 
    get_dir_name, 
    raise_fd_limit, 
    get_openable_fd_for_req
)
from runner import program_runner


def get_and_write_data(
    q:Queue,
    client:requests.Session, 
    f:BinaryIO,
    f_lock: Lock,
    failed_count
):
    while 1:
        try:
            url = q.get(block=False)
            try:
                response = client.get(url)
            except Exception as e:
                print(e)
                failed_count.increment()
            else:
                if not response.ok:
                    print(response.status_code)
                    failed_count.increment()
                else:
                    with f_lock:
                        f.write(response.content)
            finally:
                q.task_done()
        except Empty:
            break

def main(thread_count=5):
    if thread_count > get_openable_fd_for_req():
        ValueError(
            "Thread count should be less than process fd limit",
            "soft_limit - 124"
        )

    total_bytes = 0
    total_urls = 100_000
    threads:list[Thread] = []
    f_lock = Lock()
    url_q = Queue()

    for url in generate_valid_urls(total_urls):
        url_q.put(url)

    class FailedCounter:
        def __init__(self) -> None:
            self.count = 0
            self.c_lock = Lock()

        def increment(self):
            with self.c_lock:
                self.count += 1
    
    failed_count = FailedCounter()

    with tempfile.NamedTemporaryFile("ab+", delete=True) as f:
        
        with requests.Session() as client:
            for _ in range(thread_count):
                t = Thread(
                        target=get_and_write_data, 
                        args=(
                            url_q, 
                            client,
                            f,
                            f_lock,
                            failed_count
                        )
                )
                t.start()
                threads.append(t)
        
        for thread in threads:
            thread.join()

        f.flush()
        total_bytes = os.stat(f.name).st_size

    return total_bytes, failed_count.count


if __name__ == "__main__":
    raised = raise_fd_limit()
    max_ts = 1000 if raised else 900
    for count in [10, 100, max_ts]:
        print("execution for", count, "threads...\n")
        program_runner(
            main,
            f"{count}_threads_data_with_100_000_urls",
            get_dir_name(__file__),
            thread_count=count,
            descr=f"""Io bound execution using {count} threads. The experiment fetches 100_000 urls and stores the response data into a file. The returned values represnt the total bytes received from network and the number of failed requests (>=400 status code or error)."""
        )
        time.sleep(10)


