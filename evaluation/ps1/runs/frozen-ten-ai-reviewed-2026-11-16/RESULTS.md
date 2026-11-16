# Exploratory frozen-set execution results

Labels: AI-assisted review, **not human verified**. No semantic accuracy claim. All ten questions were frozen before this run; after inspection they are no longer an untouched set for further tuning.

| Case | Mode | Decision/reason | Group recall@3 | Raw exact-span coverage | Final exact-span coverage | Fallback | Supplement |
|---|---|---|---|---|---|---|---|
| fresh-01 | fusion | abstained/no_policy_found | 0.0 | 0.0 | 0.0 | False | False |
| fresh-01 | hyde | abstained/no_policy_found | 1.0 | 0.0 | 0.0 | True | False |
| fresh-01 | raw | abstained/no_policy_found | 1.0 | 0.0 | 0.0 | False | False |
| fresh-02 | fusion | abstained/quote_verification_failed | 1.0 | 0.5 | 0.0 | True | False |
| fresh-02 | hyde | abstained/no_policy_found | 0.0 | 0.0 | 0.0 | False | False |
| fresh-02 | raw | abstained/quote_verification_failed | 1.0 | 0.5 | 0.0 | False | False |
| fresh-03 | fusion | answered/— | 0.0 | 0.0 | 0.0 | False | True |
| fresh-03 | hyde | abstained/no_policy_found | 0.0 | 0.0 | 0.0 | False | False |
| fresh-03 | raw | abstained/quote_verification_failed | 0.0 | 0.0 | 0.0 | False | False |
| fresh-04 | fusion | abstained/quote_verification_failed | unscored: mapping incomplete | 0.5 | 0.0 | False | False |
| fresh-04 | hyde | abstained/quote_verification_failed | unscored: mapping incomplete | 0.5 | 0.0 | False | False |
| fresh-04 | raw | answered/— | unscored: mapping incomplete | 0.5 | 1.0 | False | True |
| fresh-05 | fusion | abstained/unsupported_cited_claim | 1.0 | 1.0 | 0.0 | True | False |
| fresh-05 | hyde | answered/— | 1.0 | 1.0 | 1.0 | False | True |
| fresh-05 | raw | abstained/unsupported_cited_claim | 1.0 | 1.0 | 0.0 | False | False |
| fresh-06 | fusion | abstained/no_policy_found | 1.0 | 0.0 | 0.0 | False | False |
| fresh-06 | hyde | abstained/no_policy_found | 1.0 | 0.0 | 0.0 | True | False |
| fresh-06 | raw | answered/— | 1.0 | 0.3333333333333333 | 0.3333333333333333 | False | True |
| fresh-07 | fusion | answered/— | unscored: mapping incomplete | 1.0 | 1.0 | False | False |
| fresh-07 | hyde | answered/— | unscored: mapping incomplete | 1.0 | 1.0 | False | True |
| fresh-07 | raw | answered/— | unscored: mapping incomplete | 1.0 | 1.0 | False | True |
| fresh-08 | fusion | answered/— | 1.0 | 1.0 | 1.0 | True | True |
| fresh-08 | hyde | answered/— | 1.0 | 1.0 | 1.0 | True | True |
| fresh-08 | raw | answered/— | 1.0 | 1.0 | 1.0 | False | True |
| fresh-09 | fusion | clarification_required/— | None | None | None | False | False |
| fresh-09 | hyde | clarification_required/— | None | None | None | False | False |
| fresh-09 | raw | clarification_required/— | None | None | None | False | False |
| fresh-10 | fusion | abstained/no_policy_found | None | None | None | True | False |
| fresh-10 | hyde | abstained/no_policy_found | None | None | None | True | False |
| fresh-10 | raw | abstained/no_policy_found | None | None | None | False | False |

Exploratory genuine-mode retrieval aggregates (AI-reviewed relevance only; excluded fallbacks/unmapped cases):
```json
{
  "raw": {
    "service_attempts": 10,
    "accepted": 4,
    "genuine_mapped_quality_cases": 6,
    "source_group_recall_at_k": {
      "1": 0.5,
      "3": 0.8333333333333334,
      "5": 0.8333333333333334
    },
    "mrr_first_relevant": 0.6388888888888888,
    "semantic_accuracy": null
  },
  "hyde": {
    "service_attempts": 10,
    "accepted": 3,
    "genuine_mapped_quality_cases": 3,
    "source_group_recall_at_k": {
      "1": 0.3333333333333333,
      "3": 0.3333333333333333,
      "5": 0.3333333333333333
    },
    "mrr_first_relevant": 0.3333333333333333,
    "semantic_accuracy": null
  },
  "fusion": {
    "service_attempts": 10,
    "accepted": 3,
    "genuine_mapped_quality_cases": 3,
    "source_group_recall_at_k": {
      "1": 0.3333333333333333,
      "3": 0.3333333333333333,
      "5": 0.6666666666666666
    },
    "mrr_first_relevant": 0.4,
    "semantic_accuracy": null
  }
}
```

