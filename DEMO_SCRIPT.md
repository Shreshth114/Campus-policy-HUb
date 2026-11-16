# Campus Policy Intelligence — Presenter Demonstration Script

**Target Duration:** 4 to 5 minutes  
**Target Audience:** Technical interviewers & evaluators (Dell Technologies)  
**Core Themes:** HyDE retrieval accuracy vs Raw, structural guardrails, deterministic policy intelligence, dual trust architecture.  
**Notice:** All fixtures shown during this demo are explicitly **SYNTHETIC TEST FIXTURES** created for reproducibility. No benchmark numbers are claimed without human-verified gold labels.

---

## Preparation (Before Starting)

1. Ensure the server is running on `http://127.0.0.1:8000`:
   ```bash
   cd ps1-policy-assistant
   python -m src.server
   ```
2. Open Chrome/Safari to `http://127.0.0.1:8000`.
3. If no personal workspace is active, click **"Load synthetic demo workspace"** on the Home tab. This immediately populates the browser session with two synthetic test policies (*Synthetic Test Fixture A* and *Synthetic Test Fixture B*).

---

## Minute-by-Minute Script

### [0:00 – 0:45] Act 1: The Problem & The Student-First Platform

**Action:** Open `Home` (`#view-home`). Point to the hero headline: *"Understand your college rules. Know your options."*

**Presenter Script:**
> "Welcome. University academic regulations are notorious for two problems:
> 1. **Vocabulary mismatch:** Students ask natural, casual questions like *'Can I write exams if I had a medical issue?'*, whereas official regulations use legalistic terms like *'attendance condonation upon certification approved by the Head of Department'*.
> 2. **Hallucination risk in RAG:** Traditional RAG often hallucinates permissions or mixes unverified student uploads with authoritative college policies.
>
> To solve this, we built **Campus Policy Intelligence**. It is a student-first platform. Notice that on Home, a student can drop their own college PDFs directly into an anonymous personal capability workspace with zero institutional sign-in required. Everything is scoped locally using 256-bit anonymous tokens."

---

### [0:45 – 1:45] Act 2: Three-Way Retrieval Comparison (Raw vs HyDE vs Fusion)

**Action:** Click **"Advanced ▾"** in the top navigation, select **"Compare Retrieval"** (`#view-compare`).  
Enter or use the pre-filled question:  
`"What are the attendance requirements?"`  
Click **"Compare"**.

**Presenter Script:**
> "Here is our core technical contribution: a live, side-by-side three-way comparison between Raw Search, HyDE Search, and Reciprocal Rank Fusion.
>
> 1. **Column 1 — Raw Query Search:** Directly embeds the user's brief casual question using our local FastEmbed model (`bge-small-en-v1.5`, 384 dimensions). It scores chunks purely on keyword/semantic overlap with the short query.
>
> 2. **Column 2 — HyDE Search:** Uses Groq to generate a hypothetical handbook excerpt written in dense, regulatory language. Look at the generated passage: it includes phrases like *'prescribed attendance quota... documented contemporaneous register'*. This hypothetical passage is embedded and searched against our ChromaDB collection. Notice how it surfaces highly formal passages that raw query keywords might under-score.
>
> 3. **Column 3 — Fusion Ranking (RRF):** Merges both result lists using Reciprocal Rank Fusion.
>
> **CRITICAL ARCHITECTURAL GUARD:** Look at the scores in the Fusion column. We report the RRF rank score (`0.033`) separately from the true Cosine Similarity (`0.731`). We never conflate RRF with cosine confidence. Most importantly: the generated HyDE text is structurally isolated—it is used *only* as an embedding vector key and is **never** passed into answer generation."

---

### [1:45 – 2:30] Act 3: Grounded Answers, Guardrails & Quote Verification

**Action:** Click **"Ask & Analyse"** (`#view-analysis`) or ask a question from Home:  
`"What attendance percentage is required?"`  
Click **"Ask question"**.

**Presenter Script:**
> "When the answer generates, notice the multi-tier guardrails in action:
> 1. **Confidence Gate:** Every chunk is evaluated against our cosine confidence threshold (`0.35`). If evidence is weak or absent, the system immediately abstains instead of inventing policies.
> 2. **Citation Verification:** Every claim is explicitly tagged with `[C1]`, `[C2]`. Python validates that every citation maps to an actual retrieved chunk.
> 3. **Quote Verification:** Look at the exact quotations. Our backend verifies that every quotation is an exact contiguous substring of the cited source. If an LLM hallucinates an altered quote or attributes it to the wrong document, the guardrail rejects it.
> 4. **Dual Trust Banner:** At the bottom, notice the explicit trust banner: *'Answers are based on documents you uploaded. They have not been verified by your institution.'* There is zero confusion between personal uploads and verified college data."

