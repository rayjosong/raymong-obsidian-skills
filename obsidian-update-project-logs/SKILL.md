---
name: obsidian-update-project-logs
description: Propose deduplicated worklog entries from a specified Obsidian daily note for exact existing project-hub Log sections, then append only entries the user approves. Use for a narrow manual project-log propagation request or as an approved follow-up to the daily-review workflow.
---

# Update Project Logs

## Build the proposal

1. Read the specified daily note, defaulting to today's existing note. Use its
   `journal-date` as the entry date. Scan `## ⏳ Log`, `## 📝 Scratchpad`, and
   `## 🤖 AI Synthesis` when present.
2. Resolve only explicit wikilinks to exact existing files in `07 - Projects/`. A strong
   contextual mention may be reported as ambiguous, but must not select a target by
   inference.
3. Open each exact project hub and locate its `## Log` or `### Log` section. If no Log
   exists, report the gap and do not restructure the project note.
4. Draft concise entries only for meaningful progress, decisions, outcomes, or blockers:

   ```markdown
   - **[[YYYY-MM-DD]]**: <project update> (from [[daily note]])
   ```

5. Deduplicate against the whole Log using the date, source daily note, event or
   decision, and semantic meaning. Different wording is not a new update.
6. Present the exact project path and full proposed append string for approval. Make no
   edit during this pass.

## Apply an approval

- Re-read the project hub and deduplicate again immediately before writing.
- Append only the approved string at the end of the existing Log section.
- Never reorder, rewrite, or delete prior entries.
- Report updated, skipped-as-duplicate, ambiguous, and missing-Log targets separately.

When invoked from `obsidian-daily-review-batch`, reuse its approved proposal rather than
asking for a second approval, but still perform the exact-target and dedupe checks.
