from google.adk.agents import Agent

MODEL = "gemini-2.0-flash"

root_agent = Agent(
    name="linux_troubleshooter",
    description="linux troubleshooting assistant",
    model=MODEL,
    instruction="""Help the user troubleshoot their linux problems.
    """,
    # automatic delegation (AutoFlow): llm considers its own instructions/tools and descriptions from sub-agents.
    sub_agents=[],
)
