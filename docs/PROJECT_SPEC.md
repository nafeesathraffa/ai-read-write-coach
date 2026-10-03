# PROJECT SPEC

## 1. Overview

**What the application does**
The learner does their own speaking, writing, and reading. The app gives an activity, takes the learner's own work, evaluates it against a published criterion-specific rubric with evidence quotes drawn from the learner's own text, offers optional revision or a targeted follow-up, and tracks progress on a profile / dashboard.

**Who it's for**
Students, early-career professionals, and self-learners who need clearer thinking on the page and out loud. Demo story: a student who understands a text but cannot explain it, or who freezes when speaking without notes.

**The problem it solves**
Most tools either give passive content or do the work for the learner. Skill comes from producing work, getting criterion-based feedback, revising, and practicing the weak part again. This app enforces that loop and refuses to replace the learner.

---

## 2. Hackathon requirements

**Official rules:** [add link to the official hackathon rules page here. The rules are the source of truth; this section is only a checklist.]

**Track**
Best Apps and Agents.

**Nebius and Nemotron requirement**
At least one NVIDIA open-source model. Intended: Nemotron.

**Judging criteria**

Stage one: Pass/Fail (track, runtime Token Factory inference call; at least one NVIDIA open-source model).

Stage two:
- **Technological Implementation** - Live Token Factory chat.completions with NVIDIA Nemotron; server-side key; schema validation; usage logging. Dual-model split if it earns its place (see §6).
- **Design** - One loop: activity → work → evaluation → revision / follow-up → profile → dashboard. Responsive HTML/CSS. Demo account with real evaluations. Speech with typed fallback. Honest score labels.
- **Potential Impact** - Specific audience above. Improvement shown only after a minimum number of attempts. Original, revision, and follow-up linked.
- **Quality of the Idea** - Evidence-checked evaluation; deterministic metrics from app code; targeted follow-ups; recommendations that cite real attempts; dual-model routing (if kept).

**Other official requirements to satisfy**
- Public source repo with an OSI-approved license (MIT).
- English README explaining setup and how Nemotron / Token Factory / other Nebius tools were used, including where Token Factory accelerated the workflow.
- Working demo URL.
- Public YouTube demo video under 3 minutes, in English (or with translation), no unauthorized copyrighted music or trademarks.
- Feedback on Token Factory / AI Cloud / NVIDIA tools used.
- Project is new or a significant update during the Submission Period.
- Free judge access through 15 December 2026, 12:00 PM PT.
- If login is required, credentials in the testing instructions.
- Original work; complies with third-party licenses; reading passages must not infringe copyright.

---

## 3. User flow

1. **Open the app.** Landing page states what it is, what it is not, and shows the Demo button plus a normal login.
2. **Demo account.** Logs into a pre-seeded account labeled Demo in the UI, containing only real Nemotron evaluations. (How Demo behaves for multiple judges: see Decision log D-05.)
3. **Dashboard.** Per-criterion averages and attempt counts. No overall score. Improvement is shown only after the approved thresholds (§5, Reporting rules).
4. **Pick an activity.** Impromptu Speaking is the MVP path; Writing and Reading follow.
5. **Speaking, topic.** The fast model proposes a topic; if that fails, the hand-written fallback bank is used.
6. **Prepare, then speak.** 60-second preparation timer (default; configurable), then a 60-second speaking timer (default). Transcript via Web Speech API (Chrome / Edge) or typed / pasted fallback.
7. **Metrics.** The app computes word count, WPM, fillers, repeated phrases locally. These are facts, not model output.
8. **Crisis gate.** Broad lexicon trigger first; a separate model check only on a trigger. If flagged, skip scoring, show fixed supportive copy and verified helplines, and redact the stored text.
9. **Evaluation.** Nemotron returns structured JSON against the rubric with evidence quotes from the learner's own text. The app schema-validates and substring-checks every quote. A loading state is shown while waiting (see §6, Latency).
10. **Feedback screen.** Per-criterion score, the learner's own quoted evidence, one improvement suggestion (≤ 400 chars), and app-computed metrics with the transcript caveat.
11. **Optional follow-up.** The app picks target_criterion (lowest score, then relevant history). The model only writes the challenge. After scoring, the app reports whether the criterion improved.
12. **Optional revision (Writing).** Saved as a new attempt with parent_attempt_id. Independently rescored. A separate check reports whether the weakness was addressed.
13. **Profile.** History, per-criterion trends, recommendations from the learning agent (citations validated against the database).

