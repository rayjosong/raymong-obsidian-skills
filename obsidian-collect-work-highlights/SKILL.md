---
name: obsidian-collect-work-highlights
description: Ingest evidence-backed work-highlight candidates from Raymond's authored Slack messages with directly connected replies or reactions and Google Meet Notes by Gemini documents linked from Calendar into a deduplicated Obsidian evidence note. Use for the 18:30 Asia/Singapore work-evidence scan, catch-up runs after the Mac wakes or logs in, or manual date reprocessing before the combined daily review.
---

# Ingest Work-Highlight Evidence

Run this workflow on the designated M1 Mac through the company-approved Claude
Enterprise environment. Use cloud Claude Enterprise only. Do not use a local model,
Hermes, Telegram, Codex, or another model to inspect or interpret the work sources.

This workflow is ingestion only. Create or update a durable work-evidence note for the
combined daily-review workflow to consume. Do not create an approval queue, ask for
decisions, modify a Daily Review note, or write to `00-Notes/Work Highlights.md`.

Read [references/evidence-schema.md](references/evidence-schema.md) before creating,
updating, or deduplicating evidence. Before using `gws`, also read the prerequisite and
safe-export guidance in
[`../obsidian-meeting-action-items/SKILL.md`](../obsidian-meeting-action-items/SKILL.md).
Reuse only its authentication and temporary-export mechanics, not its source search or
action-item inference.

## Enforce the execution boundary

- Require an authenticated Claude Enterprise session on the local M1 runner.
- Use the existing authenticated `gws` CLI for Calendar and Google Drive access.
- Use only the company-approved Slack capability available to Claude Enterprise.
- Keep source access read-only. Do not change Slack, Calendar, Drive, or meeting notes.
- Keep temporary Google exports outside the vault and retain no raw source dump.
- If Claude Enterprise or a required source is unavailable, mark that source `error` in
  the evidence note and retry later. Never fall back to another model or silently claim
  complete coverage.

## Determine the evidence date

Use `Asia/Singapore` for every date boundary.

- Schedule a run every day at 18:30 local time on the M1.
- Configure the local macOS runner with both a calendar trigger and load/login behavior.
  A missed 18:30 run must start on the first login or wake afterward.
- At 18:30 or later, include the current local date. Before 18:30, catch up only dates
  before today.
- Treat an 18:30 same-day note as `provisional` because work can continue afterward. On
  the next invocation, refresh the previous date through 23:59:59 and mark it
  `complete`. Preserve stable IDs while adding late evidence.
- Derive state from existing Work Evidence notes. Process every missing date in
  ascending order; update a provisional or partial note in place instead of creating
  another note.
- Consider a past date complete only after a full-day scan and when both sources are
  `ok` or `no-data`. Retry provisional dates and dates with either source in `error` on
  the next invocation.
- Ensure at most one normal run is active for an evidence date. A manual force-reprocess
  may refresh the same file but must preserve stable IDs.

The M1 does not need to remain awake continuously when the catch-up guard is present.
Do not implement scheduling by keeping a chat session permanently open.

## Collect Slack evidence

1. Search the target date for messages authored by Raymond's authenticated Slack
   identity. Use exclusive local-day bounds converted to the API's required timezone.
2. For each authored message, inspect only enough thread context to decide whether it
   demonstrates a meaningful skill or outcome.
3. Retain Raymond's authored message and only directly connected evidence:
   - a thread root needed to understand Raymond's reply;
   - replies that quote, address, answer, adopt, challenge, endorse, or report an outcome
     from Raymond's contribution; and
   - reactions attached to Raymond's message.
4. Discard unrelated branches and general thread history. Do not summarize a whole
   channel or thread merely because Raymond posted in it.
5. Preserve a canonical permalink for every retained message. Treat reactions as
   supporting evidence only; an emoji or reaction count cannot qualify on its own.

Do not include messages authored only by other people, private conversation material
unrelated to Raymond's contribution, routine status updates, or raw message-count
metrics.

## Collect Google Meet evidence

1. Use `gws` to list Calendar events intersecting the target local date.
2. Follow only Google Docs explicitly attached or linked to those events as Notes by
   Gemini. Do not replace this with a broad Drive crawl.
3. Export each permitted document as plain text to a unique scratch directory using the
   safe `gws drive files export` pattern in the sibling meeting skill.
4. For a recurring notes document, isolate the section for the target event/date. Ignore
   earlier and later sessions in the same document.
5. Retain only passages that explicitly attribute a contribution to Raymond, plus the
   minimum connected passage showing a response, decision, or outcome.
6. Preserve the Calendar event ID, Google document ID, and shareable evidence link.

Attendance, being named as a participant, or receiving an action item is not evidence of
a highlight. If attribution is ambiguous, omit the candidate and record the ambiguity in
the evidence note's gaps section.

## Select meaningful candidates

Evaluate demonstrated behavior, not flattering language. Prefer evidence of:

- technical judgment or problem solving;
- ownership, initiative, or incident leadership;
- clear communication or knowledge sharing;
- collaboration, mentoring, alignment, or unblocking others; or
- customer, business, delivery, quality, or reliability impact.

Score each possible candidate privately on four dimensions: demonstrated behavior
`0-3`, concrete outcome `0-3`, evidence quality `0-3`, and independent response or
adoption `0-2`. Include it as a candidate only when the total is at least `7`,
demonstrated behavior is at least `2`, and evidence quality is at least `2`. A
lower-scoring item may appear under `Borderline evidence` but must not be represented as
a recommended highlight.

Draft concise suggested wording in Raymond's first-person work-log voice. Describe the
situation, Raymond's specific action, and the resulting or expected value. Distinguish an
observed outcome from an inference. Avoid performance-review hype and invented impact.

## Deduplicate and write the evidence note

- Create or update `00-Inbox/Work Evidence - YYYY-MM-DD.md` using the schema.
- Generate evidence atom IDs and candidate IDs exactly as specified in the schema.
- Check the current note and earlier Work Evidence notes for exact IDs, overlapping
  evidence, and semantically equivalent contributions.
- Merge Slack and Meet evidence when both describe the same contribution. Keep the
  stable primary evidence and candidate ID.
- Store short paraphrases and direct evidence links, not raw Slack threads or full
  meeting-note text.
- Record source errors and attribution gaps so a no-candidate result is not mistaken for
  complete coverage.
- Store candidates as neutral evidence records. Do not assign proposal or decision
  states.

Return a concise ingestion receipt containing the evidence-note path, coverage state,
candidate count, source errors, and whether the run created, refreshed, or reused the
note. Leave all classification into Daily Review proposals, approval handling, and
application to the separate combined daily-review workflow. Never infer a TaskNotes task
from work evidence.
