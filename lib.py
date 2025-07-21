from pathlib import Path

def generate_valid_urls(count=10000):
    param = "abcdefghijklmnopqrstuvwxyz"
    for i in range(count):
        url = f"https://httpbin.org/anything/{i}?query={param}"

        if len(param.encode()) // 1000 >= 1:
            param = "abcdefghijklmnopqrstuvwxyz"
        else:
            param += param
        
        yield url


def get_dir_name(path_str:str):
    return Path(path_str).parent.name
