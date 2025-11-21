"""Configuration for ClinicPulse AI agents."""

import os
import warnings
from dataclasses import dataclass

import google.auth
from google.auth import exceptions as google_auth_exceptions


def _configure_environment_defaults() -> None:
    """Attempt to configure Vertex AI defaults but allow local fallback."""

    use_vertex = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "True")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", use_vertex)

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if use_vertex.lower() == "true" and project_id is None:
        try:
            _, project_id = google.auth.default()
        except google_auth_exceptions.DefaultCredentialsError:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if api_key:
                os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
            else:
                warnings.warn(
                    "ADC not found. Provide GOOGLE_CLOUD_PROJECT or set GOOGLE_GENAI_USE_VERTEXAI=FALSE "
                    "with GOOGLE_API_KEY to use AI Studio.",
                    stacklevel=2,
                )
            project_id = None

    if project_id is not None:
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)

    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")


_configure_environment_defaults()


@dataclass
class AgentConfiguration:
    """Models and knobs used across ClinicPulse AI."""

    worker_model: str = "gemini-2.5-flash"
    critic_model: str = "gemini-2.5-flash"
        # critic_model: str = "gemini-2.5-pro"
    guideline_search_iterations: int = 3


config = AgentConfiguration()
