import platform
from google.adk.agents import Agent
from ..tools.systemd import get_systemctl_status
from ..tools.network import (
    get_process_using_port,
    firewall_cmd_list_ports,
    firewall_cmd_list_services,
)
from .. import MODEL

LINUX_DISTRO = platform.freedesktop_os_release().get("ID", "unknown")

apache_agent = Agent(
    name="apache_agent",
    description="Troubleshoot apache problems.",
    model=MODEL,
    instruction=f"""Use the get_systemctl_status tool passing the
    systemd unit name that is used for apache on {LINUX_DISTRO}.
    Use the firewall-cmd tools for connectivity issues. If the firewall
    is running check that the required ports or services are open.
    """,
    tools=[
        get_systemctl_status,
        get_process_using_port,
        firewall_cmd_list_ports,
        firewall_cmd_list_services,
    ],
)
