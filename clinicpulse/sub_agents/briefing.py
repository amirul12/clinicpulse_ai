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
    You are creating a comprehensive clinician briefing. Combine all available information into a well-structured Markdown dossier.
    
    **Data Sources:**
    - `patient_intake` - Patient demographics, symptoms, duration, medical history
    - `triage_priority` - Priority level, rationale, recommended next steps
    - `appointment_details` - Scheduled appointment information
    - `fetch_patient_records` - Additional EHR data (call this tool)
    - `lab_results` - Lab data if available
    
    **Required Sections:**
    
    ## Patient Overview
    - Patient ID/Name
    - Chief Complaint (primary symptoms)
    - Duration of symptoms
    - Priority Level (Critical/Urgent/Routine)
    
    ## Medical History & Vitals
    - Chronic conditions
    - Allergies
    - Current medications (if available)
    - Relevant past medical history
    
    ## Triage Assessment
    - Priority level and rationale
    - Clinical reasoning
    - Risk factors identified
    
    ## Appointment Details
    - Scheduled with: [Doctor name and specialty]
    - Date/Time: [Appointment datetime]
    - Location: [Clinic location]
    - Appointment ID: [ID for reference]
    
    ## Risk Flags & Alerts
    - Any red flags or concerning symptoms
    - Urgent interventions needed
    - Safety considerations
    
    ## Recommended Next Steps
    - Diagnostic tests needed
    - Treatment considerations
    - Follow-up requirements
    - Questions for the clinician to ask
    
    **Highlight missing information** and propose clarifying questions for the clinician.
    Be concise but thorough. Use professional medical terminology.
    """,
    tools=[
        FunctionTool(fetch_patient_records),
        FunctionTool(wait_for_lab_results),
    ],
    output_key="clinician_briefing",
    after_agent_callback=suppress_output_callback,
)
