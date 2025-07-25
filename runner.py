import time
import json
import os
from dataclasses import dataclass, asdict, field

import psutil

from cpu import CpuSupervisor, CpuUsage


@dataclass(frozen=True)
class Metrics:
    cpu: CpuUsage
    elapsed_seconds: float
    download_speed_per_s: float|None = field(default=None) 
    upload_speed_per_s: float|None = field(default=None)
    average_speed_per_s: float|None = field(default=None)
    description: str = field(default="")


def program_runner(fn, name, dir_name, *, descr="",  **kwargs):
    net_ts = psutil.net_io_counters()

    supervisor = CpuSupervisor()
    supervisor.start()

    start = time.perf_counter()
    result = fn(**kwargs)
    elapsed = time.perf_counter() - start
    
    supervisor.stop_checking()
    supervisor.join()

    net_te = psutil.net_io_counters()

    total_bytes_sent = net_te.bytes_sent - net_ts.bytes_sent
    total_bytes_receive = net_te.bytes_recv - net_ts.bytes_recv

    data = Metrics(
            cpu=supervisor.get_usage(),
            elapsed_seconds=elapsed,
            description=descr,
            download_speed_per_s=total_bytes_receive / elapsed,
            upload_speed_per_s=total_bytes_sent / elapsed,
            average_speed_per_s=(total_bytes_receive + total_bytes_sent) / elapsed / 2
    )
    data = asdict(data)
    data["returned_value(s)"] = result
    
    os.makedirs(f"{dir_name}/json", exist_ok=True)
    with open(f"{dir_name}/json/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

    return data, result


