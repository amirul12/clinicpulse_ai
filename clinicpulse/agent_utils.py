"""Utility helpers for ClinicPulse AI agents."""

from google.adk.agents.callback_context import CallbackContext
from google.genai import types as genai_types


def suppress_output_callback(callback_context: CallbackContext) -> genai_types.Content:
    """Placeholder callback mirroring blogger sample behavior."""

    del callback_context  # Unused placeholder parameter for now.
    return genai_types.Content()
