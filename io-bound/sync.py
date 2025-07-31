import os
import requests
import tempfile

from lib import generate_valid_urls, get_dir_name
from runner import program_runner


def main(url_count=50):
    failed_count = 0
    total_bytes = 0

    with tempfile.NamedTemporaryFile(mode="ab+", delete=True) as f:
        
        with requests.Session() as s:
            for url in generate_valid_urls(url_count):
                try:
                    response = s.get(url=url)
                except Exception as e:
                    print(e)
                    failed_count += 1
                    continue
                else:
                    if not response.ok:
                        print(response.status_code)
                        failed_count += 1
                        continue
                    f.write(response.content)
        
        f.flush()
        total_bytes = os.stat(f.name).st_size

    return total_bytes, failed_count


if __name__ == "__main__":
    program_runner(
        main,
        f"sync_data_with_100_urls",
        get_dir_name(__file__),
        url_count=100,
        descr=f"""Io bound execution using sync programming. The experiment fetches 100 urls and stores the response data into a file. The returned values represnt the total bytes received from network and the number of failed requests (>=400 status code or error)."""
    )
        

