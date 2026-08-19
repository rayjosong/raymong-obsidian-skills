---
name: obsidian-weekly-review
description: Drafts or refreshes an evidence-linked Obsidian weekly review without silently mutating tasks, project logs, or Work Highlights. Use when the user asks to generate, write, update, or summarize an ISO week, run a weekly retrospective, or prepare approval-ready weekly follow-up proposals.
---

# Draft an Obsidian Weekly Review

Create a source-linked synthesis for one ISO week. Keep the workflow proposal-first: drafting a review must not silently change any source or operational note.

## Resolve the requested week and output

1. Resolve relative dates in `Asia/Singapore` and use the ISO week-year, not the calendar year. An ISO week runs Monday through Sunday.
2. Require a user-requested target week. Do not create a weekly note because a schedule fired or because the week ended unless the user explicitly requested that periodic note or authorized an ongoing schedule.
3. Interpret `this week`, `last week`, or a date using Singapore local time. Normalize the identifier to `YYYY-Www`, with a two-digit week.
4. Write only when the request asks to generate, create, or update the weekly note. For a chat-only summary, return the synthesis without creating a file.
5. When writing, target `02-Calendar/YYYY-Www.md`. Do not create a separate review note or an index.

## Gather evidence

Read the seven daily notes whose local dates fall in the target ISO week. From each existing `02-Calendar/YYYY-MM-DD.md`, inspect only these current sections when present:

- `## 📥 Captures`
- `## ⏳ Log`
- `## 📝 Scratchpad`
- `## 🤖 AI Synthesis`

Also read `00-Inbox/Daily Review - YYYY-MM-DD.md` for those dates when its status is `[[Completed]]` or `[[Waiting]]`:

- Treat applied proposals and completed review findings as facts.
- Treat pending, approved-but-unapplied, blocked, or rejected proposals as proposal state, not as completed work.
- Use a Waiting review when it adds evidence or unresolved explicit actions, and label incomplete coverage rather than filling gaps by inference.

Consult existing `06-Tasks/`, `07 - Projects/`, `08-Memory/`, and `00-Notes/Work Highlights.md` only as needed to verify current state, exact target text, links, and duplicates. Do not infer a success from calendar attendance, a planned action, an unapproved proposal, or an ambiguous log line.

For every material statement, retain one or more source wikilinks. Prefer a daily-note or Daily Review link; add a heading/block reference when available. If a source is missing or contradictory, state the gap.

## Synthesize the week

Draft concise sections in this order:

1. **Daily notes** — one link for each daily note that exists; report missing days without creating them.
2. **Highlights and achievements** — evidence-backed outcomes, decisions, meaningful interactions, or shipped work.
3. **Project progress** — movement grouped under existing project wikilinks; do not invent a project.
4. **Themes and blockers** — recurring patterns, unresolved constraints, and coverage gaps.
5. **Pending explicit actions** — actions the user explicitly recorded that remain unresolved. Verify existing TaskNotes state before calling an item pending.
6. **Approval-ready proposals** — optional exact changes that should be considered after the retrospective.

Deduplicate by underlying source and effect, not merely by wording. Sort day links chronologically, project groups by wikilink, and pending actions by source date. Prefer `None evidenced` to invented filler.

## Make changes proposal-first

Never perform these actions while drafting or refreshing a weekly review:

- change a TaskNotes status, schedule, due date, priority, context, project, estimate, reminder, or recurrence field;
- create a TaskNotes note from inferred intent;
- append or edit `00-Notes/Work Highlights.md`;
- append or edit a project hub Log; or
- move, rename, delete, or rewrite source notes.

Either defer a candidate already covered by `[[Daily Review - YYYY-MM-DD]]` to that review, or record an exact weekly proposal. Do not create a second proposal for the same effect.

Use stable IDs `WR-YYYYWww-001`, `WR-YYYYWww-002`, and so on. Every newly drafted proposal starts with `state: pending` and must contain:

- kind and exact target path;
- source wikilink(s) and quoted or tightly paraphrased evidence;
- rationale;
- exact Before and After text, or the complete content for a proposed new note;
- a precondition that can be rechecked; and
- an exact rollback.

Render those fields under one proposal heading so an approval names an unambiguous ID:

```markdown
#### WR-YYYYWww-001 — Short action
- state: pending
- kind: task-status | task-schedule | task-create | project-log | work-highlight | other
- target: `vault/relative/path.md`
- sources: [[source note]]
- evidence: ...
- rationale: ...
- Before: ...
- After: ...
- precondition: ...
- rollback: ...
- fingerprint: ...
```

Fingerprint `kind | target | source | normalized proposed action`. Preserve existing IDs, state, wording, and any decision/apply logs on refresh. Append only a genuinely new fingerprint with the next unused ID; never renumber or let an earlier `approve all` cover a later proposal. Approval or application is a separate explicit action governed by the target workflow and `AGENTS.md` permission tiers.

## Create or refresh safely

For a new weekly note, follow `x/templates/weekly template.md` and current Journals conventions:

```yaml
---
journal: Weekly
journal-date: YYYY-MM-DD
---
# Week WW, YYYY (Month D-Month D)
```

Set `journal-date` to the Monday of the ISO week. Keep the template's displayed Monday-to-Friday range. Use the ISO week-year and unpadded display week in the heading.

Manage only this delimited block:

```markdown
<!-- AI-WEEKLY-REVIEW:START week=YYYY-Www input-revision=SHA256 -->
## Weekly Review
...
<!-- AI-WEEKLY-REVIEW:END -->
```

- If the note is new, write the template-compatible frontmatter and heading, then the managed block.
- If it exists without the markers, preserve all content byte-for-byte and append the managed block. Do not reinterpret an old or user-authored section as managed content.
- If exactly one valid managed block exists for the target week, replace only that block. Preserve all text before and after it byte-for-byte.
- If markers are malformed, duplicated, or identify another week, stop and ask for repair rather than overwriting.
- Do not alter existing frontmatter, planning sections, embedded queries, or user prose. Report incompatible Journals metadata instead of fixing it opportunistically.

Compute `input-revision` as SHA-256 over sorted rows of each selected source's vault-relative path and the exact excerpt used. Immediately before writing, re-read the target and inputs. If the revisions or target changed, recompute rather than overwrite concurrent edits. If the revision and rendered managed block are unchanged, leave the file byte-for-byte unchanged.

After writing, verify the ISO dates, target path, markers, source links, proposal IDs, and unchanged surrounding content. Report the reviewed week, days covered, unresolved gaps, proposal count, and whether the file was created, refreshed, or already current.
