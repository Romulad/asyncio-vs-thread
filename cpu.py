import time
from threading import Thread
from dataclasses import dataclass, field

import psutil


@dataclass(frozen=True)
class CpuUsage:
    sys_max_usage: float
    sys_min_usage: float
    sys_average_usage: float
    proc_max_usage: float
    proc_min_usage: float
    proc_average_usage: float
    recording_interval: float
    sys_usage: list[float] = field(default_factory=list)
    proc_usage: list[float] = field(default_factory=list)
    core_count: int|None = field(default=psutil.cpu_count(logical=True))
    meaning: dict = field(default_factory=lambda: {
            "proc": "Stands for process, the process in which the program is running ",
            "sys": "Stands for system, the whole system",
            "recording_interval": "Time in second between CPU usage record"
    })


class CpuSupervisor(Thread):
    _proc = psutil.Process()
    _pst = psutil

    def __init__(self, interval=0.5) -> None:
        super().__init__()
        self._keep_checking = True
        self._interval = interval
        self.sys_wide_usage = []
        self.proc_usage = []

    def run(self) -> None:
        self._pst.cpu_percent(interval=None)
        self._proc.cpu_percent(interval=None)
        while self._keep_checking:
            time.sleep(self._interval)
            self.sys_wide_usage.append(self._pst.cpu_percent())
            self.proc_usage.append(self._proc.cpu_percent())

    def stop_checking(self):
        self._keep_checking = False

    def get_usage(self):
        cpu_usage = CpuUsage(
                sys_average_usage=sum(self.sys_wide_usage) / len(self.sys_wide_usage),
                sys_max_usage=max(self.sys_wide_usage),
                sys_min_usage=min(self.sys_wide_usage),
                sys_usage=self.sys_wide_usage,
                proc_average_usage=sum(self.proc_usage) / len(self.proc_usage),
                proc_max_usage=max(self.proc_usage),
                proc_min_usage=min(self.proc_usage),
                proc_usage=self.proc_usage,
                recording_interval=self._interval,
        )
        return cpu_usage


