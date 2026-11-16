# Actual PS1 diagnostic execution

Run status: completed

Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.

| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |
|---|---|---|---|---|---:|---:|
| ps1-02 | fusion | answered | — | groq/openai/gpt-oss-120b | 4 | 8.15 |
| ps1-02 | hyde | answered | — | groq/openai/gpt-oss-120b | 5 | 2.12 |
| ps1-02 | raw | answered | — | groq/openai/gpt-oss-120b | 4 | 0.86 |
| ps1-14 | fusion | abstained | quote_verification_failed | groq/openai/gpt-oss-120b | 5 | 1.98 |
| ps1-14 | hyde | answered | — | groq/openai/gpt-oss-120b | 5 | 7.05 |
| ps1-14 | raw | answered | — | groq/openai/gpt-oss-120b | 5 | 2.83 |
| ps1-21 | fusion | answered | — | groq/openai/gpt-oss-120b | 4 | 3.46 |
| ps1-21 | hyde | answered | — | groq/openai/gpt-oss-120b | 4 | 6.53 |
| ps1-21 | raw | answered | — | groq/openai/gpt-oss-120b | 4 | 2.38 |

## ps1-02 / fusion

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-fusion.json](ps1-02-fusion.json)

### Application output

"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%." [C1]

"Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester." [C1]
"The AAC, depending on the merit of the case may permit the student to appear for the end semester exam." [C1]
"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C1]
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier." [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns the attendance thresholds relevant to medical condonation within the university’s academic regulations. A systematic review of the institutional handbook should locate the section that delineates permissible absence percentages, documentation requirements, and the procedural steps for submitting a medical condonation request. Keywords such as “attendance,” “medical condonation,” and “absence policy” will aid the search.
```

Call 2: groq / openai/gpt-oss-120b

```text
"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%." [C1]
```

### Validator failures

```json
[
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

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.7834295034408569; RRF 0.01639344262295082

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

Rank 2; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.701009213924408; RRF 0.016129032258064516

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.6613121032714844; RRF 0.015873015873015872

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
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days.
```

Rank 4; chunk `0eea2dad6835d4bdc7bb874e03af1f5f3fc626f8341606fefccfef10231d7861`; page(s) [3]; cosine 0.6471104621887207; RRF 0.015384615384615385

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
    "raw": 119.9,
    "hyde": 995.8,
    "total": 8150.4,
    "answer": 6939.0
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 881.9930553436279,
      "input_tokens": 941,
      "output_tokens": 86,
      "finish_reason": "stop",
      "reasoning_tokens": 23,
      "tokens_estimated_before": 2200,
      "tokens_estimated_after": 1078
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
  "error": null
}
```

## ps1-02 / hyde

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-hyde.json](ps1-02-hyde.json)

### Application output

"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%." [C1]

"Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester." [C1]
"The AAC, depending on the merit of the case may permit the student to appear for the end semester exam." [C1]
"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C1]
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier." [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns the quantitative thresholds that govern the application of medical condonation to attendance records. Relevant documentation typically delineates the proportion of permissible absences attributable to documented health conditions, distinguishes between routine class attendance and examination participation, and references the procedural submission of medical evidence. Researchers should consult the institution’s attendance policy and health‑services guidelines for precise criteria.
```

Call 2: groq / openai/gpt-oss-120b

```text
"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%." [C1]
```

### Validator failures

```json
[
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

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.7414027452468872; RRF None

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

Rank 2; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.7009557485580444; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `0eea2dad6835d4bdc7bb874e03af1f5f3fc626f8341606fefccfef10231d7861`; page(s) [3]; cosine 0.6804928779602051; RRF None

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

Rank 4; chunk `63badd5867e360dd36366b9c09eae18483e23578211714475173adc9ad4d041d`; page(s) [21]; cosine 0.6756575107574463; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper will be cancelled.
• Case referred to Disciplinary Committee (DC) • The DC will enquire and submit a report for further actions on the persons involved.
• Parents will be informed to report to Dean (Academics) The cases of Suspected Mal Practice (SMP) observed while valuing the answer scripts or other material: such as insertion of answer sheets, revealing of identity or enclosure, common mistakes in different answer scripts possibly by
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 5; chunk `1b141c40bf7268d1ba7da8115d595ebaaf94d7a40b673f058ee8c0771bcb1e93`; page(s) [19]; cosine 0.6746466755867004; RRF None

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
    "hyde": 1047.3,
    "embed": 95.1,
    "retrieve": 14.2,
    "total": 2119.2,
    "answer": 849.3
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1045.4368591308594,
      "input_tokens": 206,
      "output_tokens": 111,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 841.4990901947021,
      "input_tokens": 758,
      "output_tokens": 78,
      "finish_reason": "stop",
      "reasoning_tokens": 15,
      "tokens_estimated_before": 1974,
      "tokens_estimated_after": 859
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
  "error": null
}
```

## ps1-02 / raw

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-raw.json](ps1-02-raw.json)

### Application output

"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%." [C1]

"Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester." [C1]
"The AAC, depending on the merit of the case may permit the student to appear for the end semester exam." [C1]
"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C1]
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier." [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%." [C1]
```

