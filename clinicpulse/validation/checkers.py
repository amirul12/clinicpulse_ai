"""Validation agents for ClinicPulse AI."""

from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions

from ..logging_utils import log_event


class IntakeValidationChecker(BaseAgent):
    """Confirms intake packet is complete before escalation."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        dossier = context.session.state.get("patient_intake")
        
        # If no data exists yet, DON'T escalate - wait for next user message
        # This prevents the loop from re-running the agent multiple times
        if not dossier:
            log_event("intake_validation", "no patient_intake data yet - waiting for user input")
            yield Event(author=self.name)  # NO escalate - just wait
            return

        required_fields = {"patient_id", "symptoms", "duration", "history"}

        if hasattr(dossier, "keys"):
            # When intake stores structured data
            # ONLY escalate when ALL required fields are present
            if required_fields.issubset(dossier.keys()):
                log_event(
                    "intake_validation",
                    "intake dossier validated - all fields present",
                    dossier.get("patient_id"),
                )
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return
            else:
                # Data exists but incomplete - log missing fields
                missing = required_fields - set(dossier.keys())
                log_event("intake_validation", f"incomplete data - missing: {missing}")
                yield Event(author=self.name)  # NO escalate - retry
                return
        else:
            # Fall back to text inspection to avoid AttributeError on strings
            text = str(dossier).lower()
            
            # Check for all required information in text format
            # Symptoms: look for common symptom words or pain/discomfort indicators
            has_symptoms = any(word in text for word in [
                "symptom", "pain", "ache", "fever", "cough", "nausea", "dizzy",
                "headache", "chest", "stomach", "throat", "ear", "breathing",
                "swelling", "rash", "bleeding", "fatigue", "weakness"
            ])
            
            # Duration: look for time indicators
            has_duration = any(word in text for word in [
                "duration", "day", "days", "week", "weeks", "month", "months",
                "hour", "hours", "minute", "minutes", "started", "began",
                "ago", "since", "yesterday", "today", "recent"
            ])
            
            # History: look for medical conditions OR explicit "none"/"no"
            has_history = any(word in text for word in [
                "history", "medical", "condition", "diabetes", "disease",
                "hypertension", "blood pressure", "asthma", "allergy", "allergic",
                "heart", "kidney", "liver", "cancer", "arthritis", "chronic",
                "medication", "none", "no condition", "no medical", "healthy"
            ])
            
            if has_symptoms and has_duration and has_history:
                log_event("intake_validation", "text dossier validated with history")
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return

        log_event("intake_validation", "validation failed, retrying")
        yield Event(author=self.name)


class TriageValidationChecker(BaseAgent):
    """Ensures triage prioritization exists before advancing."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        triage_decision = context.session.state.get("triage_priority")
        if not triage_decision:
            log_event("triage_validation", "triage pending")
            yield Event(author=self.name)
            return
            
        patient_id = (
            triage_decision.get("patient_id")
            if hasattr(triage_decision, "get")
            else None
        )
        
        # Check if needs_labs field is present (recommended but not required for backward compatibility)
        if hasattr(triage_decision, "get"):
            needs_labs = triage_decision.get("needs_labs")
            if needs_labs is not None:
                log_event(
                    "triage_validation",
                    f"triage priority available with lab decision: needs_labs={needs_labs}",
                    patient_id,
                )
            else:
                log_event(
                    "triage_validation",
                    "triage priority available (needs_labs field missing - defaulting to false)",
                    patient_id,
                )
        else:
            log_event(
                "triage_validation",
                "triage priority available",
                patient_id,
            )
        
        yield Event(author=self.name, actions=EventActions(escalate=True))



class LabResultsValidationChecker(BaseAgent):
    """Checks if lab_results state key is populated to resume flow."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        lab_results = context.session.state.get("lab_results")
        if lab_results:
            log_event(
                "lab_validation",
                "lab results available",
                lab_results.get("patient_id")
                if hasattr(lab_results, "get")
                else None,
            )
            yield Event(author=self.name, actions=EventActions(escalate=True))
            return
        log_event("lab_validation", "awaiting lab input")
        yield Event(author=self.name)


class AppointmentValidationChecker(BaseAgent):
    """Validates that appointment booking is complete."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        appointment = context.session.state.get("appointment_details")
        if not appointment:
            log_event("appointment_validation", "missing appointment_details state")
            yield Event(author=self.name)
            return

        # Required fields for a complete appointment
        required_fields = {"patient_id", "appointment_id", "doctor", "datetime"}

        if hasattr(appointment, "keys"):
            # When appointment stores structured data
            missing_fields = required_fields - set(appointment.keys())
            if not missing_fields:
                log_event(
                    "appointment_validation",
                    f"appointment validated: {appointment.get('appointment_id')}",
                    appointment.get("patient_id"),
                )
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return
            else:
                log_event(
                    "appointment_validation",
                    f"missing required fields: {missing_fields}",
                    appointment.get("patient_id"),
                )
        else:
            # Fall back to text inspection
            text = str(appointment).lower()
            if all(field in text for field in ("appointment", "doctor", "datetime", "patient")):
                log_event("appointment_validation", "text appointment validated")
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return

        log_event("appointment_validation", "validation failed, retrying")
        yield Event(author=self.name)

