from collections import deque
from typing import Any


class DashboardState:
    """Estado en memoria para observabilidad en tiempo real."""

    def __init__(self) -> None:
        self.recent_signals: deque[dict[str, Any]] = deque(maxlen=100)

    def push(self, item: dict[str, Any]) -> None:
        self.recent_signals.appendleft(item)

    def snapshot(self) -> dict[str, Any]:
        return {
            "recent_signals": list(self.recent_signals),
            "tracked_pairs": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"],
        }