### Validator failures

```json
[
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

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.7834295034408569; RRF None

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

Rank 2; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.6613121032714844; RRF None

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
B15.3. Permission to appear for make-up exam will be given under exceptional circumstances such as admission to a hospital due to illness or grave family calamities or with appropriate permission, etc.
Students residing in the Hostels should produce a Medical Certificate issued by Institute Medical Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. The application should be routed through and approved by Chief Warden.
Officer (IMO), certifying that he/she was admitted to hospital during the period of exam. Students residing outside the campus must produce a medical certificate from a Registered Medical practitioner and the same should be duly endorsed by parent/guardian and also by IMO, within five days.
```

Rank 4; chunk `0eea2dad6835d4bdc7bb874e03af1f5f3fc626f8341606fefccfef10231d7861`; page(s) [3]; cosine 0.6471104621887207; RRF None

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
    "embed": 86.1,
    "retrieve": 19.3,
    "total": 858.4,
    "answer": 605.1
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 593.8889980316162,
      "input_tokens": 941,
      "output_tokens": 86,
      "finish_reason": "stop",
      "reasoning_tokens": 23,
      "tokens_estimated_before": 2200,
      "tokens_estimated_after": 1078
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
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
A concise academic search query for this scenario might combine terminology related to class absenteeism and examination eligibility. Suggested keywords include: “student illness,” “class attendance deficiency,” “final examination participation,” “academic accommodation for missed coursework,” “policy on absent students writing finals,” and “procedures for requesting exam access after class absence.” This combination targets institutional guidelines addressing attendance shortfalls without implying specific procedural outcomes.
```

Call 2: groq / openai/gpt-oss-120b

```text
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.”  
“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester.”  
“The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.”  
“A student will be eligible for this concession at most in two semesters during the entire degree programme.”  
“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.”【C1】
```

### Validator failures

```json
[
  {
    "reason": "uncited_claim",
    "claim": "\u201cThose who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.\u201d"
  },
  {
    "reason": "uncited_claim",
    "claim": "\u201cApplication for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester.\u201d"
  },
  {
    "reason": "uncited_claim",
    "claim": "\u201cThe AAC, depending on the merit of the case may permit the student to appear for the end semester exam.\u201d"
  },
  {
    "reason": "uncited_claim",
    "claim": "\u201cA student will be eligible for this concession at most in two semesters during the entire degree programme.\u201d"
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%."
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
  }
]
```

### Retrieved evidence

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.7380107641220093; RRF 0.03252247488101534

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

Rank 2; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.7596902251243591; RRF 0.032266458495966696

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `cd1283c85d6c8503bb45850db72bcc2a6805c5dc2eca121071263e67bf639305`; page(s) [21]; cosine 0.7072036862373352; RRF 0.03128054740957967

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

Rank 4; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.7067438960075378; RRF 0.031009615384615385

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

Rank 5; chunk `1b141c40bf7268d1ba7da8115d595ebaaf94d7a40b673f058ee8c0771bcb1e93`; page(s) [19]; cosine 0.7116994261741638; RRF 0.015873015873015872

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
    "raw": 75.0,
    "hyde": 1048.2,
    "total": 1974.6,
    "answer": 772.9
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1006.1070919036865,
      "input_tokens": 230,
      "output_tokens": 120,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 768.2068347930908,
      "input_tokens": 876,
      "output_tokens": 214,
      "finish_reason": "stop",
      "reasoning_tokens": 21,
      "tokens_estimated_before": 1957,
      "tokens_estimated_after": 980
    }
  },
  "warnings": [
    "Quote could not be verified; the proposed answer was withheld."
  ],
  "error": null
}
```

