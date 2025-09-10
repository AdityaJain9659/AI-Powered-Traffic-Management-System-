from __future__ import annotations

"""
Bridge import from dashboard to RL repo.

This module imports the RL API from the sibling Traffic-simulation-rl repo.
The RL repo is the source of truth for all RL functionality.
"""

from pathlib import Path
import sys

# Add RL repo to path for imports
_root = Path(__file__).resolve().parents[1]
_rl_repo = _root.parent / "Traffic-simulation-rl"

if str(_rl_repo) not in sys.path:
    sys.path.insert(0, str(_rl_repo))

try:
    # Import from the actual RL repo
    from api_rl import load_rl, run_rl_step, simulate_episode, make_dummy_episode  # noqa: F401
except ImportError as e:
    # Fallback to vendored version if RL repo not available
    print(f"Warning: Could not import from RL repo: {e}")
    from ._vendored_api_rl import *  # type: ignore  # noqa: F401,F403


