import time
from threading import Thread
from dataclasses import dataclass, field

import psutil


@dataclass(frozen=True)
class MemoryUsage:
    max_usage: int
    min_usage: int
    average_usage: float
    recording_interval: float
    usage: list[float] = field(default_factory=list)
    meaning: dict = field(default_factory=lambda: {
        "recording_interval": "Time in second between memory usage record"
    })


class MemorySupervisor(Thread):
    _proc = psutil.Process()

    def __init__(self, interval=0.5) -> None:
        super().__init__()
        self._interval = interval
        self._keep_checking = True
        self.usage = []

    def run(self) -> None:
        while self._keep_checking:
            self.usage.append(self._proc.memory_info().rss)
            time.sleep(self._interval)
    
    def stop_checking(self):
        self._keep_checking = False

    def get_usage(self):
        return MemoryUsage(
            max_usage=max(self.usage),
            min_usage=min(self.usage),
            average_usage=sum(self.usage) / len(self.usage),
            usage=self.usage,
            recording_interval=self._interval,
        )


