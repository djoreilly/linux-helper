import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def top_processes_by_cpu() -> str:
    """Get the top 10 processes by cpu usage.
    Returns:
        str: the top 10 processes from the top command without the summary.
    """
    cmd = "top -b -w=250 -n 1"
    logger.info(f"Running command: {cmd}")
    output = subprocess.getoutput(cmd)
    processes = [line for line in output.splitlines()]
    # skip the summary but take the header line
    return "\n".join(processes[6:17])


def top_processes_by_memory() -> str:
    """Get the top 10 processes by memory usage.
    Returns:
        str: the top 10 processes from the top command without the summary.
    """
    cmd = "top -b -w=250 -n 1 -o=+RES"
    logger.info(f"Running command: {cmd}")
    output = subprocess.getoutput(cmd)
    processes = [line for line in output.splitlines()]
    # skip the summary but take the header line
    return "\n".join(processes[6:17])
