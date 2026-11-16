# Actual PS1 diagnostic execution

Run status: completed

Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.

| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |
|---|---|---|---|---|---:|---:|
| ps1-02 | fusion | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 4 | 1.76 |
| ps1-02 | hyde | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 5 | 2.14 |
| ps1-02 | raw | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 4 | 0.91 |
| ps1-14 | fusion | abstained | no_policy_found | groq/openai/gpt-oss-120b | 5 | 1.49 |
| ps1-14 | hyde | abstained | quote_verification_failed | groq/openai/gpt-oss-120b | 5 | 2.01 |
| ps1-14 | raw | abstained | no_policy_found | groq/openai/gpt-oss-120b | 5 | 1.00 |
| ps1-21 | fusion | abstained | unsupported_cited_claim | groq/openai/gpt-oss-120b | 4 | 1.97 |
| ps1-21 | hyde | abstained | incomplete_generation | groq/openai/gpt-oss-120b | 4 | 2.06 |
| ps1-21 | raw | abstained | incomplete_generation | groq/openai/gpt-oss-120b | 4 | 1.51 |

## ps1-02 / fusion

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-fusion.json](ps1-02-fusion.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns the attendance thresholds relevant to medical condonation within the institutional framework. The student seeks clarification on the quantitative criteria that trigger consideration of medical circumstances for excusing absences. The request references the handbook but does not provide specific figures, prompting a need to locate the precise attendance percentages or days stipulated for medical condonation.
```

Call 2: groq / openai/gpt-oss-120b

```text
Students must have at least 80 % attendance for the non‑medical period and their overall attendance—including the illness period—must not drop below 75 %【C1】.
```

### Validator failures

```json
[
  {
    "reason": "unsupported_claim_or_condition",
    "claim": "Students must have at least\u202f80\u202f% attendance for the non\u2011medical period and their overall attendance\u2014including the illness period\u2014must not drop below\u202f75\u202f%."
  }
]
```

### Retrieved evidence

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.7834295034408569; RRF 0.01639344262295082

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

Rank 2; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.701009213924408; RRF 0.016129032258064516

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.6613121032714844; RRF 0.015873015873015872

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

Rank 4; chunk `b1dca5bc1cb01039d4e036a8fb34418992863154aaa9e4057766dec6ac41b54c`; page(s) [3]; cosine 0.6471104621887207; RRF 0.015384615384615385

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
    "raw": 99.3,
    "hyde": 754.5,
    "total": 1762.1,
    "answer": 819.5
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 813.2832050323486,
      "input_tokens": 866,
      "output_tokens": 88,
      "finish_reason": "stop",
      "reasoning_tokens": 41,
      "tokens_estimated_before": 2077,
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
A targeted literature search was conducted to locate institutional policies concerning attendance thresholds that may be mitigated through medical condonation. Keywords combined “attendance requirements,” “medical exemption,” “condonation,” and “academic regulations” with Boolean operators to retrieve relevant handbook sections, policy manuals, and precedent documents. Results were filtered for explicit references to attendance percentages, documentation standards, and procedural steps associated with medically‑justified absences.
```

Call 2: groq / openai/gpt-oss-120b

```text
Students must have at least 80 % attendance for the non‑medical period, and their overall attendance—including the medical‑leave period—must not fall below 75 %【C1】.  
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "unsupported_claim_or_condition",
    "claim": "Students must have at least\u202f80\u202f% attendance for the non\u2011medical period, and their overall attendance\u2014including the medical\u2011leave period\u2014must not fall below\u202f75\u202f%."
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

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.77617347240448; RRF None

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

Rank 2; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.7327894568443298; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `b1dca5bc1cb01039d4e036a8fb34418992863154aaa9e4057766dec6ac41b54c`; page(s) [3]; cosine 0.7312868237495422; RRF None

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
B11.
Attendance ............................................................................................................................. 10
```

Rank 4; chunk `1f0b1ee8fd7a136492d25c4ed270c0870cab94bccde0ad7ef5c09393218bda37`; page(s) [3]; cosine 0.6991668939590454; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > TABLE OF CONTENTS
........................................................................................................................................................... 16 B28.
Withdrawal of Admission ...................................................................................................... 17 B29.
Unfair means during examinations (Amended in 22nd and 23rd Senate) ................................ 17 B30.
Academic Committees........................................................................................................... 17 B31.
Power to modify .................................................................................................................... 19
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `7c51cab980895e665a648d1b15160604ca27d1a76afcb2200ca2bf7171f024c6`; page(s) [1]; cosine 0.6805999279022217; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Academic Affairs
(2013-2014)
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
    "hyde": 945.4,
    "embed": 103.2,
    "retrieve": 13.8,
    "total": 2133.5,
    "answer": 923.5
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 940.403938293457,
      "input_tokens": 206,
      "output_tokens": 124,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 914.9651527404785,
      "input_tokens": 732,
      "output_tokens": 140,
      "finish_reason": "stop",
      "reasoning_tokens": 35,
      "tokens_estimated_before": 1776,
      "tokens_estimated_after": 801
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
Students must have at least 80 % attendance for the non‑medical period and their overall attendance—including the medical‑leave period—must not drop below 75 % to be eligible for medical condonation.  

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Students must have at least\u202f80\u202f% attendance for the non\u2011medical period and their overall attendance\u2014including the medical\u2011leave period\u2014must not drop below\u202f75\u202f%\u202fto be eligible for medical condonation."
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

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.7834295034408569; RRF None

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

Rank 2; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.6613121032714844; RRF None

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

Rank 4; chunk `b1dca5bc1cb01039d4e036a8fb34418992863154aaa9e4057766dec6ac41b54c`; page(s) [3]; cosine 0.6471104621887207; RRF None

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
    "embed": 61.7,
    "retrieve": 9.9,
    "total": 911.2,
    "answer": 702.6
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 694.1800117492676,
      "input_tokens": 866,
      "output_tokens": 143,
      "finish_reason": "stop",
      "reasoning_tokens": 35,
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

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns a student who experienced illness resulting in non‑attendance during instructional sessions, without indication of a missed assessment. The relevant literature examines institutional mechanisms for addressing instructional absences, including documentation requirements, academic advising protocols, and potential accommodations that permit continuation toward final examination eligibility, contingent upon verification of health‑related circumstances.
```

Call 2: groq / openai/gpt-oss-120b

```text
NO_POLICY_FOUND
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.7589457035064697; RRF 0.03278688524590164

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

Rank 2; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.7482469081878662; RRF 0.03200204813108039

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `d32957041c9fcbb2e316dea26d42dc1f95f60a0d159cb6c06d1fdafb1b8a6c22`; page(s) [21]; cosine 0.7072036862373352; RRF 0.03128054740957967

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

Rank 4; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.7058516144752502; RRF 0.031009615384615385

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

Rank 5; chunk `a983c2c22425eede0052b153f127dc8bfce4306c3f920fb701613f1d7673c67d`; page(s) [21]; cosine 0.6903567910194397; RRF 0.029411764705882353

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper of the concerned students will be cancelled.
• If the act is repeated for more than once, all the papers in the concerned semester will be cancelled.
• Parents will be informed to report to Dean (Academics) cases of destroying any evidence of malpractice, like tearing or mutilating the answer script(s) or running away along with the answer script(s) from the examination hall or premises
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
    "raw": 129.3,
    "hyde": 876.5,
    "total": 1486.6,
    "answer": 406.2
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 819.5080757141113,
      "input_tokens": 230,
      "output_tokens": 104,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 402.25887298583984,
      "input_tokens": 626,
      "output_tokens": 57,
      "finish_reason": "stop",
      "reasoning_tokens": 45,
      "tokens_estimated_before": 1791,
      "tokens_estimated_after": 631
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-14 / hyde

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-hyde.json](ps1-14-hyde.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
A concise academic search query for this scenario might read: “student illness attendance deficiency impact on final examination eligibility university policy” or “effects of class absenteeism due to health reasons on permission to sit final assessments”. Including terms such as “medical exemption”, “academic continuity”, “exam participation criteria” and “institutional guidelines for absent students” will retrieve relevant procedural documentation.
```

Call 2: groq / openai/gpt-oss-120b

```text
You can apply for a make‑up exam within five days of the missed exam, providing the reason for your absence; later applications will not be accepted.  

“Those who miss mid‑term and/or end‑term exam should apply … through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained.” [C3]
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "You can apply for a make\u2011up exam within five days of the missed exam, providing the reason for your absence; later applications will not be accepted."
  },
  {
    "reason": "unsupported_claim_or_condition",
    "claim": "\u201cThose who miss mid\u2011term and/or end\u2011term exam should apply \u2026 through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained.\u201d"
  }
]
```

### Retrieved evidence

Rank 1; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.7710750699043274; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 2; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.7239723801612854; RRF None

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

Rank 3; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.708044707775116; RRF None

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

Rank 4; chunk `a983c2c22425eede0052b153f127dc8bfce4306c3f920fb701613f1d7673c67d`; page(s) [21]; cosine 0.7046363353729248; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper of the concerned students will be cancelled.
• If the act is repeated for more than once, all the papers in the concerned semester will be cancelled.
• Parents will be informed to report to Dean (Academics) cases of destroying any evidence of malpractice, like tearing or mutilating the answer script(s) or running away along with the answer script(s) from the examination hall or premises
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `26190eb7b6f4b705fd7e2b4f52d24ffb239ea2a8a42c538bbc7522ac865ec9b1`; page(s) [19]; cosine 0.7039855122566223; RRF None

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
    "hyde": 934.7,
    "embed": 80.0,
    "retrieve": 9.1,
    "total": 2004.5,
    "answer": 857.5
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 933.8853359222412,
      "input_tokens": 230,
      "output_tokens": 116,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 852.6229858398438,
      "input_tokens": 702,
      "output_tokens": 117,
      "finish_reason": "stop",
      "reasoning_tokens": 28,
      "tokens_estimated_before": 1846,
      "tokens_estimated_after": 718
    }
  },
  "warnings": [
    "Quote could not be verified; the proposed answer was withheld."
  ],
  "error": null
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
[]
```

