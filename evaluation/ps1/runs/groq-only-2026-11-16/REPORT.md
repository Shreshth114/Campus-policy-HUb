# Actual PS1 diagnostic execution

Run status: completed

Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.

| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |
|---|---|---|---|---|---:|---:|
| ps1-02 | fusion | abstained | citation_check_failed | groq/openai/gpt-oss-120b | 4 | 4.81 |
| ps1-02 | hyde | abstained | citation_check_failed | groq/openai/gpt-oss-120b | 5 | 2.62 |
| ps1-02 | raw | abstained | citation_check_failed | groq/openai/gpt-oss-120b | 4 | 1.41 |
| ps1-14 | fusion | abstained | citation_check_failed | groq/openai/gpt-oss-120b | 5 | 2.32 |
| ps1-14 | hyde | abstained | citation_check_failed | groq/openai/gpt-oss-120b | 4 | 2.51 |
| ps1-14 | raw | abstained | citation_check_failed | groq/openai/gpt-oss-120b | 5 | 1.39 |
| ps1-21 | fusion | provider_unavailable | The AI provider is rate-limited. Retrying in 4 seconds | / | 4 | 9.85 |
| ps1-21 | hyde | provider_unavailable | The AI provider is rate-limited. Retrying in 5 seconds | groq/openai/gpt-oss-120b; / | 4 | 7.88 |
| ps1-21 | raw | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 4 | 1.41 |

## ps1-02 / fusion

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-fusion.json](ps1-02-fusion.json)

### Application output

I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
A student shall be deemed eligible for medical attendance condonation when documented medical incapacity results in an aggregate absence not exceeding twenty‑five percent (25 %) of the total scheduled contact hours for the applicable instructional unit, provided that the deficiency is substantiated by a physician’s certificate issued within five (5) calendar days of the initial missed session. Attendance shortfalls exceeding this threshold shall require intermittent academic accommodations, subject to the approval of the Head of the Department and the Office of Student Affairs, and shall be recorded on the official attendance register. All cond
```

Call 2: groq / openai/gpt-oss-120b

```text
At least 80 % attendance in the periods other than medical leave, and the overall attendance—including the medical‑leave period—must not drop below 75 %【C1】.  
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "At least\u202f80\u202f% attendance in the periods\u202fother\u202fthan medical leave, and the overall attendance\u2014including the medical\u2011leave period\u2014must not drop below\u202f75\u202f%\u3010C1\u3011."
  },
  {
    "reason": "uncited_claim",
    "claim": "\u201cThose who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.\u201d\u3010C1\u3011"
  }
]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.7932882905006409; RRF 0.03278688524590164

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

Rank 2; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.76402348279953; RRF 0.03225806451612903

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `fc0f228bc6d373fa1831a4b989c3620e3938fff5d7e6c12057da81ebd9fdf675`; page(s) [11]; cosine 0.7047102451324463; RRF 0.031746031746031744

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

Rank 4; chunk `f6e723d7552445109cf3ed7ac50579f799610086c363c75734232de942186925`; page(s) [3]; cosine 0.6695125699043274; RRF 0.030090497737556562

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
    "raw": 18.7,
    "hyde": 3769.9,
    "total": 4806.2,
    "answer": 936.5
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 3722.965955734253,
      "input_tokens": 242,
      "output_tokens": 200,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 933.7122440338135,
      "input_tokens": 858,
      "output_tokens": 263,
      "tokens_estimated_before": 2070,
      "tokens_estimated_after": 933
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
A student shall be deemed to have satisfied the minimum attendance requirement for any prescribed course when the aggregate of documented presence and duly authorized medical condonation reaches at least seventy‑five percent (75 %) of the total scheduled instructional hours for the semester. Medical condonation shall be granted only upon submission of a certified medical certificate to the Office of the Registrar within five (5) working days of the absence, and shall be subject to verification by the Head of the Department. Each instance of condonation shall be recorded on the student’s attendance ledger and may not exceed a cumulative total of ten (10) percent of the semester’s instructional time without further institutional approval.
```

Call 2: groq / openai/gpt-oss-120b

```text
At least 80 % attendance in the non‑medical periods, and the overall attendance—including the medical‑leave period—must not be below 75 %【C1】.

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "At least\u202f80\u202f% attendance in the non\u2011medical periods, and the overall attendance\u2014including the medical\u2011leave period\u2014must not be below\u202f75\u202f%\u3010C1\u3011."
  },
  {
    "reason": "uncited_claim",
    "claim": "\u201cThose who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.\u201d\u3010C1\u3011"
  }
]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.8089994192123413; RRF None

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

