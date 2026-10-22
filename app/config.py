"""Workshop task tracker configuration. Solution state."""
import os

# Challenge 2: read from the environment; no secrets in source.
SECRET_KEY = os.environ.get("TASK_API_SECRET", "dev-only-insecure-key")

# Challenge 1 bonus: DEBUG is a deployment concern, not a source constant.
DEBUG = os.environ.get("TASK_API_DEBUG", "false").lower() == "true"


def data_file():
    """Storage location for tasks. Override with TASKS_FILE in tests."""
    return os.environ.get("TASKS_FILE", "data/tasks.json")