### Retrieved evidence

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.7380107641220093; RRF None

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

Rank 2; chunk `d32957041c9fcbb2e316dea26d42dc1f95f60a0d159cb6c06d1fdafb1b8a6c22`; page(s) [21]; cosine 0.7072036862373352; RRF None

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

Rank 3; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.7019397616386414; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `50a2f1cb137902176090864d576f3ea374147d7c3da2af9571c5eae8afa17681`; page(s) [22]; cosine 0.7018308043479919; RRF None

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

Rank 5; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.7014567852020264; RRF None

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
    "embed": 66.0,
    "retrieve": 5.2,
    "total": 999.5,
    "answer": 858.4
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 855.7970523834229,
      "input_tokens": 626,
      "output_tokens": 61,
      "finish_reason": "stop",
      "reasoning_tokens": 49,
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

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns the procedural handling of medical attendance condonation, encompassing the dual attendance thresholds that trigger review, the sequential steps required for obtaining approval, and the stipulated deadline by which medical leave documentation must be submitted. The passage outlines the relevant terminology and procedural phases without asserting specific regulatory values or mandatory actions.
```

Call 2: groq / openai/gpt-oss-120b

```text
Medical attendance condonation requires at least 80 % attendance in the non‑medical period and an overall attendance of 75 % or higher; the application must be recommended by the Faculty Advisor, the concerned faculty and the HoD, submitted to the AAC by the last instructional day of the semester, and the medical‑leave certificate must reach the HoD within seven days after return (or by the last instructional day, whichever is earlier)【C1】
```

### Validator failures

```json
[
  {
    "reason": "unsupported_claim_or_condition",
    "claim": "Medical attendance condonation requires at least\u202f80\u202f% attendance in the non\u2011medical period and an overall attendance of\u202f75\u202f% or higher; the application must be recommended by the Faculty Advisor, the concerned faculty and the HoD, submitted to the AAC by the last instructional day of the semester, and the medical\u2011leave certificate must reach the HoD within\u202fseven\u202fdays after return (or by the last instructional day, whichever is earlier)"
  }
]
```

### Retrieved evidence

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.6804011464118958; RRF 0.01639344262295082

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

Rank 2; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.6001483798027039; RRF 0.016129032258064516

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
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
```

