import resource
from pathlib import Path

def generate_valid_urls(count=10000):
    param = "abcdefghijklmnopqrstuvwxyz"
    for i in range(count):
        url = f"http://to-httpbin-services-29cc40ffe47a42c4.elb.eu-west-3.amazonaws.com/anything/{i}?query={param}"

        if len(param.encode()) // 1000 >= 1:
            param = "abcdefghijklmnopqrstuvwxyz"
        else:
            param += param
        
        yield url


def get_dir_name(path_str:str):
    return Path(path_str).parent.name


def get_openable_fd_for_req():
    openable, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
    return 1000 if openable > 1024 else 500


def raise_fd_limit(count=2048):
    _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    new_soft = min(count, hard)
    resource.setrlimit(resource.RLIMIT_NOFILE, (new_soft, hard))
    new_soft, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
    return new_soft >= count



