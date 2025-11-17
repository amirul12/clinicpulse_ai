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

        required_fields = {"patient_id", "symptoms", "duration"}

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
            if all(field in text for field in ("symptom", "duration")):
                log_event("intake_validation", "text dossier validated")
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
