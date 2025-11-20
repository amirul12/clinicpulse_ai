"""Custom tool implementations for ClinicPulse AI."""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .logging_utils import log_event


def fetch_patient_records(patient_id: str) -> Dict[str, str]:
    """Mock EHR lookup returning synthetic vitals and history."""

    random.seed(hash(patient_id) % 2**32)
    log_event("fetch_patient_records", "retrieving mock EHR snapshot", patient_id)
    return {
        "patient_id": patient_id,
        "last_visit": "2024-11-12",
        "known_conditions": random.choice([
            "hypertension",
            "type 2 diabetes",
            "asthma",
            "no chronic conditions recorded",
        ]),
        "recent_vitals": {
            "bp": f"{random.randint(110, 150)}/{random.randint(70, 95)}",
            "hr": random.randint(60, 110),
            "temp_c": round(random.uniform(36.5, 38.5), 1),
        },
    }


def record_triage_decision(patient_id: str, priority_level: str) -> Dict[str, str]:
    """Store triage outcomes (mock implementation)."""

    timestamp = time.time()
    log_event(
        "record_triage_decision",
        f"priority={priority_level}",
        patient_id,
    )
    # In a full build this would persist to a database or emit telemetry.
    return {
        "patient_id": patient_id,
        "priority_level": priority_level,
        "recorded_at": timestamp,
        "status": "logged",
    }


def wait_for_lab_results(patient_id: str) -> Dict[str, str]:
    """Simulate a long-running lab wait that motivates pause/resume flows."""

    log_event("wait_for_lab_results", "initiated lab wait", patient_id)
    return {"status": "pending", "message": "Awaiting lab uploads"}


# ==================== APPOINTMENT SCHEDULING TOOLS ====================


def check_doctor_availability(
    specialty: str, urgency_level: str
) -> Dict[str, any]:
    """Check available doctors and their appointment slots (mock implementation).
    
    Args:
        specialty: Medical specialty (e.g., 'cardiology', 'general')
        urgency_level: Patient urgency ('critical', 'urgent', 'routine')
    
    Returns:
        Dictionary with available_slots, doctor, and specialty
    """

    log_event("check_doctor_availability", f"specialty={specialty}, urgency={urgency_level}")

    # Mock doctor database
    doctors = {
        "general": ["Dr. Smith", "Dr. Johnson", "Dr. Williams"],
        "cardiology": ["Dr. Heart", "Dr. Cardio"],
        "pediatrics": ["Dr. Kids", "Dr. Child"],
        "orthopedics": ["Dr. Bones", "Dr. Joint"],
        "dermatology": ["Dr. Skin", "Dr. Derm"],
    }

    available_doctors = doctors.get(specialty.lower(), doctors["general"])

    # Generate mock available slots based on urgency
    base_date = datetime.now()
    if urgency_level.lower() == "critical":
        # Same day or next day
        slot_dates = [base_date + timedelta(hours=i*2) for i in range(1, 4)]
    elif urgency_level.lower() == "urgent":
        # Within 1-3 days
        slot_dates = [base_date + timedelta(days=i) for i in range(1, 4)]
    else:
        # Routine: 1-2 weeks
        slot_dates = [base_date + timedelta(days=i) for i in range(7, 15, 2)]

    # Pick a random doctor
    selected_doctor = random.choice(available_doctors)

    available_slots = [
        {
            "datetime": slot.strftime("%Y-%m-%d %H:%M"),
            "doctor": selected_doctor,
            "specialty": specialty,
            "duration_minutes": 30,
        }
        for slot in slot_dates
    ]

    log_event(
        "check_doctor_availability",
        f"found {len(available_slots)} slots for {selected_doctor}",
    )

    return {
        "available_slots": available_slots,
        "doctor": selected_doctor,
        "specialty": specialty,
    }


def book_appointment(
    patient_id: str,
    doctor_name: str,
    appointment_datetime: str,
    appointment_type: str = "consultation",
) -> Dict[str, str]:
    """Book an appointment for a patient (mock implementation)."""

    timestamp = time.time()
    appointment_id = f"APT-{int(timestamp)}-{hash(patient_id) % 10000}"

    log_event(
        "book_appointment",
        f"doctor={doctor_name}, datetime={appointment_datetime}, type={appointment_type}",
        patient_id,
    )

    return {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "doctor": doctor_name,
        "datetime": appointment_datetime,
        "type": appointment_type,
        "status": "confirmed",
        "booked_at": timestamp,
        "location": "Clinic Building A, Room 201",
        "instructions": "Please arrive 15 minutes early for check-in",
    }


def send_appointment_confirmation(
    patient_id: str, appointment_details: Dict[str, str]
) -> Dict[str, str]:
    """Send appointment confirmation to patient (mock implementation)."""

    log_event(
        "send_appointment_confirmation",
        f"sending confirmation for {appointment_details.get('appointment_id')}",
        patient_id,
    )

    return {
        "patient_id": patient_id,
        "confirmation_sent": True,
        "channels": ["email", "sms"],
        "message": f"Appointment confirmed with {appointment_details.get('doctor')} on {appointment_details.get('datetime')}",
        "sent_at": time.time(),
    }