## ps1-14 / hyde

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-hyde.json](ps1-14-hyde.json)

### Application output

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C2]

"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C2]
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier." [C2]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns a student who experienced illness resulting in missed instructional sessions and seeks clarification regarding eligibility to sit for final examinations. The situation involves an attendance deficiency without indication of a missed assessment. Relevant documentation should be consulted to determine procedural options for addressing class absences while preserving the opportunity to complete scheduled final evaluations.
```

Call 2: groq / openai/gpt-oss-120b

```text
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C2]
```

### Validator failures

```json
[
  {
    "reason": "omitted_qualification",
    "source_label": "C2",
    "qualification": "A student will be eligible for this concession at most in two semesters during the entire degree programme."
  },
  {
    "reason": "omitted_qualification",
    "source_label": "C2",
    "qualification": "Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier."
  }
]
```

### Retrieved evidence

Rank 1; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.7432082295417786; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 2; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.7413604259490967; RRF None

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

Rank 3; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.7204734086990356; RRF None

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

Rank 4; chunk `1b141c40bf7268d1ba7da8115d595ebaaf94d7a40b673f058ee8c0771bcb1e93`; page(s) [19]; cosine 0.7180868983268738; RRF None

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

Rank 5; chunk `cd1283c85d6c8503bb45850db72bcc2a6805c5dc2eca121071263e67bf639305`; page(s) [21]; cosine 0.7019745707511902; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > Yes
• The specific paper and subsequent papers will be cancelled.
• Case referred to Disciplinary Committee (DC) • The DC may recommend Year Back • Parents will be informed to report to Dean (Academics) Communicating with any student or any other person inside or outside the examination hall with a view to take assistance or aid to write answers in the examination
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
    "hyde": 892.0,
    "embed": 38.8,
    "retrieve": 4.7,
    "total": 7048.9,
    "answer": 5994.7
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 891.1337852478027,
      "input_tokens": 230,
      "output_tokens": 101,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 795.8950996398926,
      "input_tokens": 952,
      "output_tokens": 149,
      "finish_reason": "stop",
      "reasoning_tokens": 30,
      "tokens_estimated_before": 1957,
      "tokens_estimated_after": 1068
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
  "error": null
}
```

## ps1-14 / raw

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-raw.json](ps1-14-raw.json)

### Application output

"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam." [C1]

"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C1]
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier." [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%. Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam." [C1]
```

### Validator failures

```json
[
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

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.7380107641220093; RRF None

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

Rank 2; chunk `cd1283c85d6c8503bb45850db72bcc2a6805c5dc2eca121071263e67bf639305`; page(s) [21]; cosine 0.7072036862373352; RRF None

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

Rank 3; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.7019397616386414; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `66bf4abd71f3ae0ab76b4912376a830ff6a61a28c38481ad49c3ae0b97d130d7`; page(s) [22]; cosine 0.7018308043479919; RRF None

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

Rank 5; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.7014567852020264; RRF None

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
    "embed": 87.7,
    "retrieve": 14.7,
    "total": 2821.8,
    "answer": 2550.2
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 2542.0310497283936,
      "input_tokens": 876,
      "output_tokens": 130,
      "finish_reason": "stop",
      "reasoning_tokens": 11,
      "tokens_estimated_before": 1849,
      "tokens_estimated_after": 980
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
  "error": null
}
```

## ps1-21 / fusion

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-fusion.json](ps1-21-fusion.json)

### Application output

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]

“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C1]

“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]

"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The handbook outlines two attendance thresholds that trigger medical‑attendance condonation, delineates the procedural steps required for obtaining approval, and specifies the deadline by which a medical‑leave request must be submitted. It distinguishes between routine class absences and absences affecting examination eligibility, and references the documentation and administrative channels necessary for formal consideration.
```

Call 2: groq / openai/gpt-oss-120b

```text
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]

“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C1]

“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]
```

### Validator failures

