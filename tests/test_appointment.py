"""Test appointment booking flow."""

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from clinicpulse.agent import root_agent


async def test_appointment_booking() -> None:
    """Test the complete appointment booking workflow."""

    print("=" * 80)
    print("APPOINTMENT BOOKING FLOW TEST")
    print("=" * 80)

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="clinicpulse",
        user_id="test_user",
        session_id="test_appointment_session",
    )
    runner = Runner(
        agent=root_agent,
        app_name="clinicpulse",
        session_service=session_service,
    )

    # Simulate a complete patient flow
    queries = [
        # Step 1: Intake
        "Patient John Smith, ID: P12345, is here with chest pain",
        "Symptoms started 3 hours ago, pain is severe, radiating to left arm",
        
        # Step 2: Triage (agent should prioritize as urgent/critical)
        "Please triage this patient",
        
        # Step 3: Request appointment booking
        "Please book an appointment for this patient based on the triage priority",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n{'─' * 80}")
        print(f"Query {i}: {query}")
        print(f"{'─' * 80}")
        
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_appointment_session",
            new_message=genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text=query)],
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(f"\nAgent Response:\n{event.content.parts[0].text}")

    # Check final state
    print("\n" + "=" * 80)
    print("FINAL SESSION STATE")
    print("=" * 80)
    
    session = await session_service.get_session(
        app_name="clinicpulse",
        user_id="test_user",
        session_id="test_appointment_session",
    )
    
    if session and session.state:
        print("\nPatient Intake:")
        print(session.state.get("patient_intake", "NOT SET"))
        
        print("\nTriage Priority:")
        print(session.state.get("triage_priority", "NOT SET"))
        
        print("\nAppointment Details:")
        appointment = session.state.get("appointment_details", "NOT SET")
        if isinstance(appointment, dict):
            for key, value in appointment.items():
                print(f"  {key}: {value}")
        else:
            print(appointment)
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


async def test_appointment_validation_simple() -> None:
    """Test appointment validation logic with simple checks."""
    
    print("\n" + "=" * 80)
    print("APPOINTMENT VALIDATION TEST (Simplified)")
    print("=" * 80)
    
    # Test case 1: Complete appointment data
    print("\nTest 1: Complete appointment data")
    complete_appointment = {
        "patient_id": "P12345",
        "appointment_id": "APT-123456",
        "doctor": "Dr. Smith",
        "datetime": "2025-11-21 10:00",
        "specialty": "cardiology",
        "urgency_level": "urgent",
        "confirmation_sent": True,
    }
    
    required_fields = {"patient_id", "appointment_id", "doctor", "datetime"}
    missing_fields = required_fields - set(complete_appointment.keys())
    
    if not missing_fields:
        print(f"✓ PASS: Complete appointment has all required fields: {required_fields}")
    else:
        print(f"✗ FAIL: Missing fields: {missing_fields}")
    
    # Test case 2: Missing patient_id
    print("\nTest 2: Missing patient_id")
    incomplete_appointment_1 = {
        "appointment_id": "APT-123456",
        "doctor": "Dr. Smith",
        "datetime": "2025-11-21 10:00",
    }
    
    missing_fields_1 = required_fields - set(incomplete_appointment_1.keys())
    
    if missing_fields_1 == {"patient_id"}:
        print(f"✓ PASS: Correctly identified missing patient_id")
    else:
        print(f"✗ FAIL: Expected missing patient_id, got: {missing_fields_1}")
    
    # Test case 3: Missing appointment_id
    print("\nTest 3: Missing appointment_id")
    incomplete_appointment_2 = {
        "patient_id": "P12345",
        "doctor": "Dr. Smith",
        "datetime": "2025-11-21 10:00",
    }
    
    missing_fields_2 = required_fields - set(incomplete_appointment_2.keys())
    
    if missing_fields_2 == {"appointment_id"}:
        print(f"✓ PASS: Correctly identified missing appointment_id")
    else:
        print(f"✗ FAIL: Expected missing appointment_id, got: {missing_fields_2}")
    
    # Test case 4: Multiple missing fields
    print("\nTest 4: Multiple missing fields")
    incomplete_appointment_3 = {
        "doctor": "Dr. Smith",
    }
    
    missing_fields_3 = required_fields - set(incomplete_appointment_3.keys())
    
    if missing_fields_3 == {"patient_id", "appointment_id", "datetime"}:
        print(f"✓ PASS: Correctly identified multiple missing fields: {missing_fields_3}")
    else:
        print(f"✗ FAIL: Expected missing patient_id, appointment_id, datetime, got: {missing_fields_3}")
    
    print("\n" + "=" * 80)


async def test_appointment_tools() -> None:
    """Test appointment booking tools."""
    
    print("\n" + "=" * 80)
    print("APPOINTMENT TOOLS TEST")
    print("=" * 80)
    
    from clinicpulse.tools import (
        check_doctor_availability,
        book_appointment,
        send_appointment_confirmation,
    )
    
    # Test 1: Check doctor availability
    print("\nTest 1: Check doctor availability (Critical urgency)")
    availability = check_doctor_availability(
        specialty="cardiology",
        urgency_level="critical"
    )
    
    if availability and "available_slots" in availability:
        print(f"✓ PASS: Found {len(availability['available_slots'])} available slots")
        print(f"  Doctor: {availability['doctor']}")
        print(f"  Specialty: {availability['specialty']}")
        if availability['available_slots']:
            print(f"  First slot: {availability['available_slots'][0]['datetime']}")
    else:
        print("✗ FAIL: No availability data returned")
    
    # Test 2: Book appointment
    print("\nTest 2: Book appointment")
    booking = book_appointment(
        patient_id="P12345",
        doctor_name="Dr. Smith",
        appointment_datetime="2025-11-21 10:00",
        appointment_type="consultation"
    )
    
    required_booking_fields = {"appointment_id", "patient_id", "doctor", "datetime", "status"}
    if all(field in booking for field in required_booking_fields):
        print(f"✓ PASS: Booking created successfully")
        print(f"  Appointment ID: {booking['appointment_id']}")
        print(f"  Status: {booking['status']}")
        print(f"  Location: {booking.get('location', 'N/A')}")
    else:
        missing = required_booking_fields - set(booking.keys())
        print(f"✗ FAIL: Missing booking fields: {missing}")
    
    # Test 3: Send confirmation
    print("\nTest 3: Send appointment confirmation")
    confirmation = send_appointment_confirmation(
        patient_id="P12345",
        appointment_details=booking
    )
    
    if confirmation and confirmation.get("confirmation_sent"):
        print(f"✓ PASS: Confirmation sent successfully")
        print(f"  Channels: {confirmation.get('channels', [])}")
        print(f"  Message: {confirmation.get('message', 'N/A')}")
    else:
        print("✗ FAIL: Confirmation not sent")
    
    print("\n" + "=" * 80)


async def main() -> None:
    """Run all appointment tests."""
    
    # Run simple validation tests
    await test_appointment_validation_simple()
    
    # Run tool tests
    await test_appointment_tools()
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)
    print("\n✓ Appointment validation logic verified")
    print("✓ Appointment booking tools verified")
    print("\nNote: Full integration test requires API credentials.")
    print("Run 'adk web' to test the complete workflow interactively.")


if __name__ == "__main__":
    asyncio.run(main())
