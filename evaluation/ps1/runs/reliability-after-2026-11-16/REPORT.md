# Actual PS1 diagnostic execution

Run status: completed

Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.

| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |
|---|---|---|---|---|---:|---:|
| ps1-02 | fusion | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 5 | 1.92 |
| ps1-02 | hyde | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 4 | 1.56 |
| ps1-02 | raw | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 4 | 1.09 |
| ps1-14 | fusion | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 5 | 0.20 |
| ps1-14 | hyde | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 5 | 0.11 |
| ps1-14 | raw | abstained | no_policy_found | groq/openai/gpt-oss-120b | 5 | 0.69 |
| ps1-21 | fusion | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 4 | 0.24 |
| ps1-21 | hyde | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 4 | 0.32 |
| ps1-21 | raw | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 4 | 0.14 |

## ps1-02 / fusion

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-fusion.json](ps1-02-fusion.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns the quantitative thresholds that trigger medical condonation of attendance deficiencies. Relevant documentation typically delineates specific attendance percentages below which a student may request consideration on medical grounds, accompanied by requisite evidence. The source material distinguishes routine class absences from missed examinations, each potentially subject to separate evaluative criteria.
```

Call 2: groq / openai/gpt-oss-120b

```text
Students must have at least 80 % attendance for the non‑medical period and an overall attendance (including the illness period) of at least 75 % to be considered for medical condonation.  

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Students must have at least\u202f80\u202f% attendance for the non\u2011medical period and an overall attendance (including the illness period) of at least\u202f75\u202f% to be considered for medical condonation."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "The AAC, depending on the merit of the case may permit the student to appear for the end semester exam."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "A student will be eligible for this concession at most in two semesters during the entire degree programme."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier."
  }
]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.7834295034408569; RRF 0.03252247488101534

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
```

Rank 2; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.7154680490493774; RRF 0.03252247488101534

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.6613121032714844; RRF 0.03149801587301587

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
```

Exact answer excerpt (if selected):
```text
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
```

Rank 4; chunk `ac6b11d2a25211ed773a4d8985763037eb61aad8055bfe6eb8308e03cd401f17`; page(s) [13]; cosine 0.652477502822876; RRF 0.030303030303030304

```text
Btech (Rules & Regulations)2013 21Nov2023 > Grade Points (GP)
S
A
B
C
D
P
F
0 (Failure) W
0 (Failure due to insufficient attendance) I
0 (Actual grade to be awarded later) SA
0 (Satisfactory, only for Pass/Fail Courses) US
0 (Unsatisfactory, only for Pass/Fail Courses)
B21.5. A student is considered to have credited a course or earned credits for a course only if he/she secures a grade other than F, W or I for that course.
B21.6. A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation, and the following criteria, in addition to poor attendance (less than 80%) may be considered for
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `7aa5e646bfbbd065cee501167ef3c9a182847d56cfc28e2fcea1e705c1f72da1`; page(s) [19]; cosine 0.6674221158027649; RRF 0.015873015873015872

```text
Btech (Rules & Regulations)2013 21Nov2023 > Responsibilities:
i.
To scrutinize the degree requirements, syllabus, course content proposed by Board of Studies.
ii.
To review the academic performances of slow learners and assess the causes of their unsatisfactory performance.
iii.
To consider the applications of students for special academic provisions under exceptional circumstances.
iv.
To review the cases for termination of students and recommend termination of students to the Senate.
v.
To formulate/recommend changes in the rules and regulations for various academic programmes and recommend to the Senate.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "raw": 22.6,
    "hyde": 845.5,
    "total": 1920.0,
    "answer": 974.6
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 800.8038997650146,
      "input_tokens": 206,
      "output_tokens": 105,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 971.3010787963867,
      "input_tokens": 866,
      "output_tokens": 149,
      "tokens_estimated_before": 1883,
      "tokens_estimated_after": 940
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-02 / hyde

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-hyde.json](ps1-02-hyde.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns the attendance thresholds relevant to medical condonation within the institutional handbook. The student seeks clarification on the quantitative levels of class participation that trigger eligibility for condonation on medical grounds, distinguishing between routine class absence and absence from a formally scheduled examination. The passage should reference the handbook’s terminology and structure without introducing specific percentages, deadlines, or procedural mandates.
```

Call 2: groq / openai/gpt-oss-120b

```text
Students must have at least 80 % attendance for the non‑medical period and an overall attendance (including the illness period) of at least 75 % to be considered for medical condonation.  

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Students must have at least\u202f80\u202f% attendance for the non\u2011medical period and an overall attendance (including the illness period) of at least\u202f75\u202f% to be considered for medical condonation."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "The AAC, depending on the merit of the case may permit the student to appear for the end semester exam."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "A student will be eligible for this concession at most in two semesters during the entire degree programme."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier."
  }
]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.7834295034408569; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
```

Rank 2; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.6613121032714844; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days. B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam. B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
```

