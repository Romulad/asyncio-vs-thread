import time
import json
import os
from functools import wraps
from dataclasses import dataclass, asdict, field

import psutil

from cpu import CpuSupervisor, CpuUsage
from memory import MemoryUsage, MemorySupervisor


@dataclass(frozen=True)
class Metrics:
    cpu: CpuUsage
    memory: MemoryUsage
    elapsed_seconds: float
    total_download: int|None = field(default=None)
    download_speed_per_s: float|None = field(default=None)
    total_upload: int|None = field(default=None)
    upload_speed_per_s: float|None = field(default=None)
    description: str = field(default="")


def network_usage_recorder(fn):
    @wraps(fn)
    def recorder(*arg, **kwargs):
        net_ts = psutil.net_io_counters() 

        data, result = fn(*arg, **kwargs)

        net_te = psutil.net_io_counters()

        total_bytes_sent = net_te.bytes_sent - net_ts.bytes_sent
        total_bytes_received = net_te.bytes_recv - net_ts.bytes_recv
        
        elapsed = data["elapsed_seconds"] # must exist

        data = {
            **data,
            "total_download": total_bytes_received,
            "download_speed_per_s": total_bytes_received / elapsed,
            "total_upload": total_bytes_sent,
            "upload_speed_per_s": total_bytes_sent / elapsed,
        }
        return data, result
    return recorder


def memory_usage_recorder(fn):
    @wraps(fn)
    def recorder(*arg, **kwargs):
        supervisor = MemorySupervisor()
        supervisor.start()

        data, result = fn(*arg, **kwargs)

        supervisor.stop_checking()
        supervisor.join()

        data = {
            **data,
            "memory": supervisor.get_usage()
        }
        return data, result
    return recorder


def cpu_usage_recorder(fn):
    @wraps(fn)
    def recorder(*arg, **kwargs):
        supervisor = CpuSupervisor()
        supervisor.start()

        data, result = fn(*arg, **kwargs)
        
        supervisor.stop_checking()
        supervisor.join()

        data = {
            **data,
            "cpu": supervisor.get_usage()
        }
        return data, result
    return recorder


def elapsed_time_recorder(fn):
    @wraps(fn)
    def recorder(*arg, **kwargs):
        start = time.perf_counter()
        data, result = fn(*arg, **kwargs)
        elapsed = time.perf_counter() - start

        data = {
            **data,
            "elapsed_seconds": elapsed
        }
        return data, result
    return recorder


@network_usage_recorder
@cpu_usage_recorder
@memory_usage_recorder
@elapsed_time_recorder
def execute(fn, **kwargs):
    result = fn(**kwargs)
    return {}, result


def program_runner(fn, name, dir_name, *, descr="",  **kwargs):
    metric_data, result =  execute(fn, **kwargs)

    data = Metrics(
        **metric_data,
        description=descr,
    )

    data = asdict(data)
    data["returned_value(s)"] = result
    
    os.makedirs(f"{dir_name}/json", exist_ok=True)
    with open(f"{dir_name}/json/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

    return data, result