Rank 2; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.7170696258544922; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `5f65583cd8f796ad54c50d02537940883d487b4d76540d1ae0e83e6aa389df11`; page(s) [11]; cosine 0.7011747360229492; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days.
B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam.
B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
```

Exact answer excerpt (if selected):
```text
B15. Make-up examination
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days.
```

Rank 4; chunk `7fb5bd8b152da307a1ff1472ce1031d1e02aade4d81dae4529567eaa18731334`; page(s) [17]; cosine 0.6975237727165222; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Constitution of third to eight semester DCC:
a) HoD/HoD’s nominee to act as Chairperson, b) All the Course coordinators offering courses, c) Faculty advisor of the class, d) Two students of the class nominated by the faculty advisor or elected by students among themselves.
The term of the CC/DCC shall be one semester. The committee shall meet at least twice during the semester. The Director and AAC shall have the right to be present in any meeting of any class committee. The faculty advisor shall record the proceedings of each meeting and communicate a
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `b0900abd64a3e8739d25d76c22f9f583635fa6a25b2f035d477ee3c44d7d6933`; page(s) [14]; cosine 0.6946646571159363; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B22. Declaration of Results
B22.1. The course instructor may allow the students to see the evaluated answer scripts at his/her discretion, as long as this is done before finalization of grades. The time limit fixed for such a disclosure is five days before the last date for receiving grades in the Exam Cell.
B22.2. Two copies of the result sheets for the respective course containing the final grade along with two copies with the absolute marks & grades should be submitted to the concerned DCC.
After finalization of the grades at the DCC meeting, hard and soft copies of consolidated result with a) absolute marks and grades b) only grades, will be forwarded by the HoD to the Exam cell.
A record of the approved consolidated result should be sent by the Exam cell back to the concerned HoDs.
B22.3. The Exam cell must announce the results of all the courses.
B22.4. Once grades are published, changes if any, will be allowed in case of tabulation errors only. A request for re-tabulation can be made by student to the course teacher within 2 days of result publication. A request for changes in grade due to tabulation errors (if any) can be made by the teacher of the course, by forwarding the request through the DCC to Exam cell.
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
    "hyde": 1240.4,
    "embed": 49.2,
    "retrieve": 6.3,
    "total": 2620.6,
    "answer": 1241.8
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1240.1199340820312,
      "input_tokens": 242,
      "output_tokens": 197,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1239.0210628509521,
      "input_tokens": 789,
      "output_tokens": 343,
      "tokens_estimated_before": 1899,
      "tokens_estimated_after": 856
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
At least 80 % attendance in the non‑medical period, and the overall attendance—including the medical‑leave period—must not drop below 75 %【C1】.  
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "At least\u202f80\u202f% attendance in the non\u2011medical period, and the overall attendance\u2014including the medical\u2011leave period\u2014must not drop below\u202f75\u202f%\u3010C1\u3011."
  },
  {
    "reason": "uncited_claim",
    "claim": "\u201cThose who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.\u201d\u3010C1\u3011"
  }
]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.7834295034408569; RRF None

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

Rank 2; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `fc0f228bc6d373fa1831a4b989c3620e3938fff5d7e6c12057da81ebd9fdf675`; page(s) [11]; cosine 0.6613121032714844; RRF None

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

Rank 4; chunk `f6e723d7552445109cf3ed7ac50579f799610086c363c75734232de942186925`; page(s) [3]; cosine 0.6471104621887207; RRF None

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
    "embed": 5.3,
    "retrieve": 4.4,
    "total": 1407.8,
    "answer": 1314.6
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1310.0087642669678,
      "input_tokens": 858,
      "output_tokens": 260,
      "tokens_estimated_before": 2070,
      "tokens_estimated_after": 933
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
A student shall be deemed eligible to sit for the scheduled final examination only upon satisfactory fulfillment of the attendance requirement prescribed in Article 3.2, subject to the submission of a duly authenticated medical certificate evidencing incapacity to attend classes for a period not exceeding fourteen (14) consecutive days. Upon receipt of such documentation, the Office of Academic Affairs may grant attendance condonation, permitting the student to undertake the final examination on the originally appointed date, provided that prior written permission is obtained from the Head of the Department and the Examination Committee
```

