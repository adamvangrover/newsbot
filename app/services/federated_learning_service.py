import asyncio
import random
import logging
from typing import Dict, Any, List
from datetime import datetime
from app.core.async_utils import task_manager
from app.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class FederatedLearningService:
    def __init__(self):
        self.is_running = False
        self.round_id = 0
        self.global_accuracy = 0.50
        self.participants = ["Node_Alpha", "Node_Beta", "Node_Gamma", "Node_Delta"]
        self.task_id = None
        self.status = "idle"

    async def start_training(self):
        if self.is_running:
            return
        self.is_running = True
        self.status = "training"
        self.task_id = await task_manager.start_task("federated_learning_loop", self._training_loop())
        logger.info("Federated Learning Service started.")
        await event_bus.publish("fl_status_change", self.get_status())

    async def stop_training(self):
        self.is_running = False
        self.status = "stopped"
        logger.info("Federated Learning Service stopping...")
        await event_bus.publish("fl_status_change", self.get_status())

    async def _training_loop(self):
        while self.is_running:
            self.round_id += 1
            await event_bus.publish("fl_round_start", {"round": self.round_id})

            # Simulate local training on nodes
            await asyncio.sleep(2)

            # Aggregate updates (Simulated)
            improvement = random.uniform(0.005, 0.02) * (1 - self.global_accuracy) # Diminishing returns
            self.global_accuracy += improvement

            await event_bus.publish("fl_model_updated", {
                "round": self.round_id,
                "accuracy": self.global_accuracy,
                "improvement": improvement,
                "timestamp": datetime.now().isoformat()
            })

            logger.info(f"FL Round {self.round_id} complete. Accuracy: {self.global_accuracy:.4f}")
            await asyncio.sleep(3) # Wait for next round

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "round": self.round_id,
            "accuracy": self.global_accuracy,
            "participants": len(self.participants),
            "node_list": self.participants
        }

# Global instance
fl_service = FederatedLearningService()
