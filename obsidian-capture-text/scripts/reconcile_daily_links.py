#!/usr/bin/env python3
"""Link a day's unique capture notes from one designated vault writer."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from capture_text import acquire_vault_lock, add_daily_link, fail, read_utf8_verbatim


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root")
    parser.add_argument("--date", help="Local YYYY-MM-DD; defaults to today")
    parser.add_argument("--timezone", default="Asia/Singapore")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    inbox = vault / "00-Inbox"
    calendar = vault / "02-Calendar"
    if not inbox.is_dir() or not calendar.is_dir():
        fail("--vault must contain 00-Inbox/ and 02-Calendar/")

    review_date = args.date or datetime.now(ZoneInfo(args.timezone)).date().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", review_date):
        fail("--date must be YYYY-MM-DD")
    daily_note = calendar / f"{review_date}.md"
    if not daily_note.exists():
        print(json.dumps({
            "status": "daily_note_missing",
            "review_date": review_date,
            "daily_note": None,
            "capture_count": 0,
            "linked": 0,
        }, sort_keys=True))
        return

    lock_handle = acquire_vault_lock(vault)
    captures: list[Path] = []
    created_pattern = re.compile(rf"(?m)^created: {re.escape(review_date)}\s*$")
    for path in sorted(inbox.glob("*.md"), key=lambda candidate: candidate.name.casefold()):
        if "Capture -" not in path.name:
            continue
        try:
            note = read_utf8_verbatim(path)
        except (OSError, UnicodeError) as error:
            fail(f"unable to inspect capture {path}: {error}")
        if created_pattern.search(note):
            captures.append(path)

    linked = 0
    already_linked = 0
    for capture in captures:
        result = add_daily_link(daily_note, capture.stem)
        if result == "linked":
            linked += 1
        elif result == "already_linked":
            already_linked += 1

    lock_handle.close()
    print(json.dumps({
        "status": "success",
        "review_date": review_date,
        "daily_note": daily_note.relative_to(vault).as_posix(),
        "capture_count": len(captures),
        "linked": linked,
        "already_linked": already_linked,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