Call 2: groq / openai/gpt-oss-120b

```text
Yes—you can request a make‑up exam by applying to the Head of Department (or first
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Yes\u2014you can request a make\u2011up exam by applying to the Head of Department (or first"
  }
]
```

### Retrieved evidence

Rank 1; chunk `fc0f228bc6d373fa1831a4b989c3620e3938fff5d7e6c12057da81ebd9fdf675`; page(s) [11]; cosine 0.7033289670944214; RRF 0.032018442622950824

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

Rank 2; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.7726747989654541; RRF 0.032018442622950824

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

Rank 3; chunk `5d4ede4d4536e66a820d0835ec9d3ef8b07791650aefeecf92d1d0469a9bd4d1`; page(s) [21]; cosine 0.6641040444374084; RRF 0.016129032258064516

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

Rank 4; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.7259143590927124; RRF 0.016129032258064516

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `8a3e2367b9d10b556aa852971b1375f57390533a2c1566480c06b2a4d0fd04a6`; page(s) [21]; cosine 0.6556234955787659; RRF 0.015873015873015872

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
    "raw": 23.3,
    "hyde": 1057.7,
    "total": 2324.3,
    "answer": 1177.9
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1010.9660625457764,
      "input_tokens": 250,
      "output_tokens": 200,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1175.1830577850342,
      "input_tokens": 687,
      "output_tokens": 350,
      "tokens_estimated_before": 1784,
      "tokens_estimated_after": 701
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
A student shall be deemed eligible to sit for a summative examination provided that the requisite attendance threshold, as stipulated in Article 12.3, has been satisfied or formally condoned pursuant to the Medical Absence Provision. Attendance condonation shall require submission of a contemporaneous medical certificate to the Office of Academic Affairs within ten (10) calendar days of the initial absence, together with a written request for intermittent academic accommodation signed by the Head of the Department. Upon verification of the documentation, the Registrar may grant a conditional exemption from the attendance requirement, thereby authorising the
```

Call 2: groq / openai/gpt-oss-120b

```text
Yes, you can request a make‑up exam by applying to the
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Yes, you can request a make\u2011up exam by applying to the"
  }
]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.7979430556297302; RRF None

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

Rank 2; chunk `5f65583cd8f796ad54c50d02537940883d487b4d76540d1ae0e83e6aa389df11`; page(s) [11]; cosine 0.7518724799156189; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days.
B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam.
B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination. B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately. B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc. Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam.
```

Exact answer excerpt (if selected):
```text
B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately.
```

Rank 3; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.7407485842704773; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `70985cd4d545e5278d4e5d4f87125207a2fdc5b38859c5d84fbc7962c651ef7c`; page(s) [12]; cosine 0.7297044992446899; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B16. Re-examination (Amended in 23rd Senate meeting)
exam cell of the Institute. They will be conducted within fifteen days from the declaration of the ODD or EVEN semester results. Re-examination will be offered only if there is at least one student failed in any course pertaining to respective semester.
B16.2 In case of prolonged illness of a student, if he/she misses both the end term examination and its re-examination, the student must register for the course(s) as a backlog paper when it is offered.
B16.3 The re-examination shall be held on dates laid down in the Academic Calendar or as notified separately.
B16.4 The re-examination will be conducted for the End term exam component only [while the marks of minor and mid evaluation component will be retained]. The make-up examination for eligible students (if any) may also be conducted in this re-examination slot. The student will be awarded a grade as per the grading criteria followed for the course during the semester. The result will be published within a week from the last examination.
B16.5 Students intending to appear in re-examination must submit their application in the prescribed format to the concerned HoD within five days after publication of the results of the respective semester.
B16.6 The highest grade that can be awarded in re-examination is ‘P’ (Pass).
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
    "hyde": 977.2,
    "embed": 42.8,
    "retrieve": 3.4,
    "total": 2512.9,
    "answer": 1371.8
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 977.0112037658691,
      "input_tokens": 250,
      "output_tokens": 200,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1369.5189952850342,
      "input_tokens": 694,
      "output_tokens": 350,
      "tokens_estimated_before": 2071,
      "tokens_estimated_after": 711
    }
  },
  "warnings": [],
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
Yes—you may request a make‑up exam
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "Yes\u2014you may request a make\u2011up exam"
  }
]
```

