from typing import List, Dict, Any

class CognitivePlanner:
    def __init__(self):
        pass

    def plan_action(self, goal: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simple rule-based planner.
        """
        plan = {
            "goal": goal,
            "timestamp": context.get("timestamp"),
            "strategy": "heuristic",
            "actions": []
        }

        if "analyze" in goal.lower():
             plan["actions"].append("fetch_data")
             plan["actions"].append("process_sentiment")
             plan["actions"].append("summarize")
        elif "evolve" in goal.lower():
             plan["actions"].append("load_population")
             plan["actions"].append("run_mutation")
             plan["actions"].append("evaluate_fitness")
        else:
             plan["actions"].append("log_activity")

        return plan
