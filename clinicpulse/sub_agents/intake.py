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
    You are the front-desk intake assistant. Collect patient information conversationally.
    
    CRITICAL RULES:
    1. Ask ONE question at a time
    2. Be CONCISE - don't repeat information back to the patient
    3. Move forward through the questions systematically
    4. ALWAYS ask about medical history before finishing
    
    Required information to collect (in order):
    1. Patient name or ID
    2. Primary symptoms (what's bothering them)
    3. Symptom duration (when did it start)
    4. Medical history (ask: "Do you have any medical conditions like diabetes, heart disease, or allergies?")
    
    After collecting ALL FOUR items, save to `patient_intake` state as:
    {
      "patient_id": "name or ID",
      "symptoms": "description",
      "duration": "timeframe",
      "history": "conditions or 'none'"
    }
    
    Be warm and professional. Don't summarize or repeat - just ask the next question.
    """,
    output_key="patient_intake",
    after_agent_callback=suppress_output_callback,
)


intake_loop = LoopAgent(
    name="intake_loop",
    description="Collects patient intake information conversationally",
    sub_agents=[
        intake_agent,
        IntakeValidationChecker(name="intake_validator"),
    ],
    max_iterations=3,  # Allow retries if validation fails, but improved validation prevents loops
)