---

## 4. Module scope

Build priority: see §16 (Must have / Should have / Stretch).

**Speaking: Impromptu** *(Must have)*
- Learner does: receives a topic, prepares, speaks, submits the transcript (via speech API or typed fallback).
- Model returns: JSON against speaking_v1, six criterion scores with evidence quotes, one short suggestion.
- App computes: word count, WPM, filler count, repeated phrases.
- Left out: pronunciation, accent, tone, prosody, physical delivery. No audio is stored by the app. Scoring is transcript-based and the UI says so.

**Writing** *(Should have)*
- Learner does: writes their own answer, optionally revises it later.
- Model returns: JSON against writing_v1, eight criterion scores with evidence quotes, one short suggestion. On revision, a separate weakness-addressed check.
- App computes: word count, repeated phrases. Grammar is model-scored only.
- Left out: full rewrites of the learner's work (see Out of scope and D-04).

**Reading** *(Stretch)*
- Learner does: reads a stored, reviewed passage, answers generated questions, possibly including word-in-passage items.
- Model returns: JSON against reading_v1, four criteria (plus vocabulary items when applicable) with evidence quotes from the learner's answer; passage references go in a separate field verified against the passage.
- App verifies: supporting sentence and vocabulary item occur in the passage; regenerate up to two times, then fail gracefully.
- Left out: open-web retrieval, live scraping, copyright-encumbered passages.

**Learning agent** *(Stretch)*
- Learner does: views recommendations on the profile.
- Model returns: a chosen activity from a fixed list and a short rationale that cites stored attempts.
- App verifies: every cited attempt_id, criterion, and score is checked against the database. Tools (if enabled) are read-only and never write.
- Allowed activities (proposed): Impromptu Speaking; Reading & Speaking; speaking follow-up; free writing; reflection; opinion / argument; summarization; writing from reading; a reading session.
- Left out: open-ended activity invention; any write to the database from tools.

---

## 5. Rubric

rubric_version = "v1" (proposed). Scale: 1 Beginning, 2 Developing, 3 Proficient, 4 Strong.

**Score meaning**
- 1 Beginning. The skill is largely absent or blocking meaning.
- 2 Developing. The skill is present but inconsistent or underdeveloped.
- 3 Proficient. The skill is reliably present with minor lapses.
- 4 Strong. The skill is consistently used to the purpose of the task.

### Speaking (`speaking_v1`)

**Clarity**
1: Listener cannot tell what is being claimed; sentences collapse or contradict.
2: Main claim is guessable but often muddy or tangled.
3: Claim is understandable with only small awkward spots.
4: Claim is easy to follow throughout.

**Structure**
1: No order; points appear at random.
2: Some grouping, but opening/middle/end are unclear.
3: Recognizable sequence (e.g. claim → reason → close) with minor drift.
4: Clear beginning, development, and ending that fit the topic.

**Relevance**
1: Mostly off the assigned topic.
2: Touches the topic but spends much time elsewhere.
3: Stays on topic with small asides.
4: Almost everything serves the assigned topic.

**Development of ideas**
1: Assertion only; no reason or example.
2: Thin reason or example; not carried through.
3: At least one developed reason or example.
4: Ideas are extended with specific support and a clear close.

**Vocabulary**
1: Words are too vague or misused to carry meaning.
2: Simple wording; occasional mismatch.
3: Adequate, mostly precise wording.
4: Precise wording that fits the topic without showing off.

**Repetition**
1: Same sentence-level idea loops with no progress.
2: Frequent restatement; little new information.
3: Some restatement, but the talk still moves forward.
4: Restatement only for emphasis; ideas advance.

### Writing (`writing_v1`)

**Clarity**
1: Reader cannot recover the main point.
2: Main point exists but is often obscured.
3: Main point is clear with minor fog.
4: Main point is consistently easy to recover.

**Organization**
1: No usable paragraph or section order.
2: Loose grouping; missing or weak transitions.
3: Logical order with small gaps.
4: Deliberate order; sections support the whole.

**Grammar**
1: Errors block meaning in many sentences.
2: Frequent errors; meaning usually recoverable.
3: Occasional errors; meaning intact.
4: Control of sentence grammar with rare slips.

**Vocabulary**
1: Words fail the task or are repeatedly wrong.
2: Limited or slightly off wording.
3: Adequate and mostly exact.
4: Exact wording that fits purpose and audience.

