---
name: obsidian-process-daily-note
description: Replaces only the `## 🤖 AI Synthesis` section of one Obsidian daily note from its Log and Scratchpad. Use when the user explicitly asks to summarize, resynthesize, or process a specific daily note without running the full end-of-day review or creating tasks, notes, links, logs, or highlights.
---

# Process One Daily Note

Use this narrow, manually invoked workflow only for AI Synthesis. For full daily
processing, proposals, or approval batching, use `obsidian-daily-review-batch`.

1. Resolve the requested note in `02-Calendar/`; default to today's date only when the
   user did not name a date.
2. Require an existing `## 🤖 AI Synthesis` heading. If absent, report that the note
   needs manual/template migration; do not add sections or restructure it.
3. Read only the note's `## ⏳ Log`, `## 📝 Scratchpad`, legacy `## Captured` / `## Logs`
   bodies when present, and the current synthesis. Preserve all source text.
4. Draft this exact shape, omitting optional subsections with no supported content:

   ```markdown
   ## 🤖 AI Synthesis

   ### 🎯 Daily Summary
   - One or two source-grounded sentences describing the day's main focus.

   ### 💡 Key Takeaways & Decisions
   - Supported decision, learning, or idea.

   ### ✅ Action Items
   - Explicit intended action only.

   ### 📂 Projects Touched
   - [[Verified Project]] — source-grounded context.
   ```

5. Do not hallucinate implicit tasks, create TaskNotes or Inbox notes, update project or
   person logs, classify captures, or write highlights. The Action Items subsection is
   summary text only.
6. Re-read the target and replace exactly the current synthesis block up to the next
   level-2 heading. If that Before block changed, stop rather than overwrite concurrent
   edits. Use an atomic single-file update when supported and verify only that section
   changed.
7. Report the note and exact section replaced. If the user wants broader processing,
   direct the next run to `obsidian-daily-review-batch`, which will place every proposed
   downstream change in the one approval queue.
