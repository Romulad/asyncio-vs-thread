import asyncio
import os
import time
from pathlib import Path
from tempfile import gettempdir

from aiofile import async_open, FileIOWrapperBase
import aiohttp

from lib import (
    generate_valid_urls, 
    get_dir_name, 
    get_openable_fd_for_req,
    raise_fd_limit
)
from runner import program_runner


async def get_and_write_data(
    url:str,
    client: aiohttp.ClientSession, 
    af:FileIOWrapperBase
):
    try:
        async with client.get(url) as response:
            if not response.ok:
                print(response.status)
                return False
            await af.write(await response.read())
    except Exception as e:
        print(repr(e))
        return False
    else:
        return True


async def main(url_count=50):
    tmp_filenam = Path(gettempdir()) / "data"
    failed_count = 0
    total_bytes = 0
    tcp_connector = aiohttp.TCPConnector(
        limit=get_openable_fd_for_req(),
        ttl_dns_cache=60*60*10
    )

    async with async_open(tmp_filenam, "ab+") as af:
        
        async with aiohttp.ClientSession(connector=tcp_connector) as client:
            results = await asyncio.gather(
                *[
                    get_and_write_data(url, client, af) 
                    for url in generate_valid_urls(url_count)
                ]
            )
            failed_count = url_count - sum(results)
        
        await af.flush()
        total_bytes = os.stat(tmp_filenam).st_size
    
    os.unlink(tmp_filenam)

    return total_bytes, failed_count


if __name__ == "__main__":
    raised = raise_fd_limit()
    print("Raised fd limit", raised)

    def execute(url_count=100_000):
        return asyncio.run(main(url_count))
    
    for count in [10_000, 100_000]:
        print("Execution for:", count, "urls")
        program_runner(
            execute,
            f"asyncio_data_with_{count}_urls",
            get_dir_name(__file__),
            url_count=count,
            descr=f"""Io bound execution using asyncio programming. The experiment fetches {count} urls and stores the response data into a file. The returned values represnt the total bytes received from network and the number of failed requests (>=400 status code or error)."""
        )
        time.sleep(10)
