# ClinicPulse AI - Manual Testing Guide

**Version:** 1.0  
**Date:** 2025-11-23  
**Purpose:** Comprehensive test scenarios for manual QA testing

---

## Setup

Before testing, ensure:
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Set API credentials
export GOOGLE_API_KEY="your-api-key-here"
export GOOGLE_GENAI_USE_VERTEXAI=FALSE

# 3. Start the web interface
adk web
```

---

## Test Scenario 1: Critical Emergency Case

**Patient Profile:** Chest pain (life-threatening)

### Test Questions (Answer in order):

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Sarah Johnson"** or **"P12345"** |
| 2 | "What symptoms are you experiencing?" | **"Severe chest pain radiating to my left arm"** |
| 3 | "When did the chest pain start?" | **"About 30 minutes ago"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"I have high blood pressure and diabetes"** |

### Expected Results:

✅ **Intake Complete** - All 4 fields collected  
✅ **Triage Priority:** **CRITICAL**  
✅ **Appointment:** Same-day or next available (urgent slot)  
✅ **Briefing:** Should mention:
- Chest pain as chief complaint
- Critical priority with rationale
- Immediate ECG and cardiac enzyme recommendations
- Appointment details with cardiologist

---

## Test Scenario 2: Urgent Care Case

**Patient Profile:** High fever with infection symptoms

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Michael Chen"** |
| 2 | "What symptoms are you experiencing?" | **"High fever of 103°F, severe headache, and body aches"** |
| 3 | "When did these symptoms start?" | **"2 days ago"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"No chronic conditions, but allergic to penicillin"** |

### Expected Results:

✅ **Intake Complete**  
✅ **Triage Priority:** **URGENT**  
✅ **Appointment:** Within 1-3 days  
✅ **Briefing:** Should mention:
- Fever and infection symptoms
- Urgent priority
- Penicillin allergy flagged
- Appointment with general practitioner

---

## Test Scenario 3: Routine Follow-up

**Patient Profile:** Minor symptoms, routine care

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Emily Rodriguez"** |
| 2 | "What symptoms are you experiencing?" | **"Mild knee pain when walking"** |
| 3 | "When did the knee pain start?" | **"About 2 weeks ago"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"None"** |

### Expected Results:

✅ **Intake Complete**  
✅ **Triage Priority:** **ROUTINE**  
✅ **Appointment:** 1-2 weeks out  
✅ **Briefing:** Should mention:
- Knee pain as chief complaint
- Routine priority
- Possible orthopedic referral
- Standard appointment timing

---

## Test Scenario 4: Patient with Complex Medical History

**Patient Profile:** Multiple chronic conditions

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Robert Thompson"** |
| 2 | "What symptoms are you experiencing?" | **"Shortness of breath and fatigue"** |
| 3 | "When did these symptoms start?" | **"Started gradually over the past week"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"Type 2 diabetes, heart disease, hypertension, and asthma"** |

### Expected Results:

✅ **Intake Complete**  
✅ **Triage Priority:** **URGENT** or **CRITICAL** (due to cardiac history + SOB)  
✅ **Appointment:** Prompt scheduling  
✅ **Briefing:** Should mention:
- All chronic conditions listed
- Risk assessment based on history
- Cardiology or pulmonology referral
- Comprehensive care plan

---

## Test Scenario 5: Pediatric Case

**Patient Profile:** Child with fever

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Emma Wilson (parent: Lisa Wilson)"** |
| 2 | "What symptoms are you experiencing?" | **"My 5-year-old daughter has a fever and ear pain"** |
| 3 | "When did these symptoms start?" | **"Yesterday evening"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"No known allergies or conditions"** |

### Expected Results:

✅ **Intake Complete**  
✅ **Triage Priority:** **URGENT** (pediatric fever)  
✅ **Appointment:** Same-day or next-day  
✅ **Briefing:** Should mention:
- Pediatric patient
- Ear infection suspected
- Pediatrician appointment
- Age-appropriate care notes

---

## Test Scenario 6: Minimal Information Test

**Patient Profile:** Testing validation with incomplete data

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"John"** (first name only) |
| 2 | "What symptoms are you experiencing?" | **"Headache"** (minimal detail) |
| 3 | "When did the headache start?" | **"Today"** (vague) |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"No"** |

### Expected Results:

✅ **Intake Complete** (should accept minimal but valid data)  
✅ **Triage Priority:** **ROUTINE** (non-specific symptoms)  
✅ **Appointment:** Standard scheduling  
✅ **Briefing:** Should work with limited information

---

## Test Scenario 7: Interruption and Correction

**Patient Profile:** Testing conversation flow with corrections

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Wait, let me check... It's P67890"** |
| 2 | "What symptoms are you experiencing?" | **"I have a cough. Actually, it's a cough with blood"** |
| 3 | "When did this start?" | **"I think 3 days ago, no wait, 5 days ago"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"Smoker for 20 years, no other conditions"** |

### Expected Results:

✅ **Intake Complete** (handles corrections gracefully)  
✅ **Triage Priority:** **URGENT** or **CRITICAL** (hemoptysis is serious)  
✅ **Appointment:** Urgent scheduling  
✅ **Briefing:** Should capture:
- Cough with blood (hemoptysis)
- Smoking history
- Urgent pulmonology referral

---

## Test Scenario 8: Allergy Emergency

**Patient Profile:** Severe allergic reaction

### Test Questions:

| Step | Agent Question | Your Answer |
|------|---------------|-------------|
| 1 | "Could I please get your name or patient ID?" | **"Alex Martinez"** |
| 2 | "What symptoms are you experiencing?" | **"Severe facial swelling, difficulty breathing, hives all over body"** |
| 3 | "When did these symptoms start?" | **"Just now, about 10 minutes ago after eating peanuts"** |
| 4 | "Do you have any medical conditions like diabetes, heart disease, or allergies?" | **"Known peanut allergy, carry EpiPen"** |

### Expected Results:

✅ **Intake Complete**  
✅ **Triage Priority:** **CRITICAL** (anaphylaxis)  
✅ **Appointment:** IMMEDIATE/Emergency  
✅ **Briefing:** Should mention:
- Anaphylaxis symptoms
- Critical priority
- Emergency intervention needed
- EpiPen administration

---

## Validation Checklist

After each test scenario, verify:

### ✅ Intake Phase
- [ ] Agent asks all 4 questions (name, symptoms, duration, history)
- [ ] Agent asks ONE question at a time
- [ ] Agent doesn't repeat questions
- [ ] Agent accepts answers and moves forward
- [ ] No multiple responses to single user message

### ✅ Triage Phase (Automatic)
- [ ] Triage runs automatically after intake
- [ ] Priority level is appropriate (Critical/Urgent/Routine)
- [ ] Rationale is provided
- [ ] No user prompt needed to trigger triage

### ✅ Appointment Phase (Automatic)
- [ ] Appointment booking runs automatically after triage
- [ ] Appointment time matches urgency level:
  - Critical: Same day or next available
  - Urgent: Within 1-3 days
  - Routine: 1-2 weeks
- [ ] Doctor specialty matches symptoms
- [ ] Confirmation is sent
- [ ] No user prompt needed to trigger appointment

### ✅ Briefing Phase (Automatic)
- [ ] Briefing generates automatically after appointment
- [ ] Contains all sections: Overview, Vitals/History, Risk, Next Steps
- [ ] Includes patient information
- [ ] Includes triage assessment
- [ ] Includes appointment details
- [ ] Provides clinical recommendations
- [ ] No user prompt needed to trigger briefing

### ✅ Overall Workflow
- [ ] Complete pipeline runs: Intake → Triage → Appointment → Briefing
- [ ] Status updates provided at each stage
- [ ] No errors or exceptions
- [ ] Reasonable response time (< 30 seconds for full workflow)
- [ ] Professional and clear communication

---

## Edge Cases to Test

### Edge Case 1: Empty/Invalid Responses
```
Q: "Could I please get your name?"
A: "" (empty)
Expected: Agent should re-ask or prompt for valid input
```

### Edge Case 2: Very Long Medical History
```
Q: "Do you have any medical conditions?"
A: "Diabetes, hypertension, heart disease, asthma, arthritis, COPD, kidney disease, depression, anxiety, high cholesterol, sleep apnea"
Expected: Agent should handle long input gracefully
```

### Edge Case 3: Ambiguous Symptoms
```
Q: "What symptoms are you experiencing?"
A: "I don't feel well"
Expected: Agent should ask for more specific information
```

### Edge Case 4: Multiple Symptoms
```
Q: "What symptoms are you experiencing?"
A: "Fever, cough, headache, body aches, sore throat, and fatigue"
Expected: Agent should capture all symptoms
```

---

## Performance Benchmarks

| Metric | Target | Notes |
|--------|--------|-------|
| Intake completion time | < 2 minutes | User interaction time |
| Triage processing | < 10 seconds | Automatic |
| Appointment booking | < 10 seconds | Automatic |
| Briefing generation | < 15 seconds | Automatic |
| **Total workflow** | **< 3 minutes** | Including user interaction |
| Response latency | < 3 seconds | Per agent response |

---

## Common Issues to Watch For

### ❌ Issue 1: Multiple Responses
**Problem:** Agent responds 2-3 times to one user message  
**Expected:** ONE response per user message  
**Fixed:** max_iterations=3 with proper validation

### ❌ Issue 2: Workflow Stops After Triage
**Problem:** Agent waits for user input after triage  
**Expected:** Automatic progression to appointment  
**Fixed:** AUTOMATICALLY keywords in instructions

### ❌ Issue 3: Missing Fields in Output
**Problem:** Briefing missing appointment details  
**Expected:** All sections present  
**Check:** Validation logic in checkers.py

### ❌ Issue 4: Type Annotation Errors
**Problem:** ADK parsing errors for function signatures  
**Expected:** Clean function declarations  
**Fixed:** Removed complex type annotations

---

## Reporting Issues

When reporting issues, include:

1. **Test Scenario Number** (e.g., "Scenario 2: Urgent Care Case")
2. **Step Where Issue Occurred** (e.g., "Step 3: Duration question")
3. **Expected Behavior** (what should happen)
4. **Actual Behavior** (what actually happened)
5. **Screenshots/Logs** (if available)
6. **Reproducibility** (can you reproduce it?)

Example:
```
Issue: Workflow stopped after triage
Scenario: Test Scenario 1 (Critical Emergency)
Step: After triage completion
Expected: Automatic appointment booking
Actual: Agent waited for user input
Reproducible: Yes, every time
```

---

## Success Criteria

A test scenario is considered **PASSED** if:

✅ All 4 intake questions asked and answered  
✅ Automatic progression through all phases  
✅ Appropriate triage priority assigned  
✅ Appointment booked with correct urgency  
✅ Complete briefing generated  
✅ No errors or exceptions  
✅ Professional communication throughout  
✅ Workflow completes in < 3 minutes  

---

## Quick Test Commands

```bash
# Run automated tests
python -m tests.test_appointment

# Run system health check
python check_system.py

# Start web interface for manual testing
adk web
```

---

## Notes

- Test in a clean session for each scenario
- Don't mix scenarios in one conversation
- Refresh the page between test scenarios
- Document any unexpected behavior
- Test with different API models if available

**Happy Testing! 🧪**
