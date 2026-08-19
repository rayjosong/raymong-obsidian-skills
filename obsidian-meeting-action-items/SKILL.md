---
name: obsidian-meeting-action-items
description: Search Google Drive through the gws CLI for meeting notes, extract evidence-backed action items assigned to Raymond Ong or explicitly named people, and report ownership, source, and stated deadlines. Use for requests to find meeting action items for today or a specified date; optional vault integration only proposes TaskNotes or daily-review inputs.
---

# Meeting Action Items

## Key Features
- **Default mode:** Searches for action items assigned to you (Raymond Ong) only
- **Expandable:** Optionally specify additional people (e.g., "Liyun", "Dmitry Gorbov", "Chi Hen Foo", "Arseniy")
- **Smart search:** Finds meeting notes, agendas, summaries, and recaps modified on a specified date
- **Clear output:** Formats action items with owner, source, and deadline
- **Optional Obsidian integration:** Can propose TaskNotes or structured input for the
  combined daily-review workflow

## Prerequisites

All Google Drive/Docs access in this skill goes through the `gws` (Google Workspace CLI) tool. Run these checks silently; only surface them if the user needs to act.

**1. `gws` is installed**
```bash
gws --version
```
If this fails: `brew install googleworkspace-cli`, then stop until it's resolved.

**2. Authentication (lazy — try the command first)**

Run the intended `gws` command directly. **Only if it returns 401 Unauthorized**, run this token-refresh block silently, then retry once:

```bash
export GCLOUD_SDK_ROOT=$(gcloud info --format="value(installation.sdk_root)")
export PYTHONPATH="$GCLOUD_SDK_ROOT/lib/third_party:$GCLOUD_SDK_ROOT/lib"
export GOOGLE_WORKSPACE_CLI_TOKEN=$(python3 -c "import google.auth; from google.auth.transport.requests import Request; scopes=['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/documents.readonly']; creds,project=google.auth.default(scopes=scopes); creds.refresh(Request()) if not creds.valid else None; print(creds.token)")
```

Notes:
- Auth here rides on **Application Default Credentials**, not gws-native OAuth — `gws auth status` reports `auth_method: "none"` on this machine, which is expected and not the problem. Do not run `gws auth login`.
- **Never echo `GOOGLE_WORKSPACE_CLI_TOKEN`** or any part of it to the user.
- If the token block itself fails (Python/gcloud error), ADC is not set up. Report the
  exact failed prerequisite and stop rather than inventing an authentication sequence.

## Instructions

### 1. Determine Scope
- **If no names specified:** Search for action items assigned to "Raymond Ong" only
- **If names provided:** Include all specified names + Raymond Ong
- **Supported names:** Raymond Ong, Liyun, Dmitry Gorbov (or Dmitry), Chi Hen Foo (or Chi Hen), Arseniy (or variations/initials)

### 2. Search Google Drive (`gws drive files list`)

Search for meeting-related Google Docs modified on the target date. One query covers all title keywords:

```bash
gws drive files list --params '{
  "q": "mimeType=\"application/vnd.google-apps.document\" and trashed = false and (name contains \"Meeting\" or name contains \"Notes\" or name contains \"Standup\" or name contains \"Sync\" or name contains \"1:1\" or name contains \"Agenda\" or name contains \"Plan\" or name contains \"Recap\" or name contains \"Summary\") and modifiedTime >= \"YYYY-MM-DDT00:00:00+08:00\" and modifiedTime <= \"YYYY-MM-DDT23:59:59+08:00\"",
  "orderBy": "modifiedTime desc",
  "pageSize": 50,
  "fields": "files(id,name,modifiedTime,webViewLink)"
}'
```

- **Search targets:** Documents titled with "Meeting", "Notes", "Standup", "Sync", "1:1", "Agenda", "Plan", "Recap", "Summary"
- **Date filter:** Default to today; accept a custom date parameter. Substitute the date into **both** `modifiedTime` bounds, and keep the **local UTC offset** (`+08:00`) rather than `Z` — using `Z` shifts the window and silently drops early-morning or late-evening meetings.
- **Ordering:** `orderBy: "modifiedTime desc"` puts the most recently touched docs first.
- **Empty result:** `name contains` matches the **title only**. If the query returns no files, retry once with a content search over the same window (`fullText contains \"action items\"` plus the same `modifiedTime` bounds) before reporting "no documents found".
- **Paging:** add `--page-all` if more than 50 matches are plausible (broad date range or many recurring-notes docs).
- **Editing the query:** validate any change with `--dry-run` first — it checks the JSON `--params` and escaped `q` locally without spending an API call.

### 3. Extract Action Items (`gws drive files export`)

Export each document found in step 2 as plain text, using the `id` from the search results, then read the resulting file.

**`gws drive files export` writes to a file, not stdout** — and `--output` is rejected unless it's a **relative path inside the current directory**. So always run it from a scratch directory outside the vault (your session scratchpad, or `$TMPDIR`):

```bash
cd /path/to/scratch && gws drive files export \
  --params '{"fileId": "FILE_ID", "mimeType": "text/plain"}' \
  --output ./FILE_ID.txt
```

Then read `FILE_ID.txt` and parse it. The command prints only a JSON status blob (`{"bytes": …, "saved_file": …, "status": "success"}`) — the notes text is in the file.

