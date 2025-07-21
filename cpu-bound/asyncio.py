import asyncio

from lib import generate_valid_urls, get_dir_name
from runner import program_runner


async def count_char_bytes(url:str):
    # to make it takes more time
    char_bytes = 0
    for char in url:
        char_bytes += len(char.encode())
    return char_bytes

async def main():
    total_bytes = 0
    for url in generate_valid_urls(1_00_000):
        total_bytes += await count_char_bytes(url)
    return total_bytes


if __name__ == "__main__":
    def execute():
        return asyncio.run(main())

    program_runner(
        execute,
        "asyncio_data",
        get_dir_name(__file__),
        descr="Cpu bound execution with asyncio"
    )
