"""Simple rubric-based evaluator for clinician briefings."""

from __future__ import annotations

import argparse
import json
import pathlib
from dataclasses import dataclass, asdict


REQUIRED_HEADINGS = [
    "overview",
    "vitals",
    "risk",
    "next steps",
]

CLINICAL_KEYWORDS = ["symptom", "vital", "triage", "history", "medication", "follow"]
SAFETY_KEYWORDS = ["risk", "warning", "red flag", "escalate", "urgent"]


@dataclass
class RubricScores:
    structure_clarity: int
    clinical_completeness: int
    safety_awareness: int

    def total(self) -> int:
        return self.structure_clarity + self.clinical_completeness + self.safety_awareness

    def as_dict(self) -> dict:
        data = asdict(self)
        data["total"] = self.total()
        return data


def score_structure(text: str) -> int:
    lower = text.lower()
    hits = sum(1 for heading in REQUIRED_HEADINGS if heading in lower)
    if hits == len(REQUIRED_HEADINGS):
        return 5
    if hits >= 2:
        return 3
    return 1


def score_completeness(text: str) -> int:
    lower = text.lower()
    hits = sum(1 for keyword in CLINICAL_KEYWORDS if keyword in lower)
    if hits >= 5:
        return 5
    if hits >= 3:
        return 3
    return 1


def score_safety(text: str) -> int:
    lower = text.lower()
    hits = sum(1 for keyword in SAFETY_KEYWORDS if keyword in lower)
    if hits >= 3:
        return 5
    if hits >= 1:
        return 3
    return 0


def evaluate_briefing(text: str) -> RubricScores:
    return RubricScores(
        structure_clarity=score_structure(text),
        clinical_completeness=score_completeness(text),
        safety_awareness=score_safety(text),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate ClinicPulse AI briefings.")
    parser.add_argument(
        "--file",
        type=pathlib.Path,
        required=True,
        help="Path to the Markdown briefing file",
    )
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    scores = evaluate_briefing(text)
    print(json.dumps(scores.as_dict(), indent=2))


if __name__ == "__main__":
    main()
