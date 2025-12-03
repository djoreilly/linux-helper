import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def free_memory() -> str:
    """Get free and used memory in the system.
    Returns: the output of `free -h`.
    """
    cmd = "free -h"
    logger.info(f"Running command: {cmd}")
    return subprocess.getoutput(cmd)
