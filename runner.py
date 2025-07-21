import time
import json
from dataclasses import dataclass, asdict, field

from cpu import CpuSupervisor, CpuUsage


@dataclass(frozen=True)
class Metrics:
    cpu: CpuUsage
    elapsed_seconds: float
    description: str = field(default="")


def program_runner(fn, name, dir_name, *, descr="",  **kwargs):
    supervisor = CpuSupervisor()
    supervisor.start()

    start = time.perf_counter()
    result = fn(**kwargs)
    elapsed = time.perf_counter() - start
    
    supervisor.stop_checking()
    supervisor.join()

    data = Metrics(
            cpu=supervisor.get_usage(),
            elapsed_seconds=elapsed,
            description=descr,
    )
    data = asdict(data)
    
    with open(f"{dir_name}/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

    return data, result


