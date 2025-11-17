"""Patient intake agent definitions."""

from google.adk.agents import Agent, LoopAgent

from ..agent_utils import suppress_output_callback
from ..config import config
from ..validation import IntakeValidationChecker


intake_agent = Agent(
    name="intake_collector",
    model=config.worker_model,
    description="Collects patient demographics and symptoms.",
    instruction="""
    You are the front-desk intake assistant. Ask clarifying questions until you have:
    - patient_id or name
    - primary symptoms
    - symptom duration
    - relevant medical history (if volunteered)
    Save your structured notes to the `patient_intake` state key.
    """,
    output_key="patient_intake",
    after_agent_callback=suppress_output_callback,
)


intake_loop = LoopAgent(
    name="intake_loop",
    description="Retries intake until validation passes",
    sub_agents=[
        intake_agent,
        IntakeValidationChecker(name="intake_validator"),
    ],
    max_iterations=3,
)
