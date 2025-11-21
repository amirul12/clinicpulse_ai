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
        if not dossier:
            log_event("intake_validation", "missing patient_intake state")
            yield Event(author=self.name)
            return

        required_fields = {"patient_id", "symptoms", "duration", "history"}

        if hasattr(dossier, "keys"):
            # When intake stores structured data
            if required_fields.issubset(dossier.keys()):
                log_event(
                    "intake_validation",
                    "intake dossier validated",
                    dossier.get("patient_id"),
                )
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return
        else:
            # Fall back to text inspection to avoid AttributeError on strings
            text = str(dossier).lower()
            # Check for all required information in text format
            has_symptoms = "symptom" in text or "fever" in text or "pain" in text
            has_duration = "duration" in text or "day" in text or "week" in text or "started" in text
            has_history = "history" in text or "medical" in text or "condition" in text or "diabetes" in text or "disease" in text
            
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
        if triage_decision:
            log_event(
                "triage_validation",
                "triage priority available",
                triage_decision.get("patient_id")
                if hasattr(triage_decision, "get")
                else None,
            )
            yield Event(author=self.name, actions=EventActions(escalate=True))
            return
        log_event("triage_validation", "triage pending")
        yield Event(author=self.name)


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

