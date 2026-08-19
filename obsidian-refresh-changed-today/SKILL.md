---
name: obsidian-refresh-changed-today
description: Refresh the materialized Changed Today section of the current Obsidian daily note with Markdown files modified today. Use when the user asks to refresh or inspect today's changed-file list, or when an agent-neutral session-start workflow needs to update it.
---

# Refresh Changed Today

## Run

1. Resolve the vault root as the directory containing `AGENTS.md`, `02-Calendar/`, and
   `x/scripts/update_changed_today.js`.
2. From that vault root, run:

   ```bash
   node x/scripts/update_changed_today.js
   ```

   The script resolves the vault from its own filesystem location, so it does not depend
   on a Claude-, Codex-, or shell-specific project environment variable.
3. Read stdout. A successful update reports
   `update_changed_today: N file(s) changed on YYYY-MM-DD -> 02-Calendar/YYYY-MM-DD.md`.
4. Optionally verify the region between `<!-- BEGIN changed-today -->` and
   `<!-- END changed-today -->` in the daily note.

If today's daily note does not exist, the script exits successfully without output. Tell
the user the day has not been started; do not create the note.

## Guarantees

- The script writes real wikilinks, newest first, capped at 50 entries with an overflow
  line. It derives committed changes from today's Git history and includes current dirty
  Markdown files only when their mtime is today, so cloning or creating a worktree does
  not make every file look newly edited.
- It excludes hidden directories, maintenance content, and the daily note itself.
- It excludes generated Daily Review and Work Evidence notes so refreshing review state
  cannot create a Changed Today/review feedback loop.
- It requires either exactly one ordered marker pair or no markers. Duplicate or
  mismatched markers fail without modifying the note.
- It uses a local single-run lock and a unique same-directory temporary file, atomically
  replaces only the marker region, and is idempotent.
- The list is a point-in-time view of Git history plus today's dirty files. Re-run it
  after later edits or commits.
