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

Currently only Google models are supported. The default model is `gemini-2.0-flash` and can be overridden by setting `GOOGLE_GENAI_MODEL`:
```
export GOOGLE_GENAI_MODEL=gemini-2.5-flash
```

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
Running agent linux_troubleshooter, type exit to exit.
[user]: do a health check
[general_health]: Here's a concise system health report:

**Problematic Processes (Memory Usage):**
*   **adk** (PID 12569) is using 1.663% of memory.

**Failed Systemd Units:**
*   **apache2.service** is in a failed state.

[user]: follow up on the apache problem

[apache_agent]: The Apache webserver is failing to start because another process, `nc` with PID 11311 and user root, is already using port 80. To resolve this, you need to stop the `nc` process or reconfigure it to use a different port so that Apache can bind to port 80.
[user]: exit
```
