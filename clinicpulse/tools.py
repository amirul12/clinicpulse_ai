"""Custom tool implementations for ClinicPulse AI."""

import random
import time
from typing import Dict

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