### Retrieved evidence

Rank 1; chunk `fc0f228bc6d373fa1831a4b989c3620e3938fff5d7e6c12057da81ebd9fdf675`; page(s) [11]; cosine 0.6659157872200012; RRF None

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

Rank 2; chunk `5d4ede4d4536e66a820d0835ec9d3ef8b07791650aefeecf92d1d0469a9bd4d1`; page(s) [21]; cosine 0.6641040444374084; RRF None

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

Rank 3; chunk `8a3e2367b9d10b556aa852971b1375f57390533a2c1566480c06b2a4d0fd04a6`; page(s) [21]; cosine 0.6556234955787659; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper of the concerned students will be cancelled.
• If the act is repeated for more than once, all the papers in the concerned semester will be cancelled.
• Parents will be informed to report to Dean (Academics) cases of destroying any evidence of malpractice, like tearing or mutilating the answer script(s) or running away along with the answer script(s) from the examination hall or premises
```

Exact answer excerpt (if selected):
```text
• The specific paper of the concerned students will be cancelled.
• If the act is repeated for more than once, all the papers in the concerned semester will be cancelled.
• Parents will be informed to report to Dean (Academics) cases of destroying any evidence of malpractice, like tearing or mutilating the answer script(s) or running away along with the answer script(s) from the examination hall or premises
```

Rank 4; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.6549149751663208; RRF None

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

Rank 5; chunk `0d50ea1c9af6abd2daed533351f444490abf404865c20122825cf8317fd54f2e`; page(s) [22]; cosine 0.6538349986076355; RRF None

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

Timings / usage:
```json
{
  "timings_ms": {
    "cache": 0.0,
    "embed": 11.8,
    "retrieve": 4.0,
    "total": 1387.5,
    "answer": 1306.9
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1304.490089416504,
      "input_tokens": 761,
      "output_tokens": 350,
      "tokens_estimated_before": 1722,
      "tokens_estimated_after": 797
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

The AI provider is rate-limited. Retrying in 4 seconds

### Actual generation and errors

Call 1: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError"
}
```

Call 2: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.6804011464118958; RRF 0.01639344262295082

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

Rank 2; chunk `fc0f228bc6d373fa1831a4b989c3620e3938fff5d7e6c12057da81ebd9fdf675`; page(s) [11]; cosine 0.6001483798027039; RRF 0.016129032258064516

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

Rank 3; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.590642511844635; RRF 0.015625

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `b8079d0f0e8e93cbcb742e3811316f23796d74e53d7e13c5af3813d986e45df2`; page(s) [13]; cosine 0.5776695609092712; RRF 0.015384615384615385

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
    "raw": 16.9,
    "hyde": 4354.1,
    "total": 9852.6
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 4 seconds"
}
```

## ps1-21 / hyde

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-hyde.json](ps1-21-hyde.json)

### Application output

