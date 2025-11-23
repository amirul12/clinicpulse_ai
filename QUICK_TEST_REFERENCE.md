# ClinicPulse AI - Quick Test Reference Card

## 🚀 Quick Start
```bash
source .venv/bin/activate
export GOOGLE_API_KEY="your-key"
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
adk web
```

---

## 📋 Test Scenarios with Expected Responses

### ⚠️ SCENARIO 1: CRITICAL - Chest Pain

**Conversation Flow:**

```
👤 USER: Hello

🤖 AGENT: Hello! Welcome to our clinic. Could I please get your name or patient ID?

👤 USER: Sarah Johnson

🤖 AGENT: Thank you, Sarah. What symptoms are you experiencing?

👤 USER: Severe chest pain radiating to my left arm

🤖 AGENT: When did the chest pain start?

👤 USER: About 30 minutes ago

🤖 AGENT: Do you have any medical conditions like diabetes, heart disease, or allergies?

👤 USER: I have high blood pressure and diabetes

🤖 AGENT: Thank you for providing that information.

[Intake complete]

[Running triage assessment...]
Based on your symptoms of severe chest pain radiating to the left arm, this is classified as CRITICAL priority. This requires immediate medical attention.

[Triage complete]

[Scheduling appointment...]
Appointment booked with Dr. Heart (Cardiology) for 2025-11-23 11:30
Confirmation sent via email and SMS.
Location: Clinic Building A, Room 201

[Appointment booked]

[Generating clinician briefing...]

## Patient Briefing - Sarah Johnson

### Overview
- **Patient**: Sarah Johnson
- **Chief Complaint**: Severe chest pain radiating to left arm
- **Duration**: 30 minutes
- **Priority**: CRITICAL

### Medical History
- High blood pressure
- Diabetes

### Triage Assessment
- **Priority Level**: Critical
- **Rationale**: Chest pain with radiation to left arm is a classic sign of acute coronary syndrome and requires immediate evaluation to rule out myocardial infarction.
- **Recommended Next Steps**: Immediate ECG, cardiac enzyme panel, vital signs monitoring

### Appointment Details
- **Doctor**: Dr. Heart (Cardiology)
- **Time**: 2025-11-23 11:30
- **Location**: Clinic Building A, Room 201
- **Type**: Emergency consultation

### Recommended Clinical Actions
- Immediate 12-lead ECG
- Troponin and cardiac enzyme panel
- Continuous vital signs monitoring
- Aspirin administration if not contraindicated
- Prepare for possible cardiac catheterization

[Briefing ready]
```

**✅ Expected Results:**
- Priority: **CRITICAL**
- Appointment: **Same-day, urgent slot**
- Specialty: **Cardiology**
- Timing: **Immediate/within hours**

---

### 🔴 SCENARIO 2: URGENT - High Fever

**Conversation Flow:**

