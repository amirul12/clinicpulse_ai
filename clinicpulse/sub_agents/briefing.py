"""Clinician briefing agent definitions."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ..agent_utils import suppress_output_callback
from ..config import config
from ..tools import fetch_patient_records, wait_for_lab_results


briefing_ensemble = Agent(
    name="clinician_briefing",
    model=config.critic_model,
    description="Produces doctor-ready patient dossiers.",
    instruction="""
    Combine `patient_intake`, `triage_priority`, and any fetched records into a concise briefing.
    Structure your Markdown with sections: Overview, Vitals/History, Risk Flags, Next Steps.
    Highlight missing information and propose clarifying questions for the clinician.
    """,
    tools=[
        FunctionTool(fetch_patient_records),
        FunctionTool(wait_for_lab_results),
    ],
    output_key="clinician_briefing",
    after_agent_callback=suppress_output_callback,
)
