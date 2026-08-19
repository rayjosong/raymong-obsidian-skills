---
name: obsidian-voice-dump-split
description: Preserve a speech-to-text transcription as a verbatim raw Obsidian capture, then propose how its distinct logs, tasks, ideas, and context should be classified through the daily-review workflow. Use only when the user explicitly asks to process a voice dump or transcription; this is a parked post-MVP enhancement, not the text-capture path.
---

# Split a Voice Dump

This enhancement starts only after speech has already been transcribed to text. Preserve
the original before interpreting it; never treat a cleaned transcript as the source of
truth.

## Preserve first

1. Invoke `obsidian-capture-text` with the complete transcription exactly as received.
   Use the original provider ID and timestamp when available, and identify the source as
   the voice or transcription provider.
2. Confirm the capture receipt before continuing. If capture fails, stop and return the
   transcript unchanged so the same external ID can be retried.
3. Never edit, move, archive, truncate, or delete the raw capture after it is stored.

## Propose distribution

Analyze the preserved capture without changing it. Separate only clearly distinct
intents:

- chronological observations suitable for `## ⏳ Log` or `## 📝 Scratchpad` in the
  relevant daily note;
- explicit and inferred actions suitable for TaskNotes proposals;
- concepts, designs, research, or context that should remain in the Inbox or connect to
  an existing project or memory note; and
- possible duplicates or unclear fragments that should remain untouched.

Create proposal inputs for `obsidian-daily-review-batch`. For every proposal, include:

- the exact raw-capture wikilink;
- the source segment or a faithful short excerpt;
- the proposed destination and wording;
- whether the action was explicit or inferred; and
- any uncertainty that requires a user decision.

Do not apply the proposals from this skill. Let the daily-review workflow assign stable
proposal IDs, present the approval batch, and apply only approved changes.

## Interpretation rules

- Remove fillers only in proposed wording, never in the raw capture.
- Preserve technical identifiers, names, dates, negation, and uncertainty exactly.
- Do not combine unrelated intents merely because they occurred in one recording.
- Do not invent due dates, schedules, priorities, estimates, projects, or reminders.
- Do not create TaskNotes, memory notes, synthesis notes, or project-log entries directly.