```
👤 USER: Hello

🤖 AGENT: Hello! Welcome to our clinic. Could I please get your name or patient ID?

👤 USER: Michael Chen

🤖 AGENT: Thank you, Michael. What symptoms are you experiencing?

👤 USER: High fever of 103°F, severe headache, and body aches

🤖 AGENT: When did these symptoms start?

👤 USER: 2 days ago

🤖 AGENT: Do you have any medical conditions like diabetes, heart disease, or allergies?

👤 USER: No chronic conditions, but allergic to penicillin

🤖 AGENT: Thank you for providing that information.

[Intake complete]

[Running triage assessment...]
Based on your high fever (103°F) with severe headache and body aches, this is classified as URGENT priority. These symptoms suggest a possible infection that needs prompt medical attention.

[Triage complete]

[Scheduling appointment...]
Appointment booked with Dr. Johnson (General Practice) for 2025-11-24 14:00
Confirmation sent via email and SMS.
Location: Clinic Building A, Room 201

[Appointment booked]

[Generating clinician briefing...]

## Patient Briefing - Michael Chen

### Overview
- **Patient**: Michael Chen
- **Chief Complaint**: High fever (103°F), severe headache, body aches
- **Duration**: 2 days
- **Priority**: URGENT

### Medical History
- No chronic conditions
- **Allergy**: Penicillin (IMPORTANT)

### Triage Assessment
- **Priority Level**: Urgent
- **Rationale**: High fever with systemic symptoms suggests acute infection requiring prompt evaluation and treatment. Penicillin allergy noted for medication planning.
- **Recommended Next Steps**: Physical examination, possible lab work, alternative antibiotic therapy

### Appointment Details
- **Doctor**: Dr. Johnson (General Practice)
- **Time**: 2025-11-24 14:00 (Next day)
- **Location**: Clinic Building A, Room 201
- **Type**: Urgent consultation

### Recommended Clinical Actions
- Complete physical examination
- CBC with differential
- Consider flu test or COVID-19 testing
- Antipyretics for fever management
- **AVOID penicillin-based antibiotics** - use alternatives (azithromycin, fluoroquinolones)
- Hydration assessment

[Briefing ready]
```

**✅ Expected Results:**
- Priority: **URGENT**
- Appointment: **Within 1-3 days**
- Specialty: **General Practice**
- Special Note: **Penicillin allergy flagged**

---

### 🟢 SCENARIO 3: ROUTINE - Minor Knee Pain

**Conversation Flow:**

```
👤 USER: Hi there

🤖 AGENT: Hello! Welcome to our clinic. Could I please get your name or patient ID?

👤 USER: Emily Rodriguez

🤖 AGENT: Thank you, Emily. What symptoms are you experiencing?

👤 USER: Mild knee pain when walking

🤖 AGENT: When did the knee pain start?

👤 USER: About 2 weeks ago

🤖 AGENT: Do you have any medical conditions like diabetes, heart disease, or allergies?

👤 USER: None

🤖 AGENT: Thank you for providing that information.

[Intake complete]

[Running triage assessment...]
Based on your mild knee pain that started 2 weeks ago, this is classified as ROUTINE priority. This can be addressed with a standard appointment.

[Triage complete]

[Scheduling appointment...]
Appointment booked with Dr. Bones (Orthopedics) for 2025-12-05 10:00
Confirmation sent via email and SMS.
Location: Clinic Building A, Room 201

[Appointment booked]

[Generating clinician briefing...]

## Patient Briefing - Emily Rodriguez

### Overview
- **Patient**: Emily Rodriguez
- **Chief Complaint**: Mild knee pain when walking
- **Duration**: 2 weeks
- **Priority**: ROUTINE

### Medical History
- No chronic conditions
- No known allergies

### Triage Assessment
- **Priority Level**: Routine
- **Rationale**: Mild knee pain without acute injury or severe symptoms can be evaluated in a routine appointment. No red flags for urgent intervention.
- **Recommended Next Steps**: Physical examination, possible X-ray, conservative management

### Appointment Details
- **Doctor**: Dr. Bones (Orthopedics)
- **Time**: 2025-12-05 10:00 (1-2 weeks out)
- **Location**: Clinic Building A, Room 201
- **Type**: Routine consultation

### Recommended Clinical Actions
- Physical examination of knee joint
- Range of motion assessment
- X-ray if indicated
- Consider conservative treatment: rest, ice, compression, elevation (RICE)
- Physical therapy referral if needed
- NSAIDs for pain management

[Briefing ready]
```

**✅ Expected Results:**
- Priority: **ROUTINE**
- Appointment: **1-2 weeks out**
- Specialty: **Orthopedics**
- Approach: **Conservative management**

---

### 🏥 SCENARIO 4: COMPLEX - Multiple Chronic Conditions

**Conversation Flow:**