Rank 3; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.590642511844635; RRF 0.015625

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `87f280afd7d37e99e3c2f5d35237c4747f7760cdee9a53407d8e44976c0af1fa`; page(s) [13]; cosine 0.5776695609092712; RRF 0.015384615384615385

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
    "raw": 108.7,
    "hyde": 704.0,
    "total": 1970.1,
    "answer": 1058.2
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1054.0318489074707,
      "input_tokens": 781,
      "output_tokens": 220,
      "finish_reason": "stop",
      "reasoning_tokens": 116,
      "tokens_estimated_before": 1950,
      "tokens_estimated_after": 839
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-21 / hyde

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-hyde.json](ps1-21-hyde.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
A search query concerning medical‑related attendance condonation may retrieve documents that outline the dual attendance thresholds applied to regular class participation and to examination eligibility, describe the procedural steps for obtaining a medical exemption, and specify the temporal parameters within which a medical leave request must be submitted.
```

Call 2: groq / openai/gpt-oss-120b

```text
Medical attendance condonation requires at least 80 % attendance in the non‑medical period and an overall attendance ≥ 75 %; the application must be recommended by the Faculty Advisor, the concerned faculty and the HoD, submitted to the AAC by the last instructional day of the semester, and the medical‑leave certificate must reach the HoD within seven days of return or by that last instructional day, whichever is earlier.  

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester… Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Medical attendance condonation requires at least\u202f80\u202f% attendance in the non\u2011medical period and an overall attendance\u202f\u2265\u202f75\u202f%; the application must be recommended by the Faculty Advisor, the concerned faculty and the HoD, submitted to the AAC by the last instructional day of the semester, and the medical\u2011leave certificate must reach the HoD within\u202fseven\u202fdays of return or by that last instructional day, whichever is earlier."
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
  }
]
```

### Retrieved evidence

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.6804011464118958; RRF None

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

Rank 2; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.6001483798027039; RRF None

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
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
```