---

### [2:30 – 3:15] Act 4: Rule Book & Deterministic Fact Analysis

**Action:** Click **"Rule Book"** (`#view-rulebook`). Show the extracted numerical rules.  
Then click **"Ask & Analyse"** (`#view-analysis`), enter:  
`"I have 78% attendance"`  
Click **"Parse my facts"**, then click **"Confirm & analyse"**.

**Presenter Script:**
> "Most LLM systems fail when asked: *'Am I eligible?'* because language models are unreliable at arithmetic and conditional logic.
>
> We enforce an ironclad principle: **The model extracts; deterministic code decides.**
>
> 1. In the **Rule Book**, the LLM extracts explicit numerical thresholds (e.g., Attendance `>= 75%` or `>= 80%`), bound to exact verbatim quotes.
> 2. In **Ask & Analyse**, when a student states *'I have 78% attendance'*, the student confirms the fact in the UI.
> 3. The actual eligibility evaluation runs entirely in Python using `decimal.Decimal` comparisons.
> 4. If attendance meets the 75% rule, it marks it satisfied; if another document requires 80%, it flags it. If facts or units are missing, it returns *'insufficient evidence'* rather than guessing. The LLM can generate an explanatory summary, but it cannot alter the computed verdict."

---

### [3:15 – 3:45] Act 5: Policy Conflicts & Document Version Changes

**Action:** Click **"Policy Conflicts"** (`#view-conflicts`), then click **"Document Changes"** (`#view-changes`).

**Presenter Script:**
> "Students often suffer when multiple campus documents contradict each other—for example, a Department handbook requiring 80% attendance while the General Regulations state 75%.
>
> 1. In **Policy Conflicts**, the system groups rules by subject and highlights cross-document discrepancies with verbatim source quotes and page numbers. We intentionally do not pick an arbitrary winner based on publication dates; we show the student both rules so they know what to clarify with their Dean.
> 2. In **Document Changes**, students can compare two versions of the same regulation side by side to see exactly what clauses were added, modified, or removed."

---

### [3:45 – 4:15] Act 6: Labels & Benchmark Honesty

**Action:** Click **"Label Queries"** (`#view-labels`), then click **"Benchmark"** (`#view-bench`).

**Presenter Script:**
> "Evaluation honesty is central to our engineering ethics:
> 1. In **Label Queries**, our tool proposes candidate student queries, but every candidate is marked **UNVERIFIED**.
> 2. A human evaluator must explicitly click to verify gold chunk IDs.
> 3. In the **Benchmark** tab, we refuse to fabricate retrieval accuracy metrics. If labels are unverified, the dashboard honestly states that benchmarks are pending human verification rather than displaying mock 95% scores."

---

### [4:15 – 4:45] Act 7: Architecture Walkthrough & Safe Abstention

**Action:** Click **"How it works"** (`#view-how`), pointing to the SVG architecture diagram.  
Demonstrate safe abstention by asking:  
`"What is the melting point of tungsten?"`

**Presenter Script:**
> "Finally, on the **How it works** tab, you can inspect the full pipeline: local PyMuPDF extraction, word-safe chunking, local FastEmbed dense representations, partitioned ChromaDB storage, HyDE structural isolation, and deterministic rule evaluation.
>
> Watch what happens when we ask an out-of-scope question like *'What is the melting point of tungsten?'*:
> The cosine similarity falls below the 0.35 confidence threshold, and the system cleanly abstains:
> *'I couldn't find a policy that covers this. Please contact the Department office or Academic section for clarification.'*
> Zero hallucinations. Complete source grounding.
>
> Thank you, and I look forward to your questions."

---

## Troubleshooting & Demo Fallbacks

- **If LLM API times out:** Caching is active! Repeated queries on synthetic fixtures return instantly from the local JSON cache.
- **To reset demo state:** Click **"Delete my personal workspace"** on Home, then click **"Load synthetic demo workspace"** to start fresh in 2 seconds.

