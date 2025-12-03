from google.adk.agents import Agent

from .. import MODEL
from ..tools.memory import free_memory
from ..tools.top import top_processes_by_cpu, top_processes_by_memory

general_health_agent = Agent(
    name="general_health",
    description="Performs a general health check on the system",
    model=MODEL,
    instruction="""Use all the tools to do a general health check of the system.
    Be concise and only report details for things that may be problematic.
    Use the free_memory tool to check that the system has adequate free memory.
    Take note of any processes using a lot of cpu. Ignore the `top` process and don't mention it in your report.
    Report processes that are using a significant percent of memory.
    When commenting on processes, always include their pid and any pertinent information.
    """,
    tools=[free_memory, top_processes_by_cpu, top_processes_by_memory],
)
