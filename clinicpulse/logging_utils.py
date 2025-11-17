"""Logging utilities for ClinicPulse AI."""

import logging
import os
from typing import Optional

LOGGER_NAME = "clinicpulse"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        level = os.environ.get("CLINICPULSE_LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, level, logging.INFO))
    return logger


def log_event(step: str, message: str, patient_id: Optional[str] = None) -> None:
    logger = get_logger()
    prefix = f"patient={patient_id} " if patient_id else ""
    logger.info("%sSTEP=%s %s", prefix, step.upper(), message)