Per-mode aggregates use different eligible subsets and must not be compared directly. Same-case genuine Raw/HyDE pairs:
```json
{
  "pairs": [
    {
      "id": "fresh-02",
      "raw_rr": 1.0,
      "hyde_rr": 0,
      "outcome": "loss"
    },
    {
      "id": "fresh-03",
      "raw_rr": 0,
      "hyde_rr": 0,
      "outcome": "tie"
    },
    {
      "id": "fresh-05",
      "raw_rr": 1.0,
      "hyde_rr": 1.0,
      "outcome": "tie"
    }
  ],
  "n": 3,
  "wins": 0,
  "ties": 2,
  "losses": 1
}
```

Exact-span coverage is deliberately literal; it measures inclusion of rubric phrases, not whether paraphrases are correct or the answer is safe. Application acceptance is not human correctness. Complete evidence groups and alternatives are in evidence_mapping.json. No verified labels were written.

## Per-mode service observations

- raw: 10 recorded; accepted 4; fallback 0; source-completed 4; median request seconds 0.9639178749930579; observed p95 seconds 1.640621500002453 (small sample).

- hyde: 10 recorded; accepted 3; fallback 4; source-completed 3; median request seconds 4.684515604007174; observed p95 seconds 9.645997209008783 (small sample).

- fusion: 10 recorded; accepted 3; fallback 4; source-completed 2; median request seconds 5.145150416487013; observed p95 seconds 95.63591466701473 (small sample).

## Human grading still required

Review every raw/final answer against the frozen rubric for correct meaning, all qualifications, no invented claims, appropriate abstention, and citations. Blind mode identity where feasible. No automatic checker substitutes for that judgment. Exclude provider/local quota failures from semantic abstention grading but report them in service coverage. Review errors and unmapped groups rather than silently dropping cases.

## Full outputs

### fresh-01 / fusion

I want to count an elective from another approved institute. What documents must I provide and who approves the credits?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-01-fusion.json](fresh-01-fusion.json)

### fresh-01 / hyde

I want to count an elective from another approved institute. What documents must I provide and who approves the credits?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-01-hyde.json](fresh-01-hyde.json)

### fresh-01 / raw

I want to count an elective from another approved institute. What documents must I provide and who approves the credits?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-01-raw.json](fresh-01-raw.json)

### fresh-02 / fusion

Is an outside institute's grade included in my CGPA, or do only the credits transfer?

Raw model answer:
```text
"The credits transferred will not be used for SGPA/CGPA computations." [C1]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-02-fusion.json](fresh-02-fusion.json)

### fresh-02 / hyde

Is an outside institute's grade included in my CGPA, or do only the credits transfer?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-02-hyde.json](fresh-02-hyde.json)

### fresh-02 / raw

Is an outside institute's grade included in my CGPA, or do only the credits transfer?

Raw model answer:
```text
"The credits transferred will not be used for SGPA/CGPA computations." [C1]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-02-raw.json](fresh-02-raw.json)

### fresh-03 / fusion

After returning from a semester break, who decides which courses I register for?

Raw model answer:
```text
"Students are required to submit course registration form duly filled, in consultation with their faculty advisor." [C2]
```

Final application answer:
```text
"Students are required to submit course registration form duly filled, in consultation with their faculty advisor." [C2]

"v) Registration rules for students with backlog courses: vi) All the provisions of B25 (termination of registration) will be applicable and have to be checked before course registration." [C2]
```

Full source/prompt/score record: [fresh-03-fusion.json](fresh-03-fusion.json)

### fresh-03 / hyde

After returning from a semester break, who decides which courses I register for?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-03-hyde.json](fresh-03-hyde.json)

### fresh-03 / raw

After returning from a semester break, who decides which courses I register for?

Raw model answer:
```text
"The first semester course registration will be carried out by the Institute and hence no separate registration by the students will be required." [C1]  
"Students in the second and higher semesters are required to register for courses in accordance with the semester‑wise published course schedule at the beginning of the corresponding semester. Students are required to submit course registration form duly filled, in consultation with their faculty advisor." [C1]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-03-raw.json](fresh-03-raw.json)

### fresh-04 / fusion

Can I request a re-exam if nobody failed the course?

Raw model answer:
```text
"The re‑examination will be offered only if there is at least one student failed in any course pertaining to respective semester." [C2]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-04-fusion.json](fresh-04-fusion.json)

