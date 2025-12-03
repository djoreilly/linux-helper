import logging
import os
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


def get_systemctl_status(unit: str) -> str:
    """Gets the status of a systemd unit.
    Args:
      unit: the systemd unit.
    Returns:
      str: the output of the `systemctl status <unit>` command.
    """
    cmd = " ".join(["systemctl", "status", unit, "--no-pager"])
    if os.geteuid() != 0:
        cmd = "sudo " + cmd
    logger.info(f"Running command: {cmd}")
    return subprocess.getoutput(cmd)
