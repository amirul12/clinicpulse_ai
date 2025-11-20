"""Appointment scheduling agent definitions."""

from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool

from ..agent_utils import suppress_output_callback
from ..config import config
from ..tools import (
    book_appointment,
    check_doctor_availability,
    send_appointment_confirmation,
)
from ..validation import AppointmentValidationChecker


appointment_scheduler = Agent(
    name="appointment_scheduler",
    model=config.worker_model,
    description="Books doctor appointments based on triage priority and patient needs.",
    instruction="""
    You are the appointment coordinator. Your job is to schedule a doctor appointment for the patient.

    Steps to follow:
    1. **Extract patient_id**: Get the patient_id from the `patient_intake` state (look for patient_id field or extract from the data)
    2. **Review urgency**: Check the `triage_priority` state to understand urgency level (Critical/Urgent/Routine)
    3. **Determine specialty**: Review the `patient_intake` state to determine appropriate specialty. Use "general" if unclear or not specified.
    4. **Check availability**: Call `check_doctor_availability` with specialty and urgency level to find available slots
    5. **Select slot**: Choose the earliest appropriate slot based on urgency level
    6. **Book appointment**: Call `book_appointment` with:
       - patient_id (from step 1)
       - doctor_name (from available slots)
       - appointment_datetime (selected slot datetime)
       - appointment_type (default: "consultation")
    7. **Send confirmation**: Call `send_appointment_confirmation` with:
       - patient_id
       - appointment_details (the dict returned from book_appointment)
    8. **Store complete details**: Ensure the `appointment_details` state key contains ALL fields:
       - patient_id (string)
       - appointment_id (string, from book_appointment response)
       - doctor (string, doctor name)
       - datetime (string, appointment datetime)
       - specialty (string, medical specialty)
       - urgency_level (string, from triage_priority)
       - confirmation_sent (boolean, True after sending confirmation)

    IMPORTANT:
    - Always extract patient_id from patient_intake state first
    - If patient_id is missing, set it to "UNKNOWN" and log a warning
    - Ensure all required fields are present in the final appointment_details output
    - The appointment_details must be a structured dictionary, not a text summary

    Be professional and ensure all booking details are accurate.
    """,
    tools=[
        FunctionTool(check_doctor_availability),
        FunctionTool(book_appointment),
        FunctionTool(send_appointment_confirmation),
    ],
    output_key="appointment_details",
    after_agent_callback=suppress_output_callback,
)


appointment_loop = LoopAgent(
    name="appointment_loop",
    description="Retries appointment booking if validation fails",
    sub_agents=[
        appointment_scheduler,
        AppointmentValidationChecker(name="appointment_validator"),
    ],
    max_iterations=3,
)
