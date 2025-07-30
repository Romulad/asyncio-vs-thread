import asyncio
import tempfile
import os
import io
from threading import Thread, Lock
from queue import Empty, Queue
from typing import BinaryIO

import aiohttp 

from lib import generate_valid_urls, get_dir_name
from runner import program_runner


async def target_task(
    url:str,
    client:aiohttp.ClientSession,
    vf:io.BytesIO,
    vf_lock:asyncio.Lock,
):
    # TODO: Need  way to avoid fd limit
    try:
        async with client.get(url) as response:
            if not response.ok:
                return False
            async with vf_lock: 
                vf.write(await response.read())
            return True
    except Exception:
        return False


async def async_main(
    urls:list,
):
    vf = io.BytesIO()
    vf_lock = asyncio.Lock()
    failed_count = 0
    async with aiohttp.ClientSession() as client:
        results = await asyncio.gather(
            *[
                target_task(
                    url,
                    client,
                    vf, 
                    vf_lock,
                ) for url in urls
            ]
        )
        failed_count = len(urls) - sum(results)
    return vf.getvalue(), failed_count


def get_and_write_data(
    q:Queue,
    f:BinaryIO,
    f_lock:Lock,
    failed_counter,
):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        while 1:
            try:
                urls = q.get(block=False)
            except Empty:
                break
            else:
                try:
                    data, failed_count = loop.run_until_complete(
                        async_main(urls)
                    )
                    failed_counter.increment(failed_count)
                    with f_lock:
                        f.write(data)
                finally:
                    q.task_done()
    finally:
        loop.close()


def main(thread_count=5):
    threads:list[Thread] = []
    q = Queue()
    url_count = 100_000
    total_bytes = 0
    f_lock = Lock()
    
    # create a set of of url for each thread to process
    url_set_count = url_count // thread_count
    url_set = []
    for url in generate_valid_urls(url_count):
        if len(url_set) >= url_set_count:
            q.put(url_set)
            url_set = []
        url_set.append(url)

    # if we did not reach url_set_count but url_set contains url
    if url_set:
        q.put(url_set)

    class FailedCounter:
        def __init__(self) -> None:
            self.count = 0
            self.c_lock = Lock()

        def increment(self, count=1):
            with self.c_lock:
                self.count += count
    
    failed_counter = FailedCounter()

    with tempfile.NamedTemporaryFile("ab+", delete=True) as f:
        for _ in range(thread_count):
            t = Thread(
                target=get_and_write_data,
                args=(
                    q, 
                    f, 
                    f_lock,
                    failed_counter,
                )
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        f.flush()
        total_bytes = os.stat(f.name).st_size
    
    return total_bytes, failed_counter.count


if __name__ == "__main__":
    program_runner(
        main,
        "asyncio_plus_thread_with_100_000_urls",
        get_dir_name(__file__),
        thread_count=5,
        descr=f"""Io bound execution using 5 threads plus asyncio loop in each. The experiment fetches 100_000 urls and stores the response data into a file. The returned values represnt the total bytes received from network and the number of failed requests (>=400 status code or error)."""
    )


