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
    1. Review the `triage_priority` state to understand urgency level (Critical/Urgent/Routine)
    2. Review the `patient_intake` state to determine appropriate specialty (use "general" if unclear)
    3. Call `check_doctor_availability` with specialty and urgency level to find available slots
    4. Select the earliest appropriate slot based on urgency
    5. Call `book_appointment` with patient_id, doctor name, and selected datetime
    6. Call `send_appointment_confirmation` to notify the patient
    7. Store all appointment details in the `appointment_details` state key with fields:
       - patient_id
       - appointment_id
       - doctor
       - datetime
       - specialty
       - urgency_level
       - confirmation_sent

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
