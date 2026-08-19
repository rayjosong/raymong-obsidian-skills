---
name: obsidian-inbox-process
description: Process one or more explicitly selected existing Markdown notes in 00-Inbox by understanding them, adding safe retrieval metadata, and connecting them to existing vault context. Use for focused, on-demand inbox-note triage; do not use as an end-of-day review, daily-note processor, or automatic task orchestrator.
---

# Process Selected Inbox Notes

Process only the exact `00-Inbox/` note or explicitly listed set of notes named by the
user. If the request says only "process my inbox," list candidate notes and ask the user
to select them before changing anything. Use `obsidian-daily-review-batch` for a day's
captures or an evening review.

## Process

1. Resolve each requested path under `00-Inbox/`. Read each note in full and record its
   current frontmatter and outgoing wikilinks.
2. Identify the note's main idea, source type, relevant existing projects, people,
   topics, and explicit actions. Do not infer facts from filenames alone.
3. Add or update only safe, additive retrieval metadata:
   - `summary`: one factual sentence grounded in the note;
   - `area`: an existing coarse domain when clear;
   - `maturity`: `developing`, or `connected` only after the note has meaningful links
     to existing project or memory notes; and
   - `related`: existing internal wikilinks when unambiguous.
4. Preserve every existing field, especially plugin-managed and Bases-queried keys.
   Preserve the body except for small, clearly useful links; do not rewrite the source
   text for style.
5. Before adding a body link, confirm the exact target exists. Do not create a dangling
   link from a guessed name.
6. Report each changed note, the exact metadata or links added, and anything left
   uncertain.

## Proposal-only outcomes

Do not create these during focused inbox processing unless the user separately approves
the exact proposal:

- TaskNotes tasks from either explicit or inferred actions;
- new Person, Topic, Decision, Goal, or Context memory notes;
- new project hubs or project-log entries;
- distilled synthesis or source notes; or
- moves, renames, archival, or deletion of the selected Inbox note.

For each useful proposal, provide the source note, exact destination, proposed title or
entry, and why it belongs there. Route approved task creation through the TaskNotes
workflow and approved batch classifications through `obsidian-daily-review-batch` when
they are part of a daily review.

## Boundaries

- Do not read or edit daily notes unless the user explicitly includes one as supporting
  context; never write an end-of-day synthesis from this skill.
- Do not edit `.base` dashboards. Correct metadata makes their views update naturally.
- Do not move a note to signal maturity. Maturity is metadata, not folder promotion.
- Do not manufacture dates, statuses, priorities, projects, estimates, contexts, or
  reminders.
- If selected notes describe the same subject, do not merge them. Report the possible
  duplicate and propose a canonical relationship for review.
