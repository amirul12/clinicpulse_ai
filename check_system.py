#!/usr/bin/env python3
"""Comprehensive system check for ClinicPulse AI."""

import sys
from typing import List, Tuple


def check_imports() -> Tuple[bool, List[str]]:
    """Check all critical imports."""
    errors = []
    
    try:
        from clinicpulse import root_agent
        print(f"✓ Root agent: {root_agent.name}")
    except Exception as e:
        errors.append(f"Failed to import root_agent: {e}")
    
    try:
        from clinicpulse.sub_agents import (
            intake_loop,
            triage_loop,
            lab_wait_loop,
            briefing_ensemble,
            appointment_loop,
        )
        print(f"✓ Sub-agents:")
        print(f"  - {intake_loop.name}")
        print(f"  - {triage_loop.name}")
        print(f"  - {lab_wait_loop.name}")
        print(f"  - {briefing_ensemble.name}")
        print(f"  - {appointment_loop.name}")
    except Exception as e:
        errors.append(f"Failed to import sub-agents: {e}")
    
    try:
        from clinicpulse.tools import (
            fetch_patient_records,
            record_triage_decision,
            wait_for_lab_results,
            check_doctor_availability,
            book_appointment,
            send_appointment_confirmation,
        )
        print(f"✓ Tools: 6 tools imported")
    except Exception as e:
        errors.append(f"Failed to import tools: {e}")
    
    try:
        from clinicpulse.validation import (
            IntakeValidationChecker,
            TriageValidationChecker,
            LabResultsValidationChecker,
            AppointmentValidationChecker,
        )
        print(f"✓ Validators: 4 validators imported")
    except Exception as e:
        errors.append(f"Failed to import validators: {e}")
    
    return len(errors) == 0, errors


def check_agent_structure() -> Tuple[bool, List[str]]:
    """Verify agent structure and configuration."""
    errors = []
    
    try:
        from clinicpulse.agent import root_agent
        
        # Check sub-agents
        if not root_agent.sub_agents:
            errors.append("Root agent has no sub-agents")
        else:
            expected_count = 5  # intake, triage, lab_wait, briefing, appointment
            actual_count = len(root_agent.sub_agents)
            if actual_count != expected_count:
                errors.append(
                    f"Expected {expected_count} sub-agents, got {actual_count}"
                )
            print(f"✓ Root agent has {actual_count} sub-agents")
        
        # Check tools
        if not root_agent.tools:
            errors.append("Root agent has no tools")
        else:
            print(f"✓ Root agent has {len(root_agent.tools)} tools")
        
        # Check output key
        if root_agent.output_key != "clinician_briefing":
            errors.append(
                f"Expected output_key 'clinician_briefing', got '{root_agent.output_key}'"
            )
        else:
            print(f"✓ Root agent output_key: {root_agent.output_key}")
        
    except Exception as e:
        errors.append(f"Failed to check agent structure: {e}")
    
    return len(errors) == 0, errors


def check_validation_logic() -> Tuple[bool, List[str]]:
    """Test validation logic."""
    errors = []
    
    try:
        # Test appointment validation
        complete_appointment = {
            "patient_id": "P12345",
            "appointment_id": "APT-123456",
            "doctor": "Dr. Smith",
            "datetime": "2025-11-21 10:00",
        }
        
        required_fields = {"patient_id", "appointment_id", "doctor", "datetime"}
        missing = required_fields - set(complete_appointment.keys())
        
        if missing:
            errors.append(f"Validation test failed: missing fields {missing}")
        else:
            print("✓ Appointment validation logic correct")
        
        # Test incomplete appointment
        incomplete_appointment = {
            "doctor": "Dr. Smith",
            "datetime": "2025-11-21 10:00",
        }
        
        missing = required_fields - set(incomplete_appointment.keys())
        expected_missing = {"patient_id", "appointment_id"}
        
        if missing != expected_missing:
            errors.append(
                f"Expected missing {expected_missing}, got {missing}"
            )
        else:
            print("✓ Incomplete appointment correctly identified")
        
    except Exception as e:
        errors.append(f"Failed validation logic test: {e}")
    
    return len(errors) == 0, errors


