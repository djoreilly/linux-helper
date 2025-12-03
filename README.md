# Linux troubleshooting assistant

AI-driven agent for troubleshooting Linux problems. Built on the [Google ADK framework](https://google.github.io/adk-docs/) as a [Multi-Agent System](https://google.github.io/adk-docs/agents/multi-agents/).
The project structure follows the [Python Sample Agents](https://github.com/google/adk-samples/tree/main/python/agents).

## Installation
This project uses [uv](https://github.com/astral-sh/uv) for dependency management which can usually be installed with your package manager.
```
uv sync
```

## Running the agent
Note: [tools](linux_agent/tools) are used to get information from the system. These are read-only, but root is needed to get detailed information from [systemctl status](linux_agent/tools/systemd.py). Sudo will be tried.

Using ADK CLI:
```
export GEMINI_API_KEY=
uv run adk run linux_agent
```

Using the ADK Dev UI:
```
export GEMINI_API_KEY=
uv run adk web
```

## Example Interactions
### Apache
Break apache by taking port 80:
```
$ sudo systemctl stop apache2.service
$ sudo nc -l 80 &
$ sudo systemctl start apache2.service
Job for apache2.service failed because the control process exited with error code.
See "systemctl status apache2.service" and "journalctl -xeu apache2.service" for details.
```

Run the agent:
```
$ uv run adk run linux_agent
...
Running agent linux_troubleshooter, type exit to exit.
[user]: do a health check
[general_health]: The system has adequate free memory.

The following systemd unit is in a failed state: apache2.service. I will transfer this to the apache agent.

[apache_agent]: The apache2.service unit is in a failed state. I will check the status of the apache2 service.

[apache_agent]: The Apache webserver failed to start because address 80 is already in use. This usually means another process is already listening on that port.
```

Sometimes it fails to transfer automatically to another agent. The user can nudge it, e.g.:
```
$ uv run adk run linux_agent
...
[user]: do a health check
[general_health]: The system has adequate free memory.

The following processes are using a significant amount of memory:
*   PID 12025 (adk) is using 1.662% of memory.

The following systemd units are in a failed state:
*   apache2.service: This indicates a problem with the Apache web server.

[user]: follow up on the apache problem
[apache_agent]: The apache2.service failed to start because the address [::]:80 and 0.0.0.0:80 are already in use. This usually means another process is already listening on port 80. It could be another web server or some other application.

Here's how to troubleshoot:
...
```
