# Actual PS1 diagnostic execution

Run status: completed

Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.

| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |
|---|---|---|---|---|---:|---:|
| ps1-14 | fusion | answered | — | groq/openai/gpt-oss-120b | 5 | 3.98 |

## ps1-14 / fusion

I was sick and missed classes. Is there a way to still write my finals?

Full machine-readable record: [ps1-14-fusion.json](ps1-14-fusion.json)

### Application output

"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%" [C1].  
"Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester" [C1].  
"The AAC, depending on the merit of the case may permit the student to appear for the end semester exam" [C1].  
"A student will be eligible for this concession at most in two semesters during the entire degree programme" [C1].  
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier" [C1].

### Actual generation and errors

Call 1: groq / openai/gpt-oss-120b

```text
The inquiry concerns a student who experienced illness resulting in non‑attendance during instructional sessions, without indication of a missed assessment. The focus is on determining whether institutional provisions exist that permit participation in scheduled final examinations despite documented class absences. Relevant considerations include documented medical evidence, attendance records, and procedural mechanisms for requesting examination eligibility under such circumstances.
```

Call 2: groq / openai/gpt-oss-120b

```text
"Those who have 80% or more attendance for the period other than their medical leave will be considered for condonation of shortage of attendance, provided, the overall attendance in the course including the period of illness does not fall below 75%" [C1].  
"Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester" [C1].  
"The AAC, depending on the merit of the case may permit the student to appear for the end semester exam" [C1].  
"A student will be eligible for this concession at most in two semesters during the entire degree programme" [C1].  
"Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier" [C1].
```

### Validator failures

```json
[]
```

### Retrieved evidence

Rank 1; chunk `738f1a48edbd9e73b88d173dd1df5bcbc56a824787c80dce766c89905d5447b2`; page(s) [10]; cosine 0.7732698917388916; RRF 0.03278688524590164

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

Rank 2; chunk `910120c5809774aab0016e2e828ab8a6ede2af5dcaa5e88c08ae4504f5ca4fa5`; page(s) [15]; cosine 0.7543956637382507; RRF 0.03200204813108039

```text
Btech (Rules & Regulations)2013 21Nov2023 > B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Exact answer excerpt (if selected):
```text
B25.1. Due to unsatisfactory academic performance
If a student exceeds more than 12 regular semesters from the date of first registration, excluding those semesters in which drop was taken on medical ground or for valid reason beyond control of the student. If this condition is met then the case will be referred to the Academic Advisory Committee (AAC).
```

Rank 3; chunk `fa63463767dc75916a091e42c004b51b84233c802ed0976b1907837f75d82be7`; page(s) [21]; cosine 0.717210054397583; RRF 0.03128054740957967

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

Rank 4; chunk `e6034d465cf6d0d7b41b44a8b4b5840d9242f98747dba0a941a55c420e8060c7`; page(s) [11]; cosine 0.7240833640098572; RRF 0.03125763125763126

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

Rank 5; chunk `6326a40876fa4dc9b5255d5988882a1e3bc15fc5c605c626f27580ee94d8453a`; page(s) [21]; cosine 0.7188817858695984; RRF 0.030090497737556562

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
    "raw": 27.0,
    "hyde": 1890.7,
    "total": 3975.0,
    "answer": 1981.4
  },
  "llm_usage": {
    "hyde": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1849.6201038360596,
      "input_tokens": 230,
      "output_tokens": 107,
      "cache_hit": false
    },
    "answer": {
      "provider": "groq",
      "model": "openai/gpt-oss-120b",
      "latency_ms": 1972.9957580566406,
      "input_tokens": 949,
      "output_tokens": 296,
      "finish_reason": "stop",
      "reasoning_tokens": 88,
      "tokens_estimated_before": 2003,
      "tokens_estimated_after": 1068
    }
  },
  "warnings": [],
  "error": null
}
```

## Production integrity

```json
{
  "files_checked": 237,
  "byte_identical": true
}
```