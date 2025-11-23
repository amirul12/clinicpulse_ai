"""Main agent orchestration for ClinicPulse AI."""

import datetime

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .sub_agents import (
    appointment_loop,
    briefing_ensemble,
    intake_loop,
    lab_wait_loop,
    triage_loop,
)
from .tools import (
    book_appointment,
    check_doctor_availability,
    fetch_patient_records,
    record_triage_decision,
    send_appointment_confirmation,
    wait_for_lab_results,
)


clinicpulse_agent = Agent(
    name="clinicpulse_ai",
    model=config.worker_model,
    description="ClinicPulse AI orchestrates intake, triage, and clinician briefings for outpatient clinics.",
    instruction=f"""
    You are ClinicPulse AI, the digital flow manager for clinics. You AUTOMATICALLY progress through this pipeline:

    **WORKFLOW (Execute automatically in sequence):**
    
    1. **Intake Phase** – Delegate to `intake_loop` to collect patient information.
       - Ask questions one at a time through the intake agent
       - Wait for user responses during this phase
       - Once `patient_intake` state has all required fields, AUTOMATICALLY proceed to step 2
       
    2. **Triage Phase** – IMMEDIATELY call `triage_loop` after intake completes.
       - The triage agent will assess priority level
       - Once `triage_priority` state is set, AUTOMATICALLY proceed to step 3
       
    3. **Appointment Scheduling** – IMMEDIATELY call `appointment_loop` after triage completes.
       - The appointment agent will book based on triage priority
       - Once `appointment_details` state is set, AUTOMATICALLY proceed to step 4
       
    4. **Clinician Briefing** – IMMEDIATELY call `briefing_ensemble` after appointment is booked.
       - Generate the final dossier
       - Set `clinician_briefing` state
       
    5. **Labs (Optional)** – Only if diagnostics are needed, call `lab_wait_loop` before briefing.

    **CRITICAL RULES:**
    - During INTAKE: Ask one question, wait for response, repeat until complete
    - After INTAKE completes: AUTOMATICALLY run triage → appointment → briefing WITHOUT waiting for user
    - Provide status updates: "[Intake complete] → [Triage complete] → [Appointment booked] → [Briefing ready]"
    - Don't ask "Would you like me to..." - just DO the next step automatically
    
    **Available Tools (use as needed):**
    - `fetch_patient_records` – Get EHR data
    - `record_triage_decision` – Log triage decisions
    - `check_doctor_availability` – Check appointment slots
    - `book_appointment` – Book appointments manually
    - `send_appointment_confirmation` – Send confirmations
    - `wait_for_lab_results` – Pause for lab data

    Be concise and professional. Today's date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        intake_loop,          # Step 1: Collect patient information
        triage_loop,          # Step 2: Assess priority level
        appointment_loop,     # Step 3: Schedule doctor appointment
        briefing_ensemble,    # Step 4: Generate clinician briefing
        lab_wait_loop,        # Step 5: Optional - wait for lab results if needed
    ],
    tools=[
        FunctionTool(fetch_patient_records),
        FunctionTool(record_triage_decision),
        FunctionTool(wait_for_lab_results),
        FunctionTool(check_doctor_availability),
        FunctionTool(book_appointment),
        FunctionTool(send_appointment_confirmation),
    ],
    output_key="clinician_briefing",
)


root_agent = clinicpulse_agent