Exact answer excerpt (if selected):
```text
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
```

Rank 4; chunk `cc88beed5878694ee081da67bc8b74c010d45736cbfe84cc801c50f6715bf804`; page(s) [3]; cosine 0.6471104621887207; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > TABLE OF CONTENTS
9 B10.
Discipline ................................................................................................................................. 9 B11.
Attendance ............................................................................................................................. 10 B12.
Assessment Procedure ........................................................................................................... 10 B13.
Internal Evaluation ................................................................................................................ 10 B14.
Mid and End term examination ............................................................................................. 11 B15.
Make-up examination ............................................................................................................ 11 B16. Re-examination (Amended in 23rd Senate meeting) .............................................................. 11 B17.
Summer Term Courses .......................................................................................................... 12 B18.
Repetition of a Course ........................................................................................................... 12 B19.
Courses under OT category ................................................................................................... 12 B20.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 16.1,
    "retrieve": 7.3,
    "total": 1561.7,
    "hyde": 675.9,
    "answer": 772.7
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 768.578052520752,
      "input_tokens": 866,
      "output_tokens": 149,
      "tokens_estimated_before": 2077,
      "tokens_estimated_after": 940
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-02 / raw

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-raw.json](ps1-02-raw.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
Students must have at least 80 % attendance for the non‑medical period and an overall attendance (including the illness period) of at least 75 % to be considered for medical condonation.  

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Students must have at least\u202f80\u202f% attendance for the non\u2011medical period and an overall attendance (including the illness period) of at least\u202f75\u202f% to be considered for medical condonation."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "The AAC, depending on the merit of the case may permit the student to appear for the end semester exam."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "A student will be eligible for this concession at most in two semesters during the entire degree programme."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier."
  }
]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.7834295034408569; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
```

Rank 2; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.6613121032714844; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days. B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam. B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
```

Exact answer excerpt (if selected):
```text
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
```

Rank 4; chunk `cc88beed5878694ee081da67bc8b74c010d45736cbfe84cc801c50f6715bf804`; page(s) [3]; cosine 0.6471104621887207; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > TABLE OF CONTENTS
9 B10.
Discipline ................................................................................................................................. 9 B11.
Attendance ............................................................................................................................. 10 B12.
Assessment Procedure ........................................................................................................... 10 B13.
Internal Evaluation ................................................................................................................ 10 B14.
Mid and End term examination ............................................................................................. 11 B15.
Make-up examination ............................................................................................................ 11 B16. Re-examination (Amended in 23rd Senate meeting) .............................................................. 11 B17.
Summer Term Courses .......................................................................................................... 12 B18.
Repetition of a Course ........................................................................................................... 12 B19.
Courses under OT category ................................................................................................... 12 B20.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 5.6,
    "retrieve": 4.6,
    "total": 1085.9,
    "answer": 990.9
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 983.1717014312744,
      "input_tokens": 866,
      "output_tokens": 149,
      "tokens_estimated_before": 2077,
      "tokens_estimated_after": 940
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-14 / fusion

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-fusion.json](ps1-14-fusion.json)

### Application output

The AI provider is rate-limited. Retrying in 15 seconds

### Actual generation and errors

Call 1: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

Call 2: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.7380107641220093; RRF 0.01639344262295082

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 2; chunk `1d762d9c0f0940f33c57fcc15a18899d2b721db20a6f9c91821c3799a70b0a55`; page(s) [21]; cosine 0.7072036862373352; RRF 0.016129032258064516

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper and subsequent papers will be cancelled.
• Case referred to Disciplinary Committee (DC) • The DC may recommend Year Back • Parents will be informed to report to Dean (Academics) Communicating with any student or any other person inside or outside the examination hall with a view to take assistance or aid to write answers in the examination
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.7019397616386414; RRF 0.015873015873015872

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `4050b0bc073af3c6899949c3dbefaf4ef877ff86d16707d3cf4e8d1b5ee1fec0`; page(s) [22]; cosine 0.7018308043479919; RRF 0.015625

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper will be cancelled.
• His/Her Roll No. will be noted down by exam cell.
• Parents will be informed to report to Dean (Academics)
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.7014567852020264; RRF 0.015384615384615385

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "raw": 17.7,
    "hyde": 106.7,
    "total": 201.6
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## ps1-14 / hyde

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-hyde.json](ps1-14-hyde.json)

