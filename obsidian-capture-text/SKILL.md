---
name: obsidian-capture-text
description: Captures text from Telegram/Hermes, Codex, Claude, Obsidian, or a direct human request into a unique raw Markdown note, preserves it verbatim, rejects changed-content message-ID conflicts, queues safe single-writer daily-note linking, and returns a receipt. Use whenever the user says to capture, save, note, remember, or dump text into the vault.
---

# Capture Text

Use `scripts/capture_text.py` for every capture. It makes naming, idempotency,
and receipts deterministic across agents and devices. It intentionally does not edit the
shared daily note at ingestion time; one designated runner reconciles links after sync.

## Inputs

Collect:

- the text exactly as submitted;
- `source`, preferably `telegram`, `hermes`, `codex`, `claude`, `obsidian`, or
  `manual`;
- an external message/update ID when the source provides one;
- the source timestamp with timezone when available;
- an optional one-line summary only when it is unambiguous from the text.

Do not rewrite, trim, normalize, correct, or classify the submitted text.
Classification belongs to the separate review workflow.

## Run

From the vault root, pass arbitrary text through standard input so shell quoting
cannot change it:

```bash
python3 x/skills/obsidian-capture-text/scripts/capture_text.py \
  --vault . \
  --source telegram \
  --external-id '<provider message or update ID>' \
  --created '<ISO-8601 timestamp with timezone>' \
  --timezone Asia/Singapore \
  --text-file -
```

Omit `--external-id` only when the source has no stable ID. Omit `--created` to
use the current time. `--timezone` defaults to `Asia/Singapore` and converts
provider timestamps before selecting the daily note. Omit `--summary` unless a
factual one-line summary is obvious; never infer projects, people, tasks,
status, priority, or other classifications during capture.

The script must run against the vault root containing `00-Inbox/` and
`02-Calendar/`. Do not manually recreate its writes unless it is unavailable.

## Guarantees

The script:

1. Creates one collision-safe Markdown file in `00-Inbox/`.
2. Stores `created`, `source`, and `maturity: raw`; stores `externalId` and
   `summary` only when supplied.
3. Places the submitted text after frontmatter byte-for-byte, including its
   whitespace and final-newline state.
4. Treats the same `(source, external ID, exact content)` as the same capture on retry.
   If the ID already exists with changed text or metadata, it returns an error rather than
   silently discarding an edit.
5. Queues daily-note linking instead of editing a shared note from multiple devices.
6. Emits a JSON receipt with the capture path, created/duplicate status, and queued/missing
   daily-link state.

## Reconcile daily links

Before the daily review, run this once on the designated review machine after Obsidian Sync
has landed:

```bash
python3 x/skills/obsidian-capture-text/scripts/reconcile_daily_links.py \
  --vault . \
  --date YYYY-MM-DD \
  --timezone Asia/Singapore
```

The reconciler finds that date's unique capture notes and idempotently links each one under
`## 📥 Captures` in the existing daily note. It never creates a daily note. Do not schedule
this reconciler on more than one device.

## Safety

- Do not move, rename, delete, enrich, or classify the capture in this step.
- Do not create TaskNotes from implied intent.
- Do not create a missing daily note.
- Do not call the reconciler from every capture device; it is a single-writer maintenance step.
- If the script fails, return the error and leave the submitted text in the
  conversation so it can be retried with the same external ID.
- Return the script's receipt to the caller. For a human, render the path and
  link status concisely; for automation, preserve the JSON unchanged.
