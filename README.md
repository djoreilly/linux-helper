# Linux troubleshooting assistant

AI-driven agent for troubleshooting Linux problems PoC. Built on the [Google ADK framework](https://google.github.io/adk-docs/) as a [Multi-Agent System](https://google.github.io/adk-docs/agents/multi-agents/).
The project structure follows the [Python Sample Agents](https://github.com/google/adk-samples/tree/main/python/agents).

## Overview
```
                       ┌──────────────────────────────────────┐
                       │               root_agent             │
                       │                                      │
                       │ instruction: help user troubleshoot  │
                       │              their linux system.     │
                       │                                      │
                       │ sub_agents: general_health_agent,    │
                       │             apache_agent             │
                       └──────────────────────────────────────┘

        ┌───────────────────────────────┐    ┌─────────────────────────────────┐
        │      general_health_agent     │    │           apache_agent          │
        │                               │    │                                 │
        │  instruction: Use the tools...│    │ instruction: Use the get_sys... │
        │                               │    │                                 │
        │  tools: free_memory,          │    │ tools: get_systemctl_status,    │
        │         failed_systemd_units, │    │        firewall_cmd_list_ports, │
        │         ...                   │    │        ...                      │
        └───────────────────────────────┘    └─────────────────────────────────┘
```
This is a PoC and only has a couple of sub-agents. The [root_agent](linux_agent/agent.py) takes the user prompt and delegates to the [sub-agent](linux_agent/sub_agents) it thinks best based on their descriptions. The sub-agent runs with its own context and specific instructions, using its read-only tools to get information from the system.

The [tools](linux_agent/tools) are very simple - each one executes a common Linux command and returns the standard output to the LLM. Since LLMs have lots of Linux commands/outputs in their training data, they are usually able to make a good determination. A sub-agent is able to transfer control to another peer sub-agent, and each one will report to the user if they find something that might be the root-cause.

The assistant may propose steps to fix the problem, or the user might need to ask followup questions for that. The assistant does not make changes to the system - it's up to the user to review the output and make any changes manually.

## Installation
This project uses [uv](https://github.com/astral-sh/uv) for dependency management which can usually be installed with your package manager.
```
uv sync
```

## Running the agent
Note: [tools](linux_agent/tools) are used to get information from the system. These are read-only, but root is often needed to get detailed information - sudo will be tried.

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
## Evaluation
Follow the [doc](https://google.github.io/adk-docs/evaluate/#second-approach-using-an-evalset-file) to create a EvalSet using the UI. Start a session and run a prompt like "Is Apache running?" and add the session to the EvalSet - see [example](linux_agent/evalset4972e0.evalset.json). Then run the EvalSet and it will check that the same agent trajectory and toolcalls as the recorded session were run (`tool_trajectory_avg_score` is 1.0, requires 100% to pass). The [response_match_score](https://google.github.io/adk-docs/evaluate/criteria/#response_match_score) criteria needs to be low, like 0.2 in this case. Instead use the [final_response_match_v2](https://google.github.io/adk-docs/evaluate/criteria/#final_response_match_v2) criteria by creating a [EvalConfig](eval-config.json) and run like:
```bash
(linux-helper) doreilly@leapai:~/linux-helper> adk eval --print_detailed_results --config_file_path eval-config.json linux_agent linux_agent/evalset4972e0.evalset.json
...
*********************************************************************
Eval Run Summary
evalset4972e0:
  Tests passed: 1
  Tests failed: 0
********************************************************************
Eval Set Id: evalset4972e0
Eval Id: case841f89
Overall Eval Status: PASSED
---------------------------------------------------------------------
Metric: final_response_match_v2, Status: PASSED, Score: 1.0, Threshold: 0.8
---------------------------------------------------------------------
Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0
---------------------------------------------------------------------
Invocation Details:
+----+-------------------+--------------------------+--------------------------+---------------------------+---------------------------+---------------------------+-----------------------------+
|    | prompt            | expected_response        | actual_response          | expected_tool_calls       | actual_tool_calls         | final_response_match_v2   | tool_trajectory_avg_score   |
+====+===================+==========================+==========================+===========================+===========================+===========================+=============================+
|  0 | is apache running | Yes, apache2 is running. | Yes, Apache is running.  | id='adk-0dfc0b2b-d28c-4ba | id='adk-bf6b4c8f-5562-4d8 | Status: PASSED, Score:    | Status: PASSED, Score:      |
|    |                   | The output of `systemctl | The `apache2.service` is | 1-859d-67933273be50'      | 7-be37-169373b23778'      | 1.0                       | 1.0                         |
|    |                   | status apache2` shows    | active and has been      | args={'agent_name':       | args={'agent_name':       |                           |                             |
|    |                   | that the service is      | running for 1 week and 0 | 'apache_agent'}           | 'apache_agent'}           |                           |                             |
|    |                   | active (running).        | days.                    | name='transfer_to_agent'  | name='transfer_to_agent'  |                           |                             |
|    |                   |                          |                          | partial_args=None         | partial_args=None         |                           |                             |
|    |                   |                          |                          | will_continue=None        | will_continue=None id='ad |                           |                             |
|    |                   |                          |                          | id='adk-af5fc7af-8fd6-48c | k-a780798a-1ba8-4f2f-9e91 |                           |                             |
|    |                   |                          |                          | 9-86a5-f78a387a9c22'      | -6477743a400e'            |                           |                             |
|    |                   |                          |                          | args={'unit': 'apache2'}  | args={'unit': 'apache2'}  |                           |                             |
|    |                   |                          |                          | name='get_systemctl_statu | name='get_systemctl_statu |                           |                             |
|    |                   |                          |                          | s' partial_args=None      | s' partial_args=None      |                           |                             |
|    |                   |                          |                          | will_continue=None        | will_continue=None        |                           |                             |
+----+-------------------+--------------------------+--------------------------+---------------------------+---------------------------+---------------------------+-----------------------------+
```
