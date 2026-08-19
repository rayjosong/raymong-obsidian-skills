# Work-evidence schema

Use this schema for durable, retry-safe evidence ingestion. Preserve verbatim evidence
only in the source systems; store concise paraphrases and links in Obsidian. This note is
input to the combined daily review, not an approval surface.

## File identity

Create one file per target day:

```text
00-Inbox/Work Evidence - YYYY-MM-DD.md
```

Use this frontmatter without removing any existing properties:

```yaml
---
created: YYYY-MM-DD
summary: "Evidence-backed work-highlight candidates from YYYY-MM-DD."
area: work/career
maturity: developing
evidence_date: YYYY-MM-DD
evidence_timezone: Asia/Singapore
coverage: provisional
generated_at: YYYY-MM-DDTHH:mm:ss+08:00
candidate_count: 0
---
```

Set `coverage` to only `provisional`, `partial`, or `complete`. Do not add a review
status, decision state, due date, priority, reminder, or TaskNotes metadata.

## Stable identifiers

Normalize all identifiers to lowercase before hashing.

Evidence atom IDs:

- Slack message: `slack:<workspace-id>:<channel-id>:<message-ts>`
- Slack reaction set: `slack-reactions:<workspace-id>:<channel-id>:<message-ts>`
- Meet passage: `gmeet:<calendar-event-id>:<document-id>:<passage-key>`

Build `passage-key` from the nearest stable heading plus the SHA-256 of the normalized
first sentence explicitly attributing Raymond's contribution. Normalize by trimming,
lowercasing, collapsing whitespace, and removing presentation-only punctuation. Use the
first 12 lowercase hexadecimal characters of the hash.

Choose one `primary_evidence_id` deterministically:

1. the earliest Raymond-authored Slack message that demonstrates the contribution; or
2. if no Slack evidence exists, the earliest explicitly attributed Meet passage.

Set the candidate ID to:

```text
wh-<first 12 lowercase hex characters of sha256(primary_evidence_id)>
```

Replies, reactions, newly discovered corroboration, scoring changes, and edited
suggested wording must not change an existing candidate ID. When two candidates are
merged, keep the ID whose primary evidence ranks first by the rule above and record the
other ID in `Merged IDs`.

## Evidence-note format

```markdown
# Work Evidence - 14 August 2026

- Evidence date: 2026-08-14
- Run ID: whe-2026-08-14
- Updated: 2026-08-14T18:34:12+08:00
- Coverage: provisional | partial | complete

## Source coverage

- Slack: ok | no-data | error - short factual note
- Meet: ok | no-data | error - short factual note

## Candidates

### wh-a1b2c3d4e5f6 - Concise descriptive title

- Occurred: 2026-08-14T15:20:00+08:00
- Primary evidence ID: slack:t123:c456:1786701600.123456
- Merged IDs: none
- Skill signals: technical judgment, collaboration
- Confidence: high | medium
- Score: 9/11
- Suggested wording: I identified ..., proposed ..., which helped ...
- Why it qualifies: Concrete behavior and observed outcome, stated without exaggeration.
- Evidence:
  - [Raymond's Slack message](https://...) - concise paraphrase of Raymond's contribution.
  - [Connected reply](https://...) - concise paraphrase of adoption, response, or outcome.
  - [Notes by Gemini](https://docs.google.com/...) - concise attributed meeting evidence.

## Borderline evidence

### wh-b1c2d3e4f5a6 - Concise descriptive title

- Score: 6/11
- Missing signal: No concrete outcome or independent response yet.
- Evidence: [Primary source](https://...)

## Gaps and exclusions

- Name inaccessible or failed sources and ambiguous attribution.
- Summarize categories of excluded material; do not copy unrelated thread history.
```

Omit an empty `Borderline evidence` section. Use `provisional` for a same-day 18:30
scan, `partial` whenever a source failed, and `complete` only after a full-day scan of a
past date. `partial` takes precedence over `provisional`. If a source failed, keep the
note even when there are no candidates. A complete no-data day may use the same file
with empty candidates and explicit `no-data` source states. Count only qualifying
records under `## Candidates` in `candidate_count`; exclude borderline evidence. Keep
frontmatter `coverage`, `generated_at`, and `candidate_count` synchronized with the body
after every refresh.

## Dedupe rules

Apply these checks in order:

1. **Exact ID:** Update the existing candidate; never create a second block.
2. **Evidence overlap:** If candidates share a primary atom or describe one outcome in
   the same thread or meeting, merge them.
3. **Cross-source equivalence:** Merge Slack and Meet records of the same interaction or
   decision even when their atom IDs differ.
4. **Cross-date equivalence:** If a conversation spans midnight or is rediscovered in a
   later scan, retain it only in the Work Evidence note for the date of the primary
   evidence. Add newly found corroboration to that record.

Never deduplicate merely because two records demonstrate the same skill. They must
represent the same contribution or outcome.

## Consumer contract

The combined daily-review workflow may read candidates from this note and create its own
deterministic work-highlight proposals. This evidence note must not contain:

- approval or rejection commands;
- proposal or decision states;
- Daily Review proposal IDs;
- decision or apply logs; or
- publication markers for `00-Notes/Work Highlights.md`.

On refresh, preserve evidence and candidate IDs. The consumer is responsible for
remembering human decisions and preventing already decided or published highlights from
being proposed again.
