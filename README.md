## ClinicPulse AI

ClinicPulse AI is a smart clinic flow manager that coordinates patient intake, triage, and clinician briefing using a multi-agent architecture powered by Google's Agent Development Kit (ADK). The goal is to reduce bottlenecks in outpatient clinics by giving every care team member up-to-date context before a consultation begins.

### Problem

Smaller clinics still rely on manual questioning, paper forms, and ad-hoc note taking. As a result:

- Patients repeat the same information multiple times.
- Staff lose precious minutes clarifying missing details.
- Clinicians only see partial context when they enter the exam room.

### Solution

ClinicPulse AI orchestrates a three-stage pipeline:

1. **Intake Agent** – Collects demographics, chief complaints, and symptom duration. Uses a loop validator to ensure all mandatory fields are captured before handing off.
2. **Triage Agent** – Prioritizes queues using guideline lookups (Google Search tool) and custom EHR tools to pull vitals/lab history.
3. **Clinician Briefing Agent** – Generates a concise patient dossier with recommended next steps, outstanding orders, and suggested follow-up questions.

Session memory keeps a shared patient dossier so every agent reads/writes from the same state. Observability hooks emit structured logs (think: patient_id, step, result) for compliance audits.

### Planned Capstone Features

- **Multi-agent system**: Sequential pipeline with loop agents for intake and triage validation.
- **Tools**: Combination of built-in Google Search, custom EHR lookup tool (mocked), and a code execution tool for quick vital-score computations.
- **Sessions & Memory**: `InMemorySessionService` plus a simple embedded “Patient Memory Bank” file to simulate persistence across pauses.
- **Observability**: Logging/tracing for agent handoffs; metrics for average loop retries.
- **Long-running operations**: Ability to pause when waiting for lab uploads and resume once data is available.
- **Agent evaluation**: Automated script that grades briefing quality using a rubric (clarity, completeness, safety flags).
- **Deployment readiness**: Instructions for running via `adk web` locally; optional Agent Engine/Cloud Run deployment notes for bonus points.

### Architecture Snapshot

```
User → Intake Orchestrator (LoopAgent)
      → Triage Coordinator (LoopAgent with Google Search + EHR Tool)
      → Clinician Briefing Ensemble (parallel sub-agents: History Synthesizer, Lab Reviewer, Risk Checker)
      → Output dossier + optional notifications
```

Shared state is managed through ADK session services. Tools expose the following interfaces:

- `fetch_patient_records(patient_id)` – mocked EHR dataset.
- `record_triage_decision(patient_id, priority_level)` – logs decision to state + external sink.
- `wait_for_lab_results(patient_id)` – demonstrates long-running operations by pausing/resuming agents.

### Repository Layout (initial draft)

```
clinicpulse_ai/
├── README.md
├── requirements.txt
├── clinicpulse/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── tools.py
│   ├── agent_utils.py
│   ├── validation/
│   │   ├── __init__.py
│   │   └── checkers.py
│   └── sub_agents/
│       ├── __init__.py
│       ├── intake.py
│       ├── triage.py
│       └── briefing.py
├── tests/
│   ├── README.md
│   └── test_agent.py
└── diagrams/
    └── architecture.png (placeholder)
```

Upcoming tasks:

- [x] Populate `requirements.txt` with ADK + testing deps.
- [x] Implement config + tool stubs.
- [x] Build sub-agent logic and validation loops.
- [x] Add evaluation harness + documentation updates.

## Getting Started

### Requirements

- Python 3.11+
- Access to Google ADK-compatible credentials (Vertex AI or AI Studio API key)

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env` and populate the appropriate credentials:

```bash
cp .env .env.local  # optional
```

Set `GOOGLE_GENAI_USE_VERTEXAI=True` with ADC or switch to AI Studio using `GOOGLE_API_KEY`.

### Running the Agent Locally

1. Configure credentials as above.
2. Launch ADK web runner from the project root:

```bash
adk web
```

3. Interact with ClinicPulse AI through the UI or via the integration harness:

```bash
python -m tests.test_agent
```

### Evaluation Harness

After generating a clinician briefing, point the rubric script at the Markdown file:

```bash
python -m eval.evaluate_briefing --file path/to/briefing.md
```

The script outputs a JSON summary with structure, completeness, safety scores, and a total. Use it to gate submissions before sharing with clinicians.

This README will grow with installation instructions, diagrams, and scoring notes once implementation progresses.
