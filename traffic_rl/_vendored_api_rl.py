from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd


def load_rl(model_path: str = "models/demo_rl.pth"):
    raise FileNotFoundError(
        "RL API fallback engaged. To enable full functionality, keep the RL repo "
        "checked out next to this dashboard or vendor api_rl.py here."
    )


def run_rl_step(agent: Any, state: List[float]) -> Dict[str, Optional[float]]:
    return {"action": 0, "reward": None, "avg_wait_time": None}


def simulate_episode(agent: Any, env: Any, max_steps: int = 100) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time": list(range(max_steps)),
            "action": [0] * max_steps,
            "reward": [0.0] * max_steps,
            "avg_wait_time": [None] * max_steps,
            "queue_length": [None] * max_steps,
            "phase": [0] * max_steps,
            "junction_id": [None] * max_steps,
            "waiting_time": [None] * max_steps,
            "throughput": [None] * max_steps,
        }
    )


def make_dummy_episode(max_steps: int = 100) -> pd.DataFrame:
    """Generate dummy episode data for fallback."""
    import random
    import numpy as np
    
    records = []
    np.random.seed(42)
    
    for t in range(max_steps):
        action = random.randint(0, 3)
        reward = 0.5 + 0.3 * np.sin(t * 0.1) + np.random.normal(0, 0.1)
        avg_wait_time = max(0.0, 15.0 - t * 0.1 + 2 * np.sin(t * 0.05) + np.random.normal(0, 1.0))
        queue_length = max(0, int(40 - t * 0.3 + 5 * np.sin(t * 0.08) + np.random.normal(0, 2)))
        
        records.append({
            "time": t,
            "action": action,
            "reward": round(reward, 3),
            "avg_wait_time": round(avg_wait_time, 2),
            "queue_length": queue_length,
        })
    
    return pd.DataFrame.from_records(records)


