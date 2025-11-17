"""Triage agent definitions."""

from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool, google_search

from ..agent_utils import suppress_output_callback
from ..config import config
from ..tools import fetch_patient_records, record_triage_decision
from ..validation import TriageValidationChecker


triage_agent = Agent(
    name="triage_coordinator",
    model=config.critic_model,
    description="Assigns priority levels using guidelines and tools.",
    instruction="""
    You are a clinical triage nurse. Review the `patient_intake` state, optionally
    run Google Search to confirm protocol, call tools like `record_triage_decision`,
    then write the triage summary to the `triage_priority` key with fields:
      - patient_id
      - priority_level (Critical | Urgent | Routine)
      - rationale
      - recommended_next_steps
    """,
    tools=[
        google_search,
        FunctionTool(fetch_patient_records),
        FunctionTool(record_triage_decision),
    ],
    output_key="triage_priority",
    after_agent_callback=suppress_output_callback,
)


triage_loop = LoopAgent(
    name="triage_loop",
    description="Retries triage decisions if validation fails",
    sub_agents=[
        triage_agent,
        TriageValidationChecker(name="triage_validator"),
    ],
    max_iterations=3,
)