```json
[
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "A student will be eligible for this concession at most in two semesters during the entire degree programme."
  }
]
```

### Retrieved evidence

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.6804011464118958; RRF 0.01639344262295082

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

Rank 2; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.6001483798027039; RRF 0.016129032258064516

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

Rank 3; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.590642511844635; RRF 0.015625

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `648bdba55f06bd8780de8e39af7f801fbbd3a02f9717460278a0aed8fda59a6e`; page(s) [13]; cosine 0.5776695609092712; RRF 0.015384615384615385

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
    "raw": 40.4,
    "hyde": 771.0,
    "total": 3460.1,
    "answer": 2547.5
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1372.5519180297852,
      "input_tokens": 859,
      "output_tokens": 271,
      "finish_reason": "stop",
      "reasoning_tokens": 93,
      "tokens_estimated_before": 2073,
      "tokens_estimated_after": 962
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
  "error": null
}
```

## ps1-21 / hyde

For medical attendance condonation, explain both attendance thresholds, the approval process and the medical-leave deadline.

Full machine-readable record: [ps1-21-hyde.json](ps1-21-hyde.json)

### Application output

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]

“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester.” [C1]

“The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C1]

“A student will be eligible for this concession at most in two semesters during the entire degree programme.” [C1]

“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
A search query concerning medical attendance condonation may retrieve documents that discuss the dual attendance thresholds applied to regular class participation and to examination eligibility, outline the procedural steps required for obtaining a medical exemption, and specify the temporal parameters within which a medical leave must be submitted. The results typically include institutional guidelines, procedural flowcharts, and relevant deadline notices.
```

Call 2: groq / openai/gpt-oss-120b

```text
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]

“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester.” [C1]

“The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C1]

“A student will be eligible for this concession at most in two semesters during the entire degree programme.” [C1]

“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.6804011464118958; RRF None

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

Rank 2; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.6001483798027039; RRF None

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

Rank 3; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `648bdba55f06bd8780de8e39af7f801fbbd3a02f9717460278a0aed8fda59a6e`; page(s) [13]; cosine 0.5776695609092712; RRF None

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
    "embed": 47.1,
    "retrieve": 6.7,
    "total": 6532.2,
    "hyde": 879.7,
    "answer": 5468.4
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 803.1208515167236,
      "input_tokens": 859,
      "output_tokens": 223,
      "finish_reason": "stop",
      "reasoning_tokens": 18,
      "tokens_estimated_before": 2073,
      "tokens_estimated_after": 962
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

“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]

“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C1]

“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]

"A student will be eligible for this concession at most in two semesters during the entire degree programme." [C1]

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
“Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%.” [C1]

“Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester. The AAC, depending on the merit of the case may permit the student to appear for the end semester exam.” [C1]

“Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.” [C1]
```

### Validator failures

```json
[
  {
    "reason": "omitted_qualification",
    "source_label": "C1",
    "qualification": "A student will be eligible for this concession at most in two semesters during the entire degree programme."
  }
]
```

### Retrieved evidence

Rank 1; chunk `4286f0b507ae041453ab9f53e7e830ecaa1d09084626629667d9025407ae213c`; page(s) [10]; cosine 0.6804011464118958; RRF None

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

Rank 2; chunk `989c18cddce541b081417e6028b5362476bdfed7b9d345051fa71f5ce5f2ba8a`; page(s) [11]; cosine 0.6001483798027039; RRF None

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

Rank 3; chunk `392137f81078f74beec4fd7b2361abe03c7c78095cec4086a79531c5dfeed1d4`; page(s) [15]; cosine 0.590642511844635; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 4; chunk `648bdba55f06bd8780de8e39af7f801fbbd3a02f9717460278a0aed8fda59a6e`; page(s) [13]; cosine 0.5776695609092712; RRF None

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
    "embed": 26.3,
    "retrieve": 4.2,
    "total": 2377.7,
    "answer": 2233.2
  },
  "llm_usage": {
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1370.8961009979248,
      "input_tokens": 859,
      "output_tokens": 271,
      "finish_reason": "stop",
      "reasoning_tokens": 93,
      "tokens_estimated_before": 2073,
      "tokens_estimated_after": 962
    }
  },
  "warnings": [
    "Additional conditions were appended verbatim from the cited source to complete the model response."
  ],
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