### Application output

The AI provider is rate-limited. Retrying in 15 seconds

### Actual generation and errors

Call 1: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

Call 2: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.7380107641220093; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 2; chunk `1d762d9c0f0940f33c57fcc15a18899d2b721db20a6f9c91821c3799a70b0a55`; page(s) [21]; cosine 0.7072036862373352; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper and subsequent papers will be cancelled.
• Case referred to Disciplinary Committee (DC) • The DC may recommend Year Back • Parents will be informed to report to Dean (Academics) Communicating with any student or any other person inside or outside the examination hall with a view to take assistance or aid to write answers in the examination
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.7019397616386414; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `4050b0bc073af3c6899949c3dbefaf4ef877ff86d16707d3cf4e8d1b5ee1fec0`; page(s) [22]; cosine 0.7018308043479919; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper will be cancelled.
• His/Her Roll No. will be noted down by exam cell.
• Parents will be informed to report to Dean (Academics)
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.7014567852020264; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 18.4,
    "retrieve": 3.8,
    "total": 106.3,
    "hyde": 0.5
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## ps1-14 / raw

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-raw.json](ps1-14-raw.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
NO_POLICY_FOUND
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "NO_POLICY_FOUND"
  }
]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.7380107641220093; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
B11. Attendance
```

Rank 2; chunk `1d762d9c0f0940f33c57fcc15a18899d2b721db20a6f9c91821c3799a70b0a55`; page(s) [21]; cosine 0.7072036862373352; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper and subsequent papers will be cancelled.
• Case referred to Disciplinary Committee (DC) • The DC may recommend Year Back • Parents will be informed to report to Dean (Academics) Communicating with any student or any other person inside or outside the examination hall with a view to take assistance or aid to write answers in the examination
```

Exact answer excerpt (if selected):
```text
• The specific paper and subsequent papers will be cancelled.
• Case referred to Disciplinary Committee (DC) • The DC may recommend Year Back • Parents will be informed to report to Dean (Academics) Communicating with any student or any other person inside or outside the examination hall with a view to take assistance or aid to write answers in the examination
```

Rank 3; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.7019397616386414; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `4050b0bc073af3c6899949c3dbefaf4ef877ff86d16707d3cf4e8d1b5ee1fec0`; page(s) [22]; cosine 0.7018308043479919; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper will be cancelled.
• His/Her Roll No. will be noted down by exam cell.
• Parents will be informed to report to Dean (Academics)
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.7014567852020264; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 22.5,
    "retrieve": 5.5,
    "total": 692.7,
    "answer": 604.6
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 601.9823551177979,
      "input_tokens": 626,
      "output_tokens": 60,
      "tokens_estimated_before": 1726,
      "tokens_estimated_after": 631
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-21 / fusion

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-fusion.json](ps1-21-fusion.json)

### Application output

The AI provider is rate-limited. Retrying in 15 seconds

### Actual generation and errors

Call 1: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

Call 2: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.6804011464118958; RRF 0.01639344262295082

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 2; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.6001483798027039; RRF 0.016129032258064516

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days. B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam. B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.590642511844635; RRF 0.015625

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `30335857eed83d13bf844d4c88224d79389c44a172b6b2a7f166c4f47d7c4a8b`; page(s) [13]; cosine 0.5776695609092712; RRF 0.015384615384615385