- **Never run the export with the vault as the working directory.** With no `--output` it silently writes `download.txt` into the current directory, which litters the vault; with an absolute `--output` it fails with a `400 validationError` ("resolves to … outside the current directory").
- **Sanitize `FILE_ID`** before interpolating it into the command: allow only alphanumerics, `-`, and `_`. If an ID contains any of `; & | > < ` $ ( )`, do not run the command — ask for clarification instead.
- **Per-file failures are expected, not bugs.** A `403`, `404`, or "entity not found" means the doc was deleted or access was revoked. Log the document title as unreadable, skip it, and list it in the output as a gap so the user knows the result isn't necessarily complete. Never guess at content for a doc you couldn't read.
- **Don't dump exported docs.** Meeting notes are long and contain other people's material — extract only the action-item lines and keep the rest in context.

For each document read:
- Scan for action items:
  - **"Notes by Gemini" docs** (the most common case) put them under a `Next steps` heading as `* [Full Name] Short title: Description`. Note that a running notes doc for a recurring meeting can repeat the same `Next steps` block across sessions — deduplicate by near-identical text.
  - Explicit assignments: "- [Person]: [Task]" or "Action: [Person] to [Task]"
  - Implicit assignments: Context shows a person is responsible for a follow-up
  - Marked tasks: Bullet points, checkboxes, or "TODO" patterns
- Extract:
  - **Task description** (clear, actionable wording)
  - **Assigned person** (exact match from search scope)
  - **Due date** (if mentioned; otherwise "Not specified")
  - **Source** (meeting/document title)

### 4. Format & Output
Return action items in this format:

```
## 📅 Action Items for [Date]

### [Person's Name]
- **Task:** [Clear description]
  - **Source:** [Document/Meeting title]
  - **Due:** [Deadline or "Not specified"]

### [Other Person]
- **Task:** [Description]
  - **Source:** [Document/Meeting title]
  - **Due:** [Deadline]

---

### Summary Table
| Person | Action Item Count | Key Focus / Primary Task |
| :--- | :--- | :--- |
| Raymond Ong | 3 | [Primary focus from items] |
| Liyun | 1 | [Primary focus from items] |
```

### 5. Obsidian Integration (Optional)

If invoked from the vault:

- Keep the standalone extraction as the source report.
- For actions explicitly assigned to Raymond, propose exact TaskNotes entries in
  `06-Tasks/` using the existing Task Template and preserving all TaskNotes conventions.
- If the extraction is part of the evening workflow, pass source-linked candidates to
  `obsidian-daily-review-batch` so its stable proposal IDs and approval log remain the
  single review surface.
- Do not create a competing `## ✅ Action Items` section in the daily note.
- Do not create TaskNotes or modify daily notes until the user approves the exact
  proposal.

### 6. Report Results
- Display all action items grouped by person
- Show source documents scanned
- Count action items per person
- For Raymond's assigned actions, optionally show the proposal-only TaskNotes or
  daily-review route

## Parameters
- **Date:** Defaults to today; accepts custom date (e.g., "2026-08-10")
- **People:** Defaults to Raymond Ong; accepts comma-separated list
- **Obsidian integration:** Defaults to standalone output; optionally propose TaskNotes
  or daily-review inputs

## Example Invocations

**Default (today, you only):**
```
/meeting-action-items
```

**With additional people:**
```
/meeting-action-items for Liyun, Dmitry, and Chi Hen Foo
```

**Custom date:**
```
/meeting-action-items for 2026-08-10
```

**Combined:**
```
/meeting-action-items for Liyun and Arseniy on 2026-08-09
```

## Error Handling

| Error | Meaning | What to do |
|---|---|---|
| `401 Unauthorized` | Access token expired (they last ~1 hour) | Run the token-refresh block from **Prerequisites**, retry once |
| `403 Forbidden` / insufficient scopes | Drive/Docs not authorized | Report the missing authorization and stop; do not improvise an auth change |
| `403` / `404` on a single file export | That doc was deleted or access revoked | Expected; log as unreadable, skip, report as a gap |
| `429 Too Many Requests` | Too many API calls in a short window | Wait ~60s and retry; back off further if it repeats |
| `SERVICE_DISABLED` | API off for the active GCP project | Report the active project and disabled API; stop for user/admin resolution |
| `400 validationError` on `--output` | `--output` was given an absolute path, or one outside cwd | `cd` to a scratch dir first and pass a relative `./name.txt` |
| `gws: command not found` | CLI not installed | `brew install googleworkspace-cli` |
| Docs API 403 | Expected — the Docs API isn't enabled | Use `gws drive files export` with `text/plain` (as this skill already does) |

## Implementation Notes
- **All Drive/Docs access goes through `gws`.** Do not switch to a Drive connector when
  one is available; the CLI path preserves the approved authentication and export
  behavior across agents.
- **Treat meeting notes as sensitive internal content.** Keep processing in the current
  approved execution context; do not persist or forward raw exports outside it.
- Search should be case-insensitive for names
- Default to today's date if unspecified
- If no action items found, report clearly: "No action items found for [date]"
- Verify all assignments match actual text (don't over-infer)
- If an Obsidian vault is detected, offer proposal-only integration; always provide the
  standalone output first.
- Run standalone or feed the combined daily-review workflow without creating another
  approval surface.
