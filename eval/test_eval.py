import pathlib

from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest
import dotenv

pytest_plugins = ("pytest_asyncio",)

@pytest.mark.asyncio
async def test_reject_weather_query():
    """Test the agent's ability to reject irrelevant questions."""
    await AgentEvaluator.evaluate(
        agent_module="linux_agent",
        eval_dataset_file_path_or_dir=str(pathlib.Path(__file__).parent / "data/reject-query.test.json"),
        num_runs=4,
        print_detailed_results=True,
    )
