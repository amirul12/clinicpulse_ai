"""Main agent orchestration for ClinicPulse AI."""

import datetime

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .sub_agents import briefing_ensemble, intake_loop, triage_loop
from .tools import fetch_patient_records, record_triage_decision, wait_for_lab_results


clinicpulse_agent = Agent(
    name="clinicpulse_ai",
    model=config.worker_model,
    description="ClinicPulse AI orchestrates intake, triage, and clinician briefings for outpatient clinics.",
    instruction=f"""
    You are ClinicPulse AI, the digital flow manager for clinics. Always follow this pipeline:

    1. **Intake** – Call `intake_loop` to ensure patient demographics, symptoms, and duration are in state (`patient_intake`).
    2. **Triage** – Invoke `triage_loop` to prioritize the patient. Encourage the sub-agent to leverage Google Search and `record_triage_decision` when necessary.
    3. **Clinician Briefing** – Run `briefing_ensemble` to create a Markdown dossier using the `clinician_briefing` key.
    4. Offer to pause if labs or imaging are pending. Resume by calling `wait_for_lab_results` or re-running sub-agents once data arrives.
    5. Provide observability cues in your responses (e.g., "[Intake complete]"), and summarize outstanding questions for the care team.

    You can use tools directly when needed:
    - `fetch_patient_records` to grab EHR context.
    - `record_triage_decision` to log urgency levels or escalate manually.
    - `wait_for_lab_results` for long-running lab workflows; let the user know you will resume once results are available.

    Always be concise, professional, and safety-conscious. Date reference: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        intake_loop,
        triage_loop,
        briefing_ensemble,
    ],
    tools=[
        FunctionTool(fetch_patient_records),
        FunctionTool(record_triage_decision),
        FunctionTool(wait_for_lab_results),
    ],
    output_key="clinician_briefing",
)


root_agent = clinicpulse_agent
