# Actual PS1 diagnostic execution

Run status: interrupted_network_unavailable

Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.

| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |
|---|---|---|---|---|---:|---:|
| ps1-02 | hyde | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 4 | 8.86 |
| ps1-02 | raw | provider_unavailable | The AI provider is rate-limited. Retrying in 15 seconds | / | 4 | 4.67 |

## ps1-02 / hyde

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-hyde.json](ps1-02-hyde.json)

### Application output

The AI provider is rate-limited. Retrying in 15 seconds

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

Rank 1; chunk `56d8696d51ead897547763bcc2cb996e741b700bab17e7200ab99b56b430cb5f`; page(s) [10]; cosine 0.7834295034408569; RRF None

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

Rank 2; chunk `4fea09661eece7513416e06a77ad1412526f2a356bca5bde65d4f22c2bac82d7`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `c6b64461fe3de3622e506c93a92727fe9c19015c07ce15072734df0a3ac8340e`; page(s) [11]; cosine 0.6613121032714844; RRF None

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

Rank 4; chunk `9570783cf3569dd59301c6ecad583a694c4ed397b3cc24b7e7eeb7820705601f`; page(s) [3]; cosine 0.6471104621887207; RRF None

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
    "embed": 55.4,
    "retrieve": 9.9,
    "total": 8861.8,
    "hyde": 4523.2
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## ps1-02 / raw

What attendance levels apply to medical condonation?

Full machine-readable record: [ps1-02-raw.json](ps1-02-raw.json)

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

Rank 1; chunk `56d8696d51ead897547763bcc2cb996e741b700bab17e7200ab99b56b430cb5f`; page(s) [10]; cosine 0.7834295034408569; RRF None

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

Rank 2; chunk `4fea09661eece7513416e06a77ad1412526f2a356bca5bde65d4f22c2bac82d7`; page(s) [15]; cosine 0.701009213924408; RRF None

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
[not selected / not sent]
```

Rank 3; chunk `c6b64461fe3de3622e506c93a92727fe9c19015c07ce15072734df0a3ac8340e`; page(s) [11]; cosine 0.6613121032714844; RRF None

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

Rank 4; chunk `9570783cf3569dd59301c6ecad583a694c4ed397b3cc24b7e7eeb7820705601f`; page(s) [3]; cosine 0.6471104621887207; RRF None

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
    "embed": 6.1,
    "retrieve": 5.3,
    "total": 4665.1
  },
  "llm_usage": {},
  "warnings": [],
  "error": "The AI provider is rate-limited. Retrying in 15 seconds"
}
```

## Production integrity

```json
{
  "comparison_baseline": "snapshot from scripted-results removal, earlier in this conversation",
  "files_checked": 244,
  "byte_identical": true
}
```