**Coherence**
1: Sentences do not connect; pronouns/topics jump.
2: Partial thread; some unexplained jumps.
3: Thread holds with minor bumps.
4: Each sentence follows from the last without strain.

**Argumentation**
1: No claim, or claim with no reasoning.
2: Claim plus thin or one-sided reasoning.
3: Claim, reasons, and some response to an obvious objection or limit.
4: Claim, reasons, and a fair handling of limits or counterpoints.
*(For non-argument types, score how well the piece fulfills its assigned purpose instead of "debate.")*

**Supporting examples**
1: No examples or examples that do not match the claim.
2: Vague or generic examples.
3: At least one specific, relevant example.
4: Specific examples that clearly support the point.

**Unnecessary repetition**
1: Large stretches repeat without adding meaning.
2: Noticeable recycling of the same sentences.
3: Some echo; still some forward motion.
4: Tight; repetition only for emphasis.

### Reading answers (`reading_v1`)

**Accuracy**
1: Contradicts the passage or invents the main facts.
2: Mix of correct and incorrect points.
3: Mainly consistent with the passage; small slips.
4: Consistent with the passage on the points that matter.

**Use of passage evidence**
1: No link to the text, or invented "quotes."
2: Vague gesture at the text.
3: Points to a real part of the passage.
4: Uses a relevant part of the passage in a way that answers the question.
*(evidence_quote must always come from the user's answer and pass the substring check against it. Passage references go in a separate field verified against the passage.)*

**Reasoning / inference**
1: No reasoning, or inference the passage cannot support.
2: Thin or partly unsupported inference.
3: Inference that follows from the passage with a small gap.
4: Inference clearly grounded in the passage.

**Completeness**
1: Ignores the question asked.
2: Partial answer; major part missing.
3: Addresses the question with a small omission.
4: Fully addresses what was asked without padding.

### Reporting rules
- No opaque overall score.
- All model scores labeled "AI-estimated against this rubric."
- Dashboards show per-criterion averages and attempt counts.
- Improvement shown only after at least 3 scored attempts of the same activity kind (follow-ups: same target_criterion). Threshold tracked as D-03.

---

## 6. Evaluation approach

**Pipeline (proposed)**
1. Crisis gate runs first (§8).
2. Truncate user text to the approved max length.
3. Neutralize delimiter collisions in user text.
4. User text appears only in the user message, never in the system message.
5. Deterministic metrics are passed in as facts.
6. Low temperature; request structured JSON.
7. Parse; if reasoning is present, strip it before JSON parse.
8. Schema-validate; retry 1 to 2 times.
9. Every evidence_quote must pass the evidence check. Retry once more on evidence failure; then reject (do not store).
10. Cap suggestion at 400 characters; reject if it contains ≥ 80% of the learner's full answer (token overlap).
11. Store metadata listed in §11.

**Latency**
A large model scoring six criteria with quotes plus retries can be slow. The feedback request shows a loading state, uses a fixed timeout, and on timeout switches to the fallback model once before showing a retry message. Exact timeout values are set after the Phase 1 test script measures real response times.

**Evidence check (proposed)**
Normalization: NFKC → casefold → curly quotes to straight → em / en dashes to "-" → collapse whitespace to single spaces.
- Quotes without ellipses must be a single contiguous substring after normalization.
- Quotes with "..." or "…" are split into fragments; each fragment must appear in the user text in order, non-overlapping. Any empty or missing fragment fails.

**Deterministic metrics (application code only)**
- Word count: tokens matching [A-Za-z0-9']+ after normalization.
- WPM: word_count / (speak_seconds / 60), speak_seconds ≥ 1.
- Fillers (conservative): um, umm, uhm, uh, uhh, er, err, ah, ahh, hmm, hm, uh-huh, you know, i mean, kind of, sort of. Not counted: like, so, well, right, actually, basically, literally, just.
- Repeated phrases: after normalization, all word n-grams with n ≥ 3; counted at ≥ 3 occurrences; stopword-only n-grams skipped.

The model does not count. The app computes, then passes the numbers in as facts.

**How I check the model is reasonable**
- Schema validation on every response.
- Evidence substring check on every quote.
- Suggestion guard: length cap and rewrite overlap check.
- Evaluator test set before locking the evaluation model: 6 to 9 samples (weak / medium / strong) plus 2 to 3 adversarial (prompt injection, empty / very short, off-topic). Samples reviewed by me before use. Repeated runs checked for rank order, stability, evidence validity, schema validity. Results recorded in TOOL_FEEDBACK.md.
- Idempotency: one evaluation per attempt. A refresh must not trigger another model call.

**Model roles (provisional; confirm exact IDs and structured-JSON support in the Phase 1 test script)**

Start with one model for everything. Add the fast / slow split only after the core speaking loop works.

| Role | Provisional ID | Notes |
|---|---|---|
| Fast generation | nvidia/Nemotron-3_5-Lightning | Topics, question drafts, short prompts. |
| Evaluation + learning agent (default) | nvidia/nemotron-3-super-120b-a12b | Default scorer and agent. |
| Bake-off only | nvidia/Nemotron-3-Ultra-550b-a55b | Only if the test set shows a clear gain and cost is approved. |
| Fast alternative / fallback | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B | Candidate fallback. |
| Timeout / rate-limit fallback | Lightning or Nano | Locked after Phase 1. |

---

## 7. AI behaviour

**Role of Nemotron per module**
- Speaking. Score six criteria against the transcript. Quote the learner's own words as evidence. Write one short improvement. Never count fillers or words; those come from the app.
- Writing. Score eight criteria. Quote the learner's own words. On revision, a separate check reports whether the identified weakness was addressed. Never rewrite the learner's answer.
- Reading. Score four criteria (plus vocabulary items when applicable). Evidence quotes come from the learner's answer; passage references go in a separate field.
- Learning agent. Choose one activity from the fixed list and explain why using stored attempts. Never invent activity types. Never write to the database.
- Crisis check. Separate call. Yes / no JSON. Does not score.

**Tone and depth**
Proposed: direct, supportive, no flattery, no filler. Each criterion gets one short evidence quote plus a one-line rationale. Exactly one improvement suggestion per evaluation, ≤ 400 characters, addressing the lowest-scoring criterion (or the follow-up's target_criterion).

**Handling bad or off-topic output**
- Off-topic work is scored honestly against the Relevance / Argumentation / Completeness criteria, not refused.
- Empty, very short, or clearly non-English input may trigger a re-prompt to the learner rather than a score.
- Prompt injection in user text must not override evaluator instructions. User text is data, never in the system prompt.
- If the model returns invalid JSON or invalid evidence after the allowed retries, the app rejects the evaluation and shows a retry message. It does not store partial output.

---

## 8. Safety requirements

**Inappropriate content**
- Crisis content is handled first and separately from scoring.
- General inappropriate content is lower priority for Phase 1 than crisis content; the plan is to add a coarse filter later if time allows.

**Crisis content (proposed design)**

- **Stage A: broad lexicon trigger (application code).** Any hit from a broad lexicon of self-harm, suicide, and crisis terms triggers Stage B. Prefer false positives over missed cases.
- **Stage B: model check.** On any Stage A hit, run a separate yes / no JSON check: crisis_suspected (boolean). The model also judges whether the text is a first-person current crisis versus an academic, fictional, or analytical discussion.

Decision table:

| Stage A | Stage B | Action |
|---|---|---|
| No hit | not run | Continue to scoring |
| Hit | Clear "no" (academic / fictional / analytical) | Continue to scoring |
| Hit | "Yes" | Skip scoring, show crisis copy, redact text |
| Hit | Unclear or malformed output | Skip scoring, show crisis copy, redact text (fail safe) |
| Hit | Unavailable (timeout / error) | Skip scoring, show crisis copy, redact text (fail safe) |

- **UI note (required).** The app must state it is a practice tool and not a crisis service.
- **User message.** Fixed copy, not model-generated. Short, supportive, no diagnosis. Invites the user to contact local emergency services if in danger. Shows only helplines from helplines.json, each verified from official sources.
- Never ask the model to invent phone numbers or contact details.
- **Storage.** crisis_events: user id, attempt id, timestamp, coarse category. No full user text. For flagged attempts, after the supportive message is shown, replace stored attempts.input_text with exactly `[redacted: crisis protocol]`. The flagged text must not appear in evaluations.raw_model_output. The attempt row is not deleted.

**Prompt injection**
- User text is untrusted DATA.
- User text must never be inserted into the system prompt.
- Delimiter collisions are neutralized.
- Max input length: 8,000 characters for writing / transcript, 12,000 for passage + answers (proposed).
- Instructions inside user text must not override evaluator instructions.
- Model output must pass schema validation.
- Evidence must pass substring validation.
- Invalid evidence triggers a retry and ultimately rejection.

**User data**
- No real personal writing appears in the video, screenshots, README, or the public repository.
- The app does not store audio.
- **Browser speech service disclosure.** In Chrome and Edge, the Web Speech API sends audio to the browser vendor's speech service for transcription. The UI and README must say this, and that the typed fallback avoids it.
- Flagged crisis text is redacted in the database as described above.

**API key handling**
- NEBIUS_API_KEY stays server-side in .env.
- Never in frontend code, GitHub, screenshots, or logs.
- .env is in .gitignore; .env.example documents the variable without a value.

---

## 9. Architecture

```
Browser (HTML / CSS / JS)
  → Flask routes (validation, auth, HTTP only)
    → services
      → ai_client.py         Token Factory; primary + fallback model
      → evaluation.py        rubric, schema, evidence check, retries
      → generation.py        topics, questions, follow-up prompts
      → learning_agent.py    choose from allowed activities; optional tools
      → metrics.py           word count, WPM, fillers, repeated phrases
      → evidence.py          quote-in-text verification
      → crisis.py            crisis gate: broad lexicon + model check (no scoring)
      → usage_monitor.py     tokens / cost; low-credit alert
    → repositories.py        SQL only here
    → PostgreSQL (Neon Free)

Flask backend ──API requests──> Nebius Token Factory (primary / fallback model)

Prompts: /prompts (versioned).  Schemas: /schemas (versioned).
```

**Identity:** Username + password. One account flagged is_demo and labeled Demo in the UI.

**Hosting:** Flask on Render free web service + Neon Free PostgreSQL. Do not use Render Free Postgres (30-day expiry, 14-day grace, then deletion).

**Deliberately not used** (see §15): React, Next.js, Docker, Kubernetes, Nebius Serverless, Tavily, audio files, Render paid Postgres. Adding any of these requires a Decision log entry first.

---

## 10. Speaking pipeline

1. **Topic:** Fast model proposes a topic; fallback to a hand-written bank on failure.
2. **Timers:** Prepare (default 60 s) → Speak (default 60 s). Configurable.
3. **Recording path A, Web Speech API:** Chrome / Edge only. Live transcription in the browser (audio goes to the browser's speech service; see §8).
4. **Recording path B, typed / pasted fallback:** For unsupported browsers, for judges, and when speech recognition fails.
5. **Transcript stored as text only:** No audio, ever.
6. **Metrics:** Word count, WPM, fillers, repeated phrases computed by the app.
7. **Crisis gate:** Broad lexicon first; model check only on a hit.
8. **Evaluation:** Model returns JSON; app schema-validates and evidence-checks.
9. **Feedback screen:** Per-criterion scores, the learner's own quoted evidence, one short suggestion, and app metrics with a transcript caveat.

| Risk | Mitigation |
|---|---|
| Web Speech API unavailable (Firefox, Safari, some Chromium builds) | Typed / pasted fallback is always visible and equally usable. |
| Speech recognition produces a noisy transcript | UI states that evaluation is transcript-based and does not judge pronunciation or delivery. |
| 60-second speaking limit frustrates longer answers | Timers configurable; default is a starting point, not a rule. |
| Cold-start delay on first speech session | Landing page and UI note this is possible on a free host. |
| Slow evaluation response | Loading state, timeout, one fallback-model retry (see §6). |

---

## 11. Database direction

- No weakness_signals table; weakness statistics are queries over evaluations.
- No audio storage. No opaque overall score column.
- Rate limits are computed from usage_events counts; no separate rate-limit table.

**users**: id, username, password_hash, is_demo, goals (optional), current_focus (optional), created_at.

**passages**: id, title, text, source_name, source_url, license, generator_model_id (nullable), reviewed_at, created_at.

**practice_sessions**: id, user_id, kind, subtype, started_at, ended_at. *(Named practice_sessions so it is not confused with Flask's `session`.)*

**questions**: id, practice_session_id, passage_id, qtype, prompt_text, answer_key, supporting_sentence.

**attempts**: id, practice_session_id, user_id, parent_attempt_id, role (original / revision / follow_up), input_text, input_method (speech_api / typed_fallback), prep_seconds, speak_seconds, target_criterion, crisis_flag, created_at.

**evaluations**: one row per attempt, UNIQUE(attempt_id): rubric_version, prompt_version, schema_version, model_id, temperature, criteria_json, raw_model_output, deterministic_metrics_json, created_at.

**revision_checks**: id, original_attempt_id, revised_attempt_id, weakness_criterion, addressed (boolean), explanation, model_id, prompt_version, raw_model_output, created_at.

**recommendations**: id, user_id, activity_kind, rationale, evidence_json, created_at, accepted_at.

**usage_events**: id, model_id, prompt_tokens, completion_tokens, purpose, user_id, created_at.

**crisis_events**: id, user_id, attempt_id, created_at, category (coarse). No full user text.

**Storage plan.** Neon Free. Plan against 0.5 GB until the Neon console shows otherwise.

**Backup.** Weekly pg_dump via scripts/backup_db.py to my local machine (not the public repo, not Render's ephemeral disk). Use Neon's 1 manual snapshot before risky changes.

---

## 12. Nebius and Nemotron usage notes

*(Fill in as you build: model chosen, how it is called, response times, JSON-mode behavior, where Token Factory sped up the workflow. This feeds the README and the feedback submission.)*

---

## 13. Hosting and deployment

Free-tier path.

**Render Free web service**
- Idle 15 minutes → spin down; next request ~1 minute spin-up.
- 750 free instance hours per workspace per calendar month.
- Hobby bandwidth: 5 GB / month included; if no payment method, Free services suspend for the rest of the month.
- Hobby builds: 500 pipeline minutes / month.
- Render may restart a Free service at any time.
- Do not use Render Free Postgres (30-day expiry, 14-day grace, deletion).

**Neon Free**
- Permanent free plan; no card required.
- 100 CU-hours / project / month; exhaustion suspends compute until next period; data is not deleted.
- Scale to zero after 5 minutes; cannot be disabled on Free.
- Storage: plan against 0.5 GB / project.
- Egress 5 GB / project / month.
- History 6 hours; 1 manual snapshot.
- Autoscaling capped at 0.25 CU.

**Health and keep-alive**
- /health must not query the database.
- /ready may check database readiness (manual).
- Uptime ping: GET /health every 10 to 14 minutes, only during the judging window.
- Hours math: keeping a service awake all month uses about 720 to 744 of the 750 free instance hours, so no other free service in the same Render workspace can run alongside it. Use a workspace that hosts only this app.
- Rationale for /health not touching the database: if /health opened a Neon connection on every ping, 0.25 CU × 24 × 30 ≈ 180 CU-hours would exceed the 100 CU-hour cap and lock judges out.

**Judge-access tension**
Free tiers can become a restriction if Render or Neon suspend, or if judges hit the ~1 minute Render cold start. Mitigations: keep-alive without waking Neon, usage dashboards, low-credit and host-quota alerts, generous but finite rate limits, demo account. If a quota still takes the demo down during judging, I will decide whether to upgrade or move host; I will not claim judge-access compliance until the hosted app is actually up through 15 December 2026, 12:00 PM PT.

---

## 14. Constraints

- **Budget:** Free tiers only; any spend needs a Decision log entry. No payment method on Render.
- **Free tools only:** Flask, Render Free web, Neon Free, GitHub, Web Speech API, YouTube, Devpost. No paid add-ons.
- **New-project rule:** This repository is new during the Submission Period. No reuse of earlier-app code unless a specific piece is approved in the Decision log with the required explanation.
- **Model cost:** Ultra only after the evaluator test set shows a clear gain and the extra cost is approved.
- **Storage:** Plan against 0.5 GB on Neon Free.
- **Data:** No audio stored. No real personal writing in public artifacts.
- **Time:** About 3 full free days plus shorter windows on college days.

---

## 15. Out of scope

Deliberately not building.

- React, Next.js, Vue, or any SPA framework.
- Docker, Kubernetes, or any container runtime.
- Nebius Serverless Endpoints / Jobs (encouraged, not required).
- Tavily or any web-retrieval bonus path.
- Audio file storage of any kind.
- Render paid Postgres.
- Multi-language UI. English only.
- Mobile native apps.
- Paid monitoring or APM tools.
- Real-time collaboration or multi-user sessions.
- Gamification beyond per-criterion progress (no streaks, badges, or leaderboards).
- An opaque overall score.
- A separate weakness_signals table.
- A "rewrite my answer" action (it would replace the learner's work; see D-04).

---

## 16. Timeline

Fill the dates in once you know your submission deadline. Work in this order; do not start a later tier until the earlier one works end to end.

**Priority tiers**
- **Must have:** Speaking loop (topic → speak → metrics → crisis gate → evaluation → feedback), login, Demo account with seeded real evaluations, deployment, README, demo video.
- **Should have:** Writing module, revision with weakness-addressed check, dashboard trends.
- **Stretch:** Reading module, learning agent, dual-model split, Ultra bake-off.

**Phases**

| Phase | Goal | Done when |
|---|---|---|
| 0. Setup | Repo, docs, .gitignore with .env, scripts/ | Spec filled; first commit pushed |
| 1. Model check | Script that calls Nemotron on Token Factory | Reply printed; JSON output works; model IDs confirmed; response times noted |
| 2. Core services | metrics.py, evidence.py, evaluation.py, crisis.py with tests | Evidence check and metrics pass tests on sample text |
| 3. Speaking loop | Flask routes, DB, speaking page, feedback screen | One full speaking attempt works locally, typed fallback included |
| 4. Deploy early | Render + Neon live | Hosted URL works end to end (do this before polishing) |
| 5. Evaluator test set | 6 to 9 samples + adversarial, results in TOOL_FEEDBACK.md | Model choice locked |
| 6. Demo data | Seed Demo account with real evaluations (needs several real attempts per activity, so budget credits and time) | Dashboard shows real per-criterion data and improvement |
| 7. Should-haves | Writing, revision check, dashboard trends | Each works end to end |
| 8. Stretch | Reading, learning agent, dual-model split | Only if time remains |
| 9. Submission | README, TOOL_FEEDBACK.md, demo video under 3 min, Devpost, testing instructions with credentials | Everything submitted; keep-alive running through judging |

Map phases to your free days and college-day windows here: *(add dates)*

---

## 17. Risks and fallbacks

| Risk | Impact | Fallback |
|---|---|---|
| Model returns invalid JSON or bad evidence repeatedly | No evaluation shown | Retry, then fallback model, then clear retry message; nothing partial stored |
| Evaluation too slow | Poor demo | Loading state, timeout, smaller fallback model |
| Token Factory credits run out | Demo down | Usage dashboard and low-credit alert; rate limits; pre-seeded Demo data still viewable |
| Web Speech API fails or is unsupported | No live transcript | Typed / pasted fallback always visible |
| Render cold start or suspension | Judges see a slow or dead app | Keep-alive during judging window; note on landing page; check regularly |
| Neon quota exhausted | Database unavailable | /health avoids the DB; monitor CU-hours; upgrade or move host only via a logged decision |
| Scope too big for the time | Unfinished app | Strict Must / Should / Stretch order (§16); cut Stretch first |
| API key leaked | Account abuse | .env in .gitignore; if ever committed, regenerate the key immediately |
| Crisis text mishandled | Harm to a user | Fail-safe table (§8); fixed copy; redaction; verified helplines only |

---

## 18. Decision log

Every decision gets a status (open / decided) and a date.

| ID | Decision | Status | Date | Notes |
|---|---|---|---|---|
| D-01 | Track: Best Apps and Agents | Decided | | |
| D-02 | License: MIT | Decided | | |
| D-03 | Improvement shown only after 3 scored attempts of the same kind | Open | | Confirm threshold |
| D-04 | Offer a "rewrite my answer" action in Writing? | Open | | Recommendation: no, it conflicts with "refuses to replace the learner" |
| D-05 | How the Demo account behaves with several judges at once (shared read-only, resets, or fresh sandbox per login) | Open | | Shared writable account would mix attempts and break improvement display |
| D-06 | Start with one model, add fast/slow split later | Open | | Confirm after Phase 1 |
| D-07 | Rubric version v1 and scale 1 to 4 | Open | | Marked "proposed" |
| D-08 | Input length limits (8,000 / 12,000 characters) | Open | | Marked "proposed" |
| D-09 | Allowed activity list for the learning agent | Open | | Stretch tier |
| D-10 | Filler word list and repeated-phrase rule | Open | | Marked "proposed" |
| D-11 | Hosting: Render Free web + Neon Free | Decided | | |
| D-12 | Identity: username + password | Decided | | |
| D-13 | Ultra model bake-off | Open | | Only if test set shows clear gain and cost approved |