### fresh-04 / hyde

Can I request a re-exam if nobody failed the course?

Raw model answer:
```text
"The re-examination will be offered only if there is at least one student failed in any course pertaining to respective semester." [C2]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-04-hyde.json](fresh-04-hyde.json)

### fresh-04 / raw

Can I request a re-exam if nobody failed the course?

Raw model answer:
```text
"Re-examination will be offered only if there is at least one student failed in any course pertaining to respective semester." [C1]
```

Final application answer:
```text
"Re-examination will be offered only if there is at least one student failed in any course pertaining to respective semester." [C1]

"They will be conducted within fifteen days from the declaration of the ODD or EVEN semester results." [C1]
"B16.4 The re-examination will be conducted for the End term exam component only [while the marks of minor and mid evaluation component will be retained]." [C1]
"The make-up examination for eligible students (if any) may also be conducted in this re-examination slot." [C1]
"The result will be published within a week from the last examination." [C1]
"B16.5 Students intending to appear in re-examination must submit their application in the prescribed format to the concerned HoD within five days after publication of the results of the respective semester." [C1]
```

Full source/prompt/score record: [fresh-04-raw.json](fresh-04-raw.json)

### fresh-05 / fusion

If my college allows an exam calculator, does that also allow a calculator with communication features?

Raw model answer:
```text
"While normal scientific calculators are permitted during exam, other electronic devices such as programmable calculators, calculators containing communication devices, smart watches and mobile phones are strictly prohibited to examinations." [C1] "Any exception to these provisions must be specially approved by the Senate." [C1]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-05-fusion.json](fresh-05-fusion.json)

### fresh-05 / hyde

If my college allows an exam calculator, does that also allow a calculator with communication features?

Raw model answer:
```text
"While normal scientific calculators are permitted during exam, other electronic devices such as programmable calculators, calculators containing communication devices, smart watches and mobile phones are strictly prohibited to examinations" [C1]. "Any exception to these provisions must be specially approved by the Senate" [C1].
```

Final application answer:
```text
"While normal scientific calculators are permitted during exam, other electronic devices such as programmable calculators, calculators containing communication devices, smart watches and mobile phones are strictly prohibited to examinations" [C1]. "Any exception to these provisions must be specially approved by the Senate" [C1].

"B14.2 All necessary charts & tables required in the exam will be provided by the Institute." [C1]
```

Full source/prompt/score record: [fresh-05-hyde.json](fresh-05-hyde.json)

### fresh-05 / raw

If my college allows an exam calculator, does that also allow a calculator with communication features?

Raw model answer:
```text
"While normal scientific calculators are permitted during exam, other electronic devices such as programmable calculators, calculators containing communication devices, smart watches and mobile phones are strictly prohibited to examinations." [C1] "Any exception to these provisions must be specially approved by the Senate." [C1]
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-05-raw.json](fresh-05-raw.json)

### fresh-06 / fusion

Will passing every summer subject let me ignore the summer registration deadline and fee?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-06-fusion.json](fresh-06-fusion.json)

### fresh-06 / hyde

Will passing every summer subject let me ignore the summer registration deadline and fee?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-06-hyde.json](fresh-06-hyde.json)

### fresh-06 / raw

Will passing every summer subject let me ignore the summer registration deadline and fee?

Raw model answer:
```text
"A student will have to register within the time stipulated in the announcement by paying the prescribed fees." [C1]
```

Final application answer:
```text
"A student will have to register within the time stipulated in the announcement by paying the prescribed fees." [C1]

"Summer term courses will be announced by the AAC after the publication of results of the even semester, if a minimum of 20% of the total registered regular students fail in a course." [C1]
"A summer term course may be offered by a department on the recommendation of the CC/DCC and with the approval of the AAC." [C1]
```

Full source/prompt/score record: [fresh-06-raw.json](fresh-06-raw.json)

### fresh-07 / fusion

Does a W grade count differently from F in calculating CGPA?

Raw model answer:
```text
“A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation, and the following criteria, in addition to poor attendance (less than 80%) may be considered for” [C1]
```

Final application answer:
```text
“A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation, and the following criteria, in addition to poor attendance (less than 80%) may be considered for” [C1]
```

Full source/prompt/score record: [fresh-07-fusion.json](fresh-07-fusion.json)

### fresh-07 / hyde

Does a W grade count differently from F in calculating CGPA?

Raw model answer:
```text
“A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation” [C1].
```

Final application answer:
```text
“A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation” [C1].

