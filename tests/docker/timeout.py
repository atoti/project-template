from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Timeout:
    duration: timedelta
    started_at: datetime = field(default_factory=datetime.now, init=False)

    @property
    def timed_out(self) -> bool:
        return datetime.now() > self.started_at + self.duration
