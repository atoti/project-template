from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from functools import cached_property
from time import monotonic


@dataclass(frozen=True)
class Timeout:
    duration: timedelta
    started_at: float = field(default_factory=monotonic, init=False)

    @property
    def timed_out(self) -> bool:
        return monotonic() > self.started_at + self._duration_in_seconds

    @cached_property
    def _duration_in_seconds(self) -> float:
        return self.duration.total_seconds()
