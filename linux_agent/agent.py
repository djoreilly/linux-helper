from google.adk.agents import Agent
from .sub_agents.general_health import general_health_agent

from . import MODEL

root_agent = Agent(
    name="linux_troubleshooter",
    description="linux troubleshooting assistant",
    model=MODEL,
    instruction="""Help the user troubleshoot their linux problems.
    """,
    # automatic delegation (AutoFlow): llm considers its own instructions/tools and descriptions from sub-agents.
    sub_agents=[general_health_agent],
)