Rank 3; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `87f280afd7d37e99e3c2f5d35237c4747f7760cdee9a53407d8e44976c0af1fa`; page(s) [13]; cosine 0.5776695609092712; RRF None

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
    "embed": 84.0,
    "retrieve": 10.4,
    "total": 2062.6,
    "hyde": 761.3,
    "answer": 1060.9
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1057.9450130462646,
      "input_tokens": 1549,
      "output_tokens": 350,
      "finish_reason": "length",
      "reasoning_tokens": 116,
      "tokens_estimated_before": 1950,
      "tokens_estimated_after": 839
    }
  },
  "warnings": [],
  "error": null
}
```

## ps1-21 / raw

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-raw.json](ps1-21-raw.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
Medical attendance condonation requires ≥ 80 % attendance for the non‑medical period and an overall attendance ≥ 75 %; the application must be recommended by the Faculty Advisor, the concerned faculty and the HoD, submitted to the AAC by the last instructional day of the semester, and the AAC may permit the exam. The medical‑leave application with a certified medical certificate must reach the HoD within 7 days of return or by the last instructional day, whichever is earlier. [“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Medical attendance condonation requires\u202f\u2265\u202f80\u202f% attendance for the non\u2011medical period and an overall attendance\u202f\u2265\u202f75\u202f%; the application must be recommended by the Faculty Advisor, the concerned faculty and the HoD, submitted to the AAC by the last instructional day of the semester, and the AAC may permit the exam."
  },
  {
    "reason": "uncited_claim",
    "claim": "The medical\u2011leave application with a certified medical certificate must reach the HoD within\u202f7\u202fdays of return or by the last instructional day, whichever is earlier."
  },
  {
    "reason": "uncited_claim",
    "claim": "[\u201cThose who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%."
  },
  {
    "reason": "uncited_claim",
    "claim": "Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before"
  }
]
```

### Retrieved evidence

Rank 1; chunk `f838100884ca4c21e89300962dffad5be61be561c31923d3bbc8fb70239cd77d`; page(s) [10]; cosine 0.6804011464118958; RRF None

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

Rank 2; chunk `871f1921d289d97fabc6cb99c915b8eb97ab4cb706128c9af83faaeea87a6e5f`; page(s) [11]; cosine 0.6001483798027039; RRF None

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
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination.
```

Rank 3; chunk `77eee1b82819cfe8405a2e7befdd8ff30991204e7260d1db04f2ce6df9cf3bc9`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `87f280afd7d37e99e3c2f5d35237c4747f7760cdee9a53407d8e44976c0af1fa`; page(s) [13]; cosine 0.5776695609092712; RRF None

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
    "embed": 80.3,
    "retrieve": 17.6,
    "total": 1499.3,
    "answer": 1235.7
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1232.5739860534668,
      "input_tokens": 781,
      "output_tokens": 350,
      "finish_reason": "length",
      "reasoning_tokens": 163,
      "tokens_estimated_before": 1950,
      "tokens_estimated_after": 839
    }
  },
  "warnings": [],
  "error": null
}
```

## Production integrity

```json
{
  "files_checked": 244,
  "byte_identical": true
}
```