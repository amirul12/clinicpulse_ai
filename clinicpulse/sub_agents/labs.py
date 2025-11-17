"""Lab wait/pause agent definitions."""

from google.adk.agents import Agent, LoopAgent

from ..agent_utils import suppress_output_callback
from ..config import config
from ..validation import LabResultsValidationChecker


lab_request_agent = Agent(
    name="lab_requester",
    model=config.worker_model,
    description="Pauses workflow until lab results are provided.",
    instruction="""
    If lab work or imaging is required, kindly request the outstanding results from the user.
    Store any provided details under the `lab_results` state key with keys:
      - patient_id
      - lab_summary
      - timestamp (if provided)
    Stay in this loop until the user supplies the results.
    """,
    output_key="lab_results",
    after_agent_callback=suppress_output_callback,
)


lab_wait_loop = LoopAgent(
    name="lab_wait_loop",
    description="Blocks until lab_results are available",
    sub_agents=[
        lab_request_agent,
        LabResultsValidationChecker(name="lab_results_validator"),
    ],
    max_iterations=5,
)
