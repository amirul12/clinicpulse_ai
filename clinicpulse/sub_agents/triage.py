"""Triage agent definitions."""

from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool

from ..agent_utils import suppress_output_callback
from ..config import config
from ..tools import fetch_patient_records, record_triage_decision
from ..validation import TriageValidationChecker


triage_agent = Agent(
    name="triage_coordinator",
    model=config.critic_model,
    description="Assigns priority levels using guidelines and tools.",
    instruction="""
    You are a clinical triage nurse. Your job is to assess the patient's urgency level AND determine if lab tests are needed.
    
    STEPS:
    1. Review the `patient_intake` state (symptoms, duration, history)
    2. Call `fetch_patient_records` to get additional medical history
    3. Determine priority level based on symptoms:
       - **Critical**: Life-threatening (chest pain, severe bleeding, difficulty breathing)
       - **Urgent**: Needs prompt attention (high fever, severe pain, suspected fracture)
       - **Routine**: Can wait for regular appointment (minor symptoms, follow-ups)
    4. ASSESS LAB REQUIREMENTS - Determine if diagnostic tests are needed BEFORE doctor appointment:
       - **Labs Needed**: Chest pain (ECG, cardiac enzymes), fever with infection signs (CBC, cultures), 
         suspected fractures (X-ray), abdominal pain (bloodwork, imaging), chronic disease monitoring
       - **No Labs Needed**: Minor injuries, simple infections treatable clinically, routine follow-ups,
         conditions requiring only physical examination
    5. Call `record_triage_decision` with patient_id and priority_level
    6. Save to `triage_priority` state with ALL fields:
       {
         "patient_id": "from intake",
         "priority_level": "Critical|Urgent|Routine",
         "rationale": "brief clinical reasoning",
         "recommended_next_steps": "what should happen next",
         "needs_labs": true or false,
         "lab_tests_recommended": ["test names if applicable"] or []
       }
    
    CRITICAL: Always set needs_labs to true or false based on clinical assessment.
    Be thorough but concise. Always complete all steps.
    """,
    tools=[
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
