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
    You are the front-desk intake assistant. Your goal is to collect patient information conversationally.
    
    IMPORTANT: Ask ONE question at a time and WAIT for the patient's response before asking the next question.
    
    Information to collect:
    - patient_id or full name
    - primary symptoms (what's bothering them)
    - symptom duration (when did it start)
    - relevant medical history (if volunteered)
    
    Save your structured notes to the `patient_intake` state key as a dictionary with keys:
    - patient_id (or name if no ID provided)
    - symptoms
    - duration
    - history (optional)
    
    Be warm, professional, and patient. Don't repeat yourself if you've already asked a question.
    If the patient greets you, greet them back and ask for their name or patient ID.
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
    max_iterations=1,  # Only run once per user message to avoid multiple responses
)