"A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation, and the following criteria, in addition to poor attendance (less than 80%) may be considered for (i) badly incomplete in-semester record (due to non-medical reasons), (ii) misconduct or use of unfair means in the examination, assignments, etc., or a behavior serious enough to call for disciplinary action in the opinion of the Faculty advisor or teacher of a course." [C1]
"Further, the case may be referred to the DC for consideration of further punishment depending on the seriousness of the offence." [C1]
```

Full source/prompt/score record: [fresh-07-hyde.json](fresh-07-hyde.json)

### fresh-07 / raw

Does a W grade count differently from F in calculating CGPA?

Raw model answer:
```text
“A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation” [C1]
```

Final application answer:
```text
“A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation” [C1]

"A ‘W’ grade is treated as equivalent to ‘F’ for the purpose of CGPA calculation, and the following criteria, in addition to poor attendance (less than 80%) may be considered for (i) badly incomplete in-semester record (due to non-medical reasons), (ii) misconduct or use of unfair means in the examination, assignments, etc., or a behavior serious enough to call for disciplinary action in the opinion of the Faculty advisor or teacher of a course." [C1]
"Further, the case may be referred to the DC for consideration of further punishment depending on the seriousness of the offence." [C1]
```

Full source/prompt/score record: [fresh-07-raw.json](fresh-07-raw.json)

### fresh-08 / fusion

How is CGPA converted into percentage under this document?

Raw model answer:
```text
"Percentage = (CGPA - 0.5) × 10." [C1]
```

Final application answer:
```text
"Percentage = (CGPA - 0.5) × 10." [C1]

"∑C Where, the summation is taken for all the courses registered for by the student except Pass/Fail courses, up to and including the current semester and the summer terms." [C1]
"Where, ‘C’ is the credit of the registered course and the summation is taken over all the registered courses by the student in the semester, except Pass/Fail courses." [C1]
```

Full source/prompt/score record: [fresh-08-fusion.json](fresh-08-fusion.json)

### fresh-08 / hyde

How is CGPA converted into percentage under this document?

Raw model answer:
```text
"Percentage = (CGPA - 0.5) × 10." [C1]
```

Final application answer:
```text
"Percentage = (CGPA - 0.5) × 10." [C1]

"∑C Where, the summation is taken for all the courses registered for by the student except Pass/Fail courses, up to and including the current semester and the summer terms." [C1]
"Where, ‘C’ is the credit of the registered course and the summation is taken over all the registered courses by the student in the semester, except Pass/Fail courses." [C1]
```

Full source/prompt/score record: [fresh-08-hyde.json](fresh-08-hyde.json)

### fresh-08 / raw

How is CGPA converted into percentage under this document?

Raw model answer:
```text
"Percentage = (CGPA - 0.5) × 10." [C1]
```

Final application answer:
```text
"Percentage = (CGPA - 0.5) × 10." [C1]

"∑C Where, the summation is taken for all the courses registered for by the student except Pass/Fail courses, up to and including the current semester and the summer terms." [C1]
"Where, ‘C’ is the credit of the registered course and the summation is taken over all the registered courses by the student in the semester, except Pass/Fail courses." [C1]
```

Full source/prompt/score record: [fresh-08-raw.json](fresh-08-raw.json)

### fresh-09 / fusion

Has my professor personally approved my medical leave this morning?

Raw model answer:
```text
[generation not called]
```

Final application answer:
```text
Did you miss classes, an examination, or both?
```

Full source/prompt/score record: [fresh-09-fusion.json](fresh-09-fusion.json)

### fresh-09 / hyde

Has my professor personally approved my medical leave this morning?

Raw model answer:
```text
[generation not called]
```

Final application answer:
```text
Did you miss classes, an examination, or both?
```

Full source/prompt/score record: [fresh-09-hyde.json](fresh-09-hyde.json)

### fresh-09 / raw

Has my professor personally approved my medical leave this morning?

Raw model answer:
```text
[generation not called]
```

Final application answer:
```text
Did you miss classes, an examination, or both?
```

Full source/prompt/score record: [fresh-09-raw.json](fresh-09-raw.json)

### fresh-10 / fusion

Can you confirm tomorrow's exact exam-room allocation for my roll number?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-10-fusion.json](fresh-10-fusion.json)

### fresh-10 / hyde

Can you confirm tomorrow's exact exam-room allocation for my roll number?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-10-hyde.json](fresh-10-hyde.json)

### fresh-10 / raw

Can you confirm tomorrow's exact exam-room allocation for my roll number?

Raw model answer:
```text
NO_POLICY_FOUND
```

Final application answer:
```text
I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.
```

Full source/prompt/score record: [fresh-10-raw.json](fresh-10-raw.json)