import json
import time
import functools
from pathlib import Path

CHECKPOINT_FILE = Path("checkpoints.json")

# Save workflow checkpoint
def save_checkpoint(user_id, node_name, state_dict):
    """Save the state after a workflow node completes."""
    if CHECKPOINT_FILE.exists():
        checkpoints = json.loads(CHECKPOINT_FILE.read_text())
    else:
        checkpoints = {}
    checkpoints[user_id] = {"node": node_name, "state": state_dict}
    CHECKPOINT_FILE.write_text(json.dumps(checkpoints, indent=2))

# Load workflow checkpoint
def load_checkpoint(user_id):
    """Retrieve the last saved state for a given user."""
    if CHECKPOINT_FILE.exists():
        checkpoints = json.loads(CHECKPOINT_FILE.read_text())
        return checkpoints.get(user_id)
    return None

# Retry decorator
def retry(max_attempts=3, delay=2):
    """Automatically retry a function call if it fails."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[Retry] Error: {e} (Attempt {attempts}/{max_attempts})")
                    if attempts == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
