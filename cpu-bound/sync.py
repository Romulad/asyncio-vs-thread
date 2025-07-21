from lib import generate_valid_urls, get_dir_name
from runner import program_runner


def count_char_bytes(url:str):
    # to make it takes more time
    char_bytes = 0
    for char in url:
        char_bytes += len(char.encode())
    return char_bytes

def main():
    total_bytes = 0
    for url in generate_valid_urls(1_00_000):
        total_bytes += count_char_bytes(url)
    return total_bytes


if __name__ == "__main__":
    program_runner(
        main, 
        "sync_data",
        get_dir_name(__file__),
        descr="Cpu bound execution in traditional sync mode",
    )