The AI provider is rate-limited. Retrying in 5 seconds

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
A student shall be eligible for medical attendance condonation only when the cumulative attendance record for the relevant course module falls below the prescribed minimum of seventy‑five percent (75 %) but remains above the absolute lower limit of fifty‑five percent (55 %). Condensation of attendance shall be effected upon submission of a duly completed Medical Certification Form, accompanied by the original physician’s attestation, to the Office of the Registrar within ten (10) calendar days following the final day of the documented medical absence. The request shall be reviewed by the Head of the Department, whose written approval, signified on the form, constitutes the sole authority to grant condonation; any submission thereafter shall be deemed inadmissible
```

Call 2: unavailable / unavailable

```text
{
  "error": "ProviderUnavailableError"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.8154832124710083; RRF None

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

Rank 2; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.7607181668281555; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `b0900abd64a3e8739d25d76c22f9f583635fa6a25b2f035d477ee3c44d7d6933`; page(s) [14]; cosine 0.7442047595977783; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B22. Declaration of Results
B22.1. The course instructor may allow the students to see the evaluated answer scripts at his/her discretion, as long as this is done before finalization of grades. The time limit fixed for such a disclosure is five days before the last date for receiving grades in the Exam Cell.
B22.2. Two copies of the result sheets for the respective course containing the final grade along with two copies with the absolute marks & grades should be submitted to the concerned DCC.
After finalization of the grades at the DCC meeting, hard and soft copies of consolidated result with a) absolute marks and grades b) only grades, will be forwarded by the HoD to the Exam cell.
A record of the approved consolidated result should be sent by the Exam cell back to the concerned HoDs.
B22.3. The Exam cell must announce the results of all the courses.
B22.4. Once grades are published, changes if any, will be allowed in case of tabulation errors only. A request for re-tabulation can be made by student to the course teacher within 2 days of result publication. A request for changes in grade due to tabulation errors (if any) can be made by the teacher of the course, by forwarding the request through the DCC to Exam cell.
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `5f65583cd8f796ad54c50d02537940883d487b4d76540d1ae0e83e6aa389df11`; page(s) [11]; cosine 0.7436139583587646; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B15. Make-up examination
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days.
B15.4. A student who misses the make-up exam will normally not be given another make-up exam. However, in exceptional cases of prolonged illness resulting in the student missing a make-up exam, the Chairperson of the Senate may permit the student to appear for a second make-up exam.
B15.5. If a make-up exam is requested for end term examination, the highest grade that can be awarded is ‘A’ grade.
B15.1. Students who miss the mid-term or the end-term examinations for valid reasons with due approval from the Institute, serious illness of self or a calamity in the family, are eligible for a make-up examination. B15.2. Those who miss mid-term and/or end-term exam should apply (in person or by email) to the HoD of the concerned course department (in the case of third and higher semesters) or to the first year HoD (in the case of first/second semester) through the faculty advisor within five days after the missed exam, giving the reasons for absence. Applications received after this period will not be entertained. All make-up exams for mid-term test should be completed with evaluation within 10 days prior to the end-term exam. All the make-up exams pertaining to the end-term exam should be conducted and evaluated within the dates as laid down in the academic calendar or as notified separately. B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc. Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam.
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
    "hyde": 735.2,
    "embed": 47.1,
    "retrieve": 3.5,
    "total": 7883.1
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 735.0099086761475,
      "input_tokens": 254,
      "output_tokens": 200,
      "cache_hit": false
    }
  },
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 5 seconds"
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
  "error": "ProviderUnavailableError"
}
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `dc41cb167d47719bb69ca0ce47f8e9511df425a1ffbfab6d4a7900b7adf9a4cc`; page(s) [10]; cosine 0.6804011464118958; RRF None

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

Rank 2; chunk `fc0f228bc6d373fa1831a4b989c3620e3938fff5d7e6c12057da81ebd9fdf675`; page(s) [11]; cosine 0.6001483798027039; RRF None

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

Rank 3; chunk `4be3ead69bf656f3a802d50c31a0cbba87a20eee00beac8b0752a437ad415b9d`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 4; chunk `b8079d0f0e8e93cbcb742e3811316f23796d74e53d7e13c5af3813d986e45df2`; page(s) [13]; cosine 0.5776695609092712; RRF None

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
    "embed": 14.6,
    "retrieve": 4.0,
    "total": 1411.4
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