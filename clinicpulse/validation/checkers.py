"""Validation agents for ClinicPulse AI."""

from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions


class IntakeValidationChecker(BaseAgent):
    """Confirms intake packet is complete before escalation."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        dossier = context.session.state.get("patient_intake")
        if not dossier:
            yield Event(author=self.name)
            return

        required_fields = {"patient_id", "symptoms", "duration"}

        if hasattr(dossier, "keys"):
            # When intake stores structured data
            if required_fields.issubset(dossier.keys()):
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return
        else:
            # Fall back to text inspection to avoid AttributeError on strings
            text = str(dossier).lower()
            if all(field in text for field in ("symptom", "duration")):
                yield Event(author=self.name, actions=EventActions(escalate=True))
                return

        yield Event(author=self.name)


class TriageValidationChecker(BaseAgent):
    """Ensures triage prioritization exists before advancing."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        triage_decision = context.session.state.get("triage_priority")
        if triage_decision:
            yield Event(author=self.name, actions=EventActions(escalate=True))
            return
        yield Event(author=self.name)
