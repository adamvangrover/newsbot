import time
from typing import Dict, Any
from app.core.async_utils import task_manager

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.event_counts: Dict[str, int] = {}

    async def track_event(self, event_type: str):
        self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1

    def get_status(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": uptime,
            "uptime_formatted": self._format_uptime(uptime),
            "active_tasks_count": len(task_manager.get_active_tasks()),
            "active_tasks": task_manager.get_active_tasks(),
            "event_stats": self.event_counts,
            "status": "operational",
            "system_time": time.time()
        }

    def _format_uptime(self, seconds: float) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h)}h {int(m)}m {int(s)}s"

# Global instance
system_monitor = SystemMonitor()
