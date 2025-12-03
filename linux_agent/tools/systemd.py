import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def failed_systemd_units() -> str:
    """Get systemd units in failed status.
    Returns:
        str: the output of `systemctl list-units --failed --no-pager --quiet`
    """
    cmd = "systemctl list-units --failed --no-pager --quiet"
    logger.info(f"Running command: {cmd}")
    return subprocess.getoutput(cmd)