```
👤 USER: Hello

🤖 AGENT: Hello! Welcome to our clinic. Could I please get your name or patient ID?

👤 USER: Robert Thompson

🤖 AGENT: Thank you, Robert. What symptoms are you experiencing?

👤 USER: Shortness of breath and fatigue

🤖 AGENT: When did these symptoms start?

👤 USER: Started gradually over the past week

🤖 AGENT: Do you have any medical conditions like diabetes, heart disease, or allergies?

👤 USER: Type 2 diabetes, heart disease, hypertension, and asthma

🤖 AGENT: Thank you for providing that information.

[Intake complete]

[Running triage assessment...]
Given your symptoms of shortness of breath and fatigue, combined with your history of heart disease, diabetes, hypertension, and asthma, this is classified as URGENT priority. These symptoms require prompt evaluation given your cardiac and respiratory history.

[Triage complete]

[Scheduling appointment...]
Appointment booked with Dr. Cardio (Cardiology) for 2025-11-24 09:00
Confirmation sent via email and SMS.
Location: Clinic Building A, Room 201

[Appointment booked]

[Generating clinician briefing...]

## Patient Briefing - Robert Thompson

### Overview
- **Patient**: Robert Thompson
- **Chief Complaint**: Shortness of breath and fatigue
- **Duration**: 1 week (gradual onset)
- **Priority**: URGENT

### Medical History
- **Type 2 Diabetes**
- **Heart Disease** (HIGH RISK)
- **Hypertension**
- **Asthma**

### Triage Assessment
- **Priority Level**: Urgent
- **Rationale**: Shortness of breath in a patient with known heart disease and multiple comorbidities requires urgent evaluation to rule out cardiac decompensation, pulmonary edema, or exacerbation of chronic conditions.
- **Recommended Next Steps**: Comprehensive cardiac and pulmonary workup

### Appointment Details
- **Doctor**: Dr. Cardio (Cardiology)
- **Time**: 2025-11-24 09:00 (Next day, early)
- **Location**: Clinic Building A, Room 201
- **Type**: Urgent consultation

### Recommended Clinical Actions
- **Cardiac Assessment**:
  - ECG
  - Echocardiogram
  - BNP levels
  - Troponin if acute coronary syndrome suspected
- **Pulmonary Assessment**:
  - Chest X-ray
  - Pulse oximetry
  - Spirometry if asthma exacerbation suspected
- **Metabolic Panel**:
  - HbA1c (diabetes control)
  - Renal function (given multiple conditions)
  - Electrolytes
- **Medication Review**: Assess current medications for all chronic conditions
- **Risk Stratification**: High-risk patient requiring close monitoring

[Briefing ready]
```

**✅ Expected Results:**
- Priority: **URGENT** (due to cardiac history)
- Appointment: **Next day, early slot**
- Specialty: **Cardiology**
- Comprehensive workup recommended

---

### 👶 SCENARIO 5: PEDIATRIC - Child with Fever

**Conversation Flow:**

