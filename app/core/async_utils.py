import asyncio
from typing import Dict, Any, List
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AsyncTaskManager:
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.task_metadata: Dict[str, Dict[str, Any]] = {}

    async def start_task(self, name: str, coro) -> str:
        task_id = str(uuid.uuid4())
        try:
            task = asyncio.create_task(coro)
            self.tasks[task_id] = task
            self.task_metadata[task_id] = {
                "name": name,
                "start_time": datetime.now().isoformat(),
                "status": "running"
            }
            task.add_done_callback(lambda t: self._cleanup_task(task_id, t))
            logger.info(f"Started task {name} ({task_id})")
            return task_id
        except Exception as e:
            logger.error(f"Failed to start task {name}: {e}")
            return ""

    def _cleanup_task(self, task_id: str, task: asyncio.Task):
        if task_id in self.task_metadata:
            self.task_metadata[task_id]["status"] = "completed"
            self.task_metadata[task_id]["end_time"] = datetime.now().isoformat()

            # Check for exceptions
            try:
                task.result()
            except Exception as e:
                self.task_metadata[task_id]["status"] = "failed"
                self.task_metadata[task_id]["error"] = str(e)
                logger.error(f"Task {task_id} failed: {e}")

            # Remove from active tasks map
            if task_id in self.tasks:
                del self.tasks[task_id]

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        return [
            {"id": k, **v}
            for k, v in self.task_metadata.items()
            if v["status"] == "running"
        ]

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return [{"id": k, **v} for k, v in self.task_metadata.items()]

# Global instance
task_manager = AsyncTaskManager()