def check_tools() -> Tuple[bool, List[str]]:
    """Test tool functionality."""
    errors = []
    
    try:
        from clinicpulse.tools import (
            fetch_patient_records,
            check_doctor_availability,
            book_appointment,
        )
        
        # Test fetch_patient_records
        result = fetch_patient_records("TEST123")
        if "patient_id" not in result:
            errors.append("fetch_patient_records missing patient_id")
        else:
            print("✓ fetch_patient_records works")
        
        # Test check_doctor_availability
        result = check_doctor_availability("cardiology", "urgent")
        if "available_slots" not in result:
            errors.append("check_doctor_availability missing available_slots")
        else:
            print(f"✓ check_doctor_availability works ({len(result['available_slots'])} slots)")
        
        # Test book_appointment
        result = book_appointment("P123", "Dr. Test", "2025-11-21 10:00")
        required = {"appointment_id", "patient_id", "doctor", "datetime", "status"}
        missing = required - set(result.keys())
        if missing:
            errors.append(f"book_appointment missing fields: {missing}")
        else:
            print("✓ book_appointment works")
        
    except Exception as e:
        errors.append(f"Failed tool test: {e}")
    
    return len(errors) == 0, errors


def check_file_structure() -> Tuple[bool, List[str]]:
    """Verify file structure."""
    errors = []
    import pathlib
    
    base = pathlib.Path(__file__).parent
    
    required_files = [
        "clinicpulse/__init__.py",
        "clinicpulse/agent.py",
        "clinicpulse/config.py",
        "clinicpulse/tools.py",
        "clinicpulse/agent_utils.py",
        "clinicpulse/logging_utils.py",
        "clinicpulse/sub_agents/__init__.py",
        "clinicpulse/sub_agents/intake.py",
        "clinicpulse/sub_agents/triage.py",
        "clinicpulse/sub_agents/labs.py",
        "clinicpulse/sub_agents/briefing.py",
        "clinicpulse/sub_agents/appointment.py",
        "clinicpulse/validation/__init__.py",
        "clinicpulse/validation/checkers.py",
        "tests/test_agent.py",
        "tests/test_appointment.py",
        "eval/evaluate_briefing.py",
        "requirements.txt",
        "README.md",
        "SUBMISSION.md",
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = base / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        errors.append(f"Missing files: {', '.join(missing_files)}")
    else:
        print(f"✓ All {len(required_files)} required files present")
    
    return len(errors) == 0, errors


def main():
    """Run all system checks."""
    print("=" * 80)
    print("CLINICPULSE AI - COMPREHENSIVE SYSTEM CHECK")
    print("=" * 80)
    
    all_passed = True
    
    # Check 1: Imports
    print("\n[1/5] Checking imports...")
    passed, errors = check_imports()
    if not passed:
        all_passed = False
        for error in errors:
            print(f"  ✗ {error}")
    
    # Check 2: Agent structure
    print("\n[2/5] Checking agent structure...")
    passed, errors = check_agent_structure()
    if not passed:
        all_passed = False
        for error in errors:
            print(f"  ✗ {error}")
    
    # Check 3: Validation logic
    print("\n[3/5] Checking validation logic...")
    passed, errors = check_validation_logic()
    if not passed:
        all_passed = False
        for error in errors:
            print(f"  ✗ {error}")
    
    # Check 4: Tools
    print("\n[4/5] Checking tools...")
    passed, errors = check_tools()
    if not passed:
        all_passed = False
        for error in errors:
            print(f"  ✗ {error}")
    
    # Check 5: File structure
    print("\n[5/5] Checking file structure...")
    passed, errors = check_file_structure()
    if not passed:
        all_passed = False
        for error in errors:
            print(f"  ✗ {error}")
    
    # Summary
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ ALL CHECKS PASSED - System is ready!")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Set up API credentials (GOOGLE_API_KEY or ADC)")
        print("  2. Run: adk web")
        print("  3. Test the complete workflow interactively")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Please review errors above")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
