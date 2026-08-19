# Daily review proposal schema

Use this structure so humans, Telegram handlers, and later agents can refresh and
apply the single queue deterministically.

## Contents

- [Note shape](#note-shape)
- [Required proposal fields](#required-proposal-fields)
- [Exact proposal examples](#exact-proposal-examples)
- [Coverage, state, refresh, and transaction rules](#coverage-state-refresh-and-transaction-rules)

## Note shape

```markdown
---
created: 2026-08-13
status: "[[Waiting]]"
summary: "Approval-ready review of captures, daily context, and work evidence for 2026-08-13."
area: personal/second-brain
maturity: developing
review_date: 2026-08-13
review_timezone: Asia/Singapore
scheduled_for: "18:30"
generated_at: 2026-08-13T18:30:00+08:00
updated_at: 2026-08-13T18:30:00+08:00
run_result: success
personal_coverage: complete
personal_input_count: 3
personal_input_revision: "sha256:1234567890abcdef..."
work_coverage: provisional
work_evidence_revision: "sha256:abcdef1234567890..."
proposal_count: 2
source_notes:
  - "[[2026-08-13]]"
  - "[[Work Evidence - 2026-08-13]]"
---
# Daily Review — 2026-08-13

> [!warning] Personal review ready; work evidence provisional
> Current IDs may be decided now. Later amendments receive new pending IDs.

## Coverage
- Personal inputs: complete — 3 inputs at `sha256:1234567890abcdef...`
- Daily note: [[2026-08-13]]
- Raw captures reviewed: [[Capture A]], [[Capture B]]
- Work evidence: provisional — [[Work Evidence - 2026-08-13]] at `sha256:abcdef1234567890...`
- Gaps: Work evidence covers activity through 18:30; a full-day refresh is pending.

## Proposals

<proposal blocks in the required kind order>

## Amendment Log
- 2026-08-13T18:30:00+08:00 — Initial draft; personal revision `sha256:123...`; work revision `sha256:abc...` (provisional); added DR-20260813-001 and DR-20260813-002.

## Decision Log
- _No decisions recorded._

## Apply Log
- _Nothing applied. Normal approval applies immediately; “approve without applying” is the explicit exception._
```

## Required proposal fields

Every proposal uses this shape. `before` and `after` may be literal blocks. For a new
file, use `before: file absent` and put the complete file in `after`.

```markdown
### DR-20260813-001 — Concise action title
- status: pending
- kind: metadata
- fingerprint: a1b2c3d4e5f6
- source: [[Source note]]
- target: `00-Inbox/Source note.md`
- evidence: Concise source-grounded evidence, with heading or line when useful.
- rationale: Why this exact proposal follows from the evidence.
- precondition: Target exists and the named field is absent.
- before: `summary` absent
- after: `summary: "Exact proposed value"`
- rollback: Remove only the exact `summary` key/value added by this proposal.
```

Sort a new review by kind in this order, then target and source:

1. `daily-synthesis`
2. `metadata`
3. `inbox-note`
4. `task`
5. `connection`
6. `memory-note`
7. `project-log`
8. `person-log`
9. `work-highlight`
10. `duplicate`
11. `stale`

## Exact proposal examples

### Daily synthesis

```markdown
### DR-20260813-001 — Synthesize the daily note
- status: pending
- kind: daily-synthesis
- fingerprint: 02a3b4c5d6e7
- source: [[2026-08-13]]
- target: `02-Calendar/2026-08-13.md`
- evidence: The Log and Scratchpad contain substantive entries; the current synthesis is the empty template.
- rationale: An exact synthesis makes the day reviewable without changing any source capture.
- precondition: The target still contains the exact `before` block between `## 🤖 AI Synthesis` and the next level-2 heading.
- before: |
    ## 🤖 AI Synthesis
- after: |
    ## 🤖 AI Synthesis

    ### 🎯 Daily Summary
    - Focused on the specific work supported by the source entries.

    ### 💡 Key Takeaways & Decisions
    - Exact supported decision or learning.

    ### ✅ Action Items
    - Exact explicit intended action; this does not create a TaskNote.

    ### 📂 Projects Touched
    - [[Existing Project]] — specific context.
- rollback: Replace only the exact `after` block with the recorded `before` block if it is still unchanged.
```

Omit unsupported optional subsections. Never add the synthesis heading when absent.

### Atomic Inbox idea note

```markdown
### DR-20260813-002 — Capture one atomic idea
- status: pending
- kind: inbox-note
- fingerprint: 13b4c5d6e7f8
- source: [[2026-08-13]]
- target: `00-Inbox/Specific idea title.md`
- evidence: Exact source line expressing this one idea.
- rationale: The idea is durable enough to revisit and is distinct from other captured ideas.
- precondition: The target path is absent and no semantically equivalent Inbox or durable note exists.
- before: file absent
- after: |
    ---
    created: 2026-08-13
    type: "[[Idea]]"
    status: "[[Idea]]"
    summary: "One-line description of this single idea."
    maturity: raw
    related:
      - "[[2026-08-13]]"
    ---
    # Specific idea title

    Source-faithful detail for this idea only.
- rollback: Delete only this exact file if its full content is still identical; deletion requires the applicable approval.
```

Do not combine unrelated ideas, erase the source line, or choose an occupied path.

### TaskNote without invented fields

```markdown
### DR-20260813-003 — Create the explicit task
- status: pending
- kind: task
- fingerprint: 24c5d6e7f8a9
- source: [[2026-08-13]]
- target: `06-Tasks/Review the incident alert.md`
- evidence: “I need to review the incident alert.”
- rationale: The source states an intended action rather than a possibility or observation.
- precondition: The target path is absent and no open TaskNote represents the same action.
- before: file absent
- after: |
    ---
    created: 2026-08-13
    source: "[[2026-08-13]]"
    type: "[[Task]]"
    status: "[[Waiting]]"
    dateCreated: 2026-08-13T18:30:00.000+08:00
    dateModified: 2026-08-13T18:30:00.000+08:00
    ---
    # Review the incident alert

    Extracted from [[2026-08-13]].

    Exact source-supported context.
- rollback: Delete only this exact file if its full content is still identical; deletion requires the applicable approval.
```

Omit priority, due, schedule, context, project, estimate, reminder, and recurrence
fields unless their exact values are explicit in the source.

### Project or person Log append

```markdown
### DR-20260813-004 — Append the project worklog
- status: pending
- kind: project-log
- fingerprint: 35d6e7f8a9b0
- source: [[2026-08-13]]
- target: `07 - Projects/Existing Project.md`
- evidence: Exact daily-note line linked to [[Existing Project]].
- rationale: The line records durable work, a decision, or a blocker for the verified project.
- insertion-anchor: `- **[[2026-08-12]]**: Exact current final Log entry.`
- precondition: The target and existing Log heading still exist, the exact insertion anchor is unchanged, and no entry on 2026-08-13 already covers this meaning.
- before: The exact insertion anchor is the final line of the Log section.
- after: |
    - **[[2026-08-12]]**: Exact current final Log entry.
    - **[[2026-08-13]]**: Exact proposed project update.
- rollback: Remove only the exact 2026-08-13 line if unique and unchanged; preserve every other Log entry.
```

Use `kind: person-log` for a verified `type: Person` target. If the Log is empty,
record the exact heading plus its following boundary as the insertion anchor. Block
instead of rebasing when the anchor changed; a refresh may propose a new exact append.

### Work highlight

```markdown
### DR-20260813-005 — Record an evidence-backed work highlight
- status: pending
- kind: work-highlight
- fingerprint: 46e7f8a9b0c1
- source: [[Work Evidence - 2026-08-13]]
- source-evidence-id: wh-a1b2c3d4e5f6
- target: `00-Notes/Work Highlights.md`
- evidence: [Raymond's Slack message](https://example.invalid) plus a concise connected response.
- rationale: The evidence shows a specific contribution, demonstrated judgment, and meaningful response.
- precondition: Neither the hidden ID nor a semantically equivalent highlight exists in the target.
- before: The exact date block does not contain this highlight.
- after: |
    - [[2026-08-13|13 August 2026]] **Thursday** (15:20)
      - I identified ..., proposed ..., which helped ... [Evidence](https://example.invalid)
        <!-- work-highlight-id: wh-a1b2c3d4e5f6 -->
- rollback: Remove only the exact nested highlight and hidden ID; preserve the date block and all other entries.
```

## Coverage, state, refresh, and transaction rules

- `personal_coverage`: `complete | error`.
- `work_coverage`: `missing | error | provisional | complete | no-data`.
- Work coverage mapping is exact: no evidence file is `missing`; evidence `partial` is
  `error`; evidence `provisional` is `provisional`; evidence `complete` is `no-data`
  only when `candidate_count: 0` and both source states are explicitly `no-data`, and
  is otherwise `complete`.
- `run_result`: `success | error`; success describes the pass against recorded
  revisions, not queue closure.
- Omit Work Evidence from `source_notes` when missing.
- Preserve last successful revisions when a refresh errors; record the failed attempt
  in Coverage without claiming a new successful revision.
- Use the warning callout for missing, error, or provisional work coverage.
- Normal flow is `pending -> approved -> applied` or `pending -> approved -> blocked`.
- `pending -> approved` alone requires explicit “without applying.”
- Rejection is `pending -> rejected`. A non-applied proposal may become `superseded`
  only when a newer proposal names it.
- Terminal states are `rejected`, `applied`, and `superseded`; all others need attention.
- Preserve IDs, states, proposal text, and logs on refresh. Append with the next ID and
  never apply an old `approve all` to new IDs.
- Before applying, accept only the exact recorded Before or exact After state. Exact
  After permits crash recovery; anything else blocks.
- Apply and verify each ID independently with atomic single-file updates where
  supported. Continue after a blocked item and report partial success.

Set the note to `[[Completed]]` only when personal coverage is complete, work coverage
is complete or no-data, and every proposal is terminal. Otherwise use `[[Waiting]]`.