```
👤 USER: Hello

🤖 AGENT: Hello! Welcome to our clinic. Could I please get your name or patient ID?

👤 USER: Emma Wilson (parent: Lisa Wilson)

🤖 AGENT: Thank you. What symptoms is Emma experiencing?

👤 USER: My 5-year-old daughter has a fever and ear pain

🤖 AGENT: When did these symptoms start?

👤 USER: Yesterday evening

🤖 AGENT: Does Emma have any medical conditions like diabetes, heart disease, or allergies?

👤 USER: No known allergies or conditions

🤖 AGENT: Thank you for providing that information.

[Intake complete]

[Running triage assessment...]
For a 5-year-old child with fever and ear pain, this is classified as URGENT priority. Pediatric patients with fever and ear pain require prompt evaluation to prevent complications.

[Triage complete]

[Scheduling appointment...]
Appointment booked with Dr. Kids (Pediatrics) for 2025-11-23 15:00
Confirmation sent via email and SMS.
Location: Clinic Building A, Room 201

[Appointment booked]

[Generating clinician briefing...]

## Patient Briefing - Emma Wilson

### Overview
- **Patient**: Emma Wilson (Age: 5 years)
- **Parent/Guardian**: Lisa Wilson
- **Chief Complaint**: Fever and ear pain
- **Duration**: Since yesterday evening (~24 hours)
- **Priority**: URGENT

### Medical History
- No known chronic conditions
- No known allergies
- **Pediatric patient** - age-appropriate care required

### Triage Assessment
- **Priority Level**: Urgent
- **Rationale**: Pediatric fever with ear pain suggests acute otitis media (ear infection). Prompt treatment prevents complications such as mastoiditis or hearing loss. Same-day or next-day appointment recommended for pediatric fever cases.
- **Recommended Next Steps**: Otoscopic examination, possible antibiotic therapy

### Appointment Details
- **Doctor**: Dr. Kids (Pediatrics)
- **Time**: 2025-11-23 15:00 (Same day)
- **Location**: Clinic Building A, Room 201
- **Type**: Pediatric urgent consultation

### Recommended Clinical Actions
- **Examination**:
  - Otoscopic examination of both ears
  - Throat examination
  - Temperature check
  - Lymph node palpation
- **Likely Diagnosis**: Acute otitis media
- **Treatment Considerations**:
  - Age-appropriate antibiotic (amoxicillin first-line)
  - Antipyretics (acetaminophen or ibuprofen - age/weight appropriate dosing)
  - Pain management for ear pain
- **Parent Education**:
  - Medication administration
  - Warning signs (worsening symptoms, high fever >104°F)
  - Follow-up in 48-72 hours if no improvement
- **Special Considerations**: Pediatric dosing, child-friendly communication

[Briefing ready]
```

**✅ Expected Results:**
- Priority: **URGENT** (pediatric fever)
- Appointment: **Same-day or next-day**
- Specialty: **Pediatrics**
- Age-appropriate care emphasized

---

### 🚨 SCENARIO 6: EMERGENCY - Anaphylaxis

**Conversation Flow:**

