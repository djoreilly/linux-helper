import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_process_using_port(port: int) -> str:
    """Use lsof to find the process using <port>.
    Args:
      port: the port number to check.
    Returns:
      str: the output of the `lsof -i :<port>` command.
    """
    cmd = ["lsof", "-i", f":{port}"]
    if os.geteuid() != 0:
        cmd.insert(0, "sudo")
    logger.info(f"Running command: {cmd}")
    process = subprocess.run(cmd, stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8")


def firewall_cmd_list_ports() -> str:
    """Use firewall-cmd to list open ports.
    Returns:
        str: the output of the `firewall-cmd --list-ports` command.
    """
    cmd = ["firewall-cmd", "--list-ports"]
    if os.geteuid() != 0:
        cmd.insert(0, "sudo")
    logger.info(f"Running command: {cmd}")
    process = subprocess.run(cmd, stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8")


def firewall_cmd_list_services() -> str:
    """Use firewall-cmd to list open services.
    Returns:
        str: the output of the `firewall-cmd --list-services` command.
    """
    cmd = ["firewall-cmd", "--list-services"]
    if os.geteuid() != 0:
        cmd.insert(0, "sudo")
    logger.info(f"Running command: {cmd}")
    process = subprocess.run(cmd, stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8")