```text
Btech (Rules & Regulations)2013 21Nov2023 > B21. Grading
B21.1. The faculty will return evaluated tests, assignments, tutorials, term papers, etc., within two weeks after their respective test/examination etc.
B21.2. Only the final grades (after approval by DCC) and attendance of all the students should be communicated by the teachers of the courses. Students may seek clarification regarding grades etc., from the concerned Course coordinator, if required.
B21.3. The DCC meeting will be convened within ten days after the last day of the end-term examination. The letter grades to be awarded to the students for different subjects will be finalized in the meeting.
B21.4. Based on the relative performance, each student is awarded a final letter grade for each of the course. The letter grades and the grade points are as follows. (Amended in 6th Senate
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "raw": 30.3,
    "hyde": 91.6,
    "total": 236.6
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## ps1-21 / hyde

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-hyde.json](ps1-21-hyde.json)

### Application output

The AI provider is rate-limited. Retrying in 15 seconds

### Actual generation and errors

Call 1: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

Call 2: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.6804011464118958; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 2; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.6001483798027039; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days. B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam. B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `30335857eed83d13bf844d4c88224d79389c44a172b6b2a7f166c4f47d7c4a8b`; page(s) [13]; cosine 0.5776695609092712; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B21. Grading
B21.1. The faculty will return evaluated tests, assignments, tutorials, term papers, etc., within two weeks after their respective test/examination etc.
B21.2. Only the final grades (after approval by DCC) and attendance of all the students should be communicated by the teachers of the courses. Students may seek clarification regarding grades etc., from the concerned Course coordinator, if required.
B21.3. The DCC meeting will be convened within ten days after the last day of the end-term examination. The letter grades to be awarded to the students for different subjects will be finalized in the meeting.
B21.4. Based on the relative performance, each student is awarded a final letter grade for each of the course. The letter grades and the grade points are as follows. (Amended in 6th Senate
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 20.8,
    "retrieve": 9.7,
    "total": 318.3,
    "hyde": 98.0
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## ps1-21 / raw

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-raw.json](ps1-21-raw.json)

### Application output

The AI provider is rate-limited. Retrying in 15 seconds

### Actual generation and errors

Call 1: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError",
  "provider": "groq",
  "status_code": 429,
  "retry_after_s": 15.0,
  "details": "{}"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `0930554c3b684462fca094df93f5fb7a528530ca8f065c0e7a0af03201c1a21e`; page(s) [10]; cosine 0.6804011464118958; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B11. Attendance
B11.1. Every member of the faculty handling a class shall record attendance on all days of instruction. The teacher of the course is required to finalize the attendance on the last instructional day of the course in the semester.
B11.2. A student whose attendance is less than 80% for a course is not eligible to appear for the End-term examination for that course.
B11.3. The details of all students who have attendance less than 80% in a course will be announced by the teacher in the class. These details will be sent to the concerned HoDs and AAC.
B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.
Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam. A student will be eligible for this concession at most in two semesters during the entire degree programme. Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.
B11.5. Students who are involved in extra-curricular activities, and those who represent the Institute in Sports & Games, Cultural Festivals, and Technical Festivals outside the Institute, should take prior approval from the HoD, Faculty Adviser and Teachers of the concerned courses. As an incentive to those, relaxation is provided such that their attendance should not fall below 75%. Additionally, specific to the nature of the activity, prior approval in writing needs to be taken from the following, citing reasons for absence.
1. Concerned Faculty Advisor and/or Faculty coordinator of the event - Technical Paper presentation/Attending Technical Festival.
2. Sports officer - Sports & Games.
All such applications for the condonation should be recommended by the concerned HoD and forwarded to AAC within seven instructional days after the programme/activity.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 2; chunk `b51f1377c2f10f11bf1aaaf6822edeb80107ebd464f69e409485ac0d85737db1`; page(s) [11]; cosine 0.6001483798027039; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days. B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam. B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `73bdd62de67829e1dde31528de6bc65e0c59bcb66c64bfceb86e6dce4904347b`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `30335857eed83d13bf844d4c88224d79389c44a172b6b2a7f166c4f47d7c4a8b`; page(s) [13]; cosine 0.5776695609092712; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B21. Grading
B21.1. The faculty will return evaluated tests, assignments, tutorials, term papers, etc., within two weeks after their respective test/examination etc.
B21.2. Only the final grades (after approval by DCC) and attendance of all the students should be communicated by the teachers of the courses. Students may seek clarification regarding grades etc., from the concerned Course coordinator, if required.
B21.3. The DCC meeting will be convened within ten days after the last day of the end-term examination. The letter grades to be awarded to the students for different subjects will be finalized in the meeting.
B21.4. Based on the relative performance, each student is awarded a final letter grade for each of the course. The letter grades and the grade points are as follows. (Amended in 6th Senate
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 10.9,
    "retrieve": 4.6,
    "total": 135.1
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## Production integrity

```json
{
  "files_checked": 244,
  "byte_identical": true
}
```