```
👤 USER: HELP!

🤖 AGENT: Hello! I'm here to help. Could I please get your name or patient ID?

👤 USER: Alex Martinez

🤖 AGENT: Thank you, Alex. What symptoms are you experiencing?

👤 USER: Severe facial swelling, difficulty breathing, hives all over body

🤖 AGENT: When did these symptoms start?

👤 USER: Just now, about 10 minutes ago after eating peanuts

🤖 AGENT: Do you have any medical conditions like diabetes, heart disease, or allergies?

👤 USER: Known peanut allergy, carry EpiPen

🤖 AGENT: Thank you for providing that information.

[Intake complete]

[Running triage assessment...]
⚠️ CRITICAL EMERGENCY: Based on your symptoms of severe facial swelling, difficulty breathing, and hives after peanut exposure with known peanut allergy, this is ANAPHYLAXIS - a life-threatening allergic reaction requiring IMMEDIATE emergency intervention.

[Triage complete]

[Scheduling appointment...]
⚠️ EMERGENCY PROTOCOL ACTIVATED
Immediate emergency appointment arranged.
Emergency services notified.
Location: Emergency Department - IMMEDIATE

[Appointment booked]

[Generating clinician briefing...]

## ⚠️ EMERGENCY PATIENT BRIEFING - Alex Martinez

### Overview
- **Patient**: Alex Martinez
- **Chief Complaint**: Anaphylaxis (severe allergic reaction)
- **Trigger**: Peanut exposure
- **Duration**: 10 minutes ago (ACUTE)
- **Priority**: ⚠️ CRITICAL EMERGENCY

### Medical History
- **Known peanut allergy**
- **Carries EpiPen**

### Triage Assessment
- **Priority Level**: CRITICAL EMERGENCY
- **Rationale**: Classic presentation of anaphylaxis with:
  - Severe facial swelling (angioedema)
  - Difficulty breathing (respiratory compromise)
  - Hives (urticaria)
  - Known allergen exposure (peanuts)
  
  This is a life-threatening emergency requiring immediate intervention.

### Emergency Protocol
- **Status**: EMERGENCY - IMMEDIATE INTERVENTION REQUIRED
- **Location**: Emergency Department
- **EMS**: Consider calling 911 if not already done

### IMMEDIATE Actions Required

**FIRST AID (If EpiPen available):**
1. ✅ Administer EpiPen immediately to outer thigh
2. ✅ Call 911 / Emergency services
3. ✅ Position patient lying down with legs elevated
4. ✅ Monitor breathing and consciousness
5. ✅ Prepare for second EpiPen dose if needed (5-15 minutes)

**EMERGENCY DEPARTMENT TREATMENT:**
- **Airway Management**: 
  - Assess airway patency
  - Prepare for intubation if severe respiratory distress
  - Oxygen supplementation
- **Medications**:
  - Epinephrine IM (0.3-0.5mg) - repeat q5-15min if needed
  - IV antihistamines (diphenhydramine)
  - IV corticosteroids (methylprednisolone)
  - IV fluids for blood pressure support
  - Bronchodilators if wheezing
- **Monitoring**:
  - Continuous vital signs
  - Cardiac monitoring
  - Pulse oximetry
  - Watch for biphasic reaction (4-8 hours)
- **Observation**: Minimum 4-6 hours post-treatment

### Critical Notes
- ⚠️ **TIME-SENSITIVE EMERGENCY**
- ⚠️ **Airway compromise risk**
- ⚠️ **Cardiovascular collapse risk**
- ⚠️ **Requires immediate epinephrine**
- ⚠️ **Extended observation required**

### Discharge Planning (Post-Stabilization)
- EpiPen prescription (2 auto-injectors)
- Allergy action plan
- Allergist referral
- Medical alert bracelet
- Strict peanut avoidance education

[EMERGENCY BRIEFING COMPLETE]
```

**✅ Expected Results:**
- Priority: **CRITICAL EMERGENCY**
- Appointment: **IMMEDIATE / Call 911**
- Location: **Emergency Department**
- Protocol: **Anaphylaxis emergency protocol**

---

## ✅ Quick Validation Checklist

After each scenario, verify:

**Intake Phase:**
- [ ] Agent asks 4 questions (name, symptoms, duration, history)
- [ ] ONE question at a time
- [ ] No repeated questions
- [ ] Accepts answers and progresses

**Automatic Progression:**
- [ ] Triage runs automatically (no user prompt)
- [ ] Appointment books automatically (no user prompt)
- [ ] Briefing generates automatically (no user prompt)

**Output Quality:**
- [ ] Priority matches severity (Critical/Urgent/Routine)
- [ ] Appointment timing appropriate for priority
- [ ] Specialty matches symptoms
- [ ] Briefing includes all sections
- [ ] Professional, clear communication

**Performance:**
- [ ] Total workflow < 3 minutes
- [ ] No errors or exceptions
- [ ] Status updates provided

---

## 🎯 Expected Priority Levels

| Scenario | Priority | Timing | Specialty |
|----------|----------|--------|-----------|
| Chest Pain | CRITICAL | Same-day/Hours | Cardiology |
| High Fever | URGENT | 1-3 days | General Practice |
| Knee Pain | ROUTINE | 1-2 weeks | Orthopedics |
| SOB + Cardiac Hx | URGENT | Next day | Cardiology |
| Pediatric Fever | URGENT | Same/Next day | Pediatrics |
| Anaphylaxis | CRITICAL | IMMEDIATE | Emergency |

---

## 📊 Quick Commands

```bash
# Run automated tests
python -m tests.test_appointment

# System health check
python check_system.py

# Start web interface
adk web
```

---

**Full Detailed Guide:** See `MANUAL_TESTING_GUIDE.md`
