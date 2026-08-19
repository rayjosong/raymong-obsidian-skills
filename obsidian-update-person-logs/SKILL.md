---
name: obsidian-update-person-logs
description: Propose deduplicated observations from a specified Obsidian daily note for exact existing Person-note Log sections, then append only entries the user approves. Use for a narrow manual person-log propagation request or as an approved follow-up to the daily-review workflow.
---

# Update Person Logs

## Build the proposal

1. Read the specified daily note, defaulting to today's existing note. Use its
   `journal-date` as the entry date. Scan `## ⏳ Log`, `## 📝 Scratchpad`, and
   `## 🤖 AI Synthesis` when present.
2. Resolve only explicit wikilinks whose exact targets are files in `08-Memory/` with
   `type: Person`. Do not infer a person from an unlinked name.
3. Open each exact Person note and locate `## Log`. If it is absent, report the gap and
   do not restructure the note.
4. Draft one concise, source-grounded observation per meaningful interaction. Format it:

   ```markdown
   - **[[YYYY-MM-DD]]**: <observation> (from [[daily note]])
   ```

5. Deduplicate against the whole existing Log using the date, daily-note source, named
   interaction, and semantic meaning. Do not create a second entry merely because the
   wording differs.
6. Present the exact target path and full proposed append string for approval. Make no
   edit during this pass.

## Apply an approval

- Re-read the target note and deduplicate again immediately before writing.
- Append only the approved string at the end of the existing `## Log` section.
- Never reorder, rewrite, or delete prior entries.
- Report updated, skipped-as-duplicate, and unresolved targets separately.

When invoked from `obsidian-daily-review-batch`, reuse its approved proposal rather than
asking for a second approval, but still perform the exact-target and dedupe checks.
