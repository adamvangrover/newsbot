from typing import List, Dict, Any, Optional
import time

class MemoryStore:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.memories: List[Dict[str, Any]] = []

    def add(self, content: Any, metadata: Dict[str, Any] = None):
        if len(self.memories) >= self.capacity:
            self.memories.pop(0) # FIFO

        entry = {
            "timestamp": time.time(),
            "content": content,
            "metadata": metadata or {}
        }
        self.memories.append(entry)

    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Simple keyword search for now
        results = []
        for mem in reversed(self.memories):
            if query.lower() in str(mem["content"]).lower():
                results.append(mem)
            if len(results) >= limit:
                break
        return results

    def get_all(self) -> List[Dict[str, Any]]:
        return self.memories
