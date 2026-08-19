#!/usr/bin/env python3
"""Reliably save a verbatim text capture into this Obsidian vault."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import NoReturn, TextIO
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


CAPTURE_HEADING = "## 📥 Captures"
SYNTHESIS_HEADING = "## 🤖 AI Synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault",
        default=".",
        help="Vault root (default: current directory)",
    )
    parser.add_argument("--source", required=True, help="Capture origin")
    parser.add_argument(
        "--external-id",
        help="Stable provider message/update ID used for retry deduplication",
    )
    parser.add_argument(
        "--created",
        help="ISO-8601 source timestamp; defaults to now in the vault timezone",
    )
    parser.add_argument(
        "--timezone",
        default="Asia/Singapore",
        help="Vault timezone used to select the daily note (default: Asia/Singapore)",
    )
    parser.add_argument(
        "--summary",
        help="Optional factual one-line summary; omit when interpretation is needed",
    )
    text_group = parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument("--text", help="Capture text (stdin is safer for arbitrary text)")
    text_group.add_argument(
        "--text-file",
        help="UTF-8 file containing the capture, or '-' to read standard input",
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    print(json.dumps({"status": "error", "error": message}), file=sys.stderr)
    raise SystemExit(2)


def parse_created(value: str | None, timezone_name: str) -> datetime:
    try:
        vault_timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        fail(f"unknown IANA timezone: {timezone_name}")
    if value is None:
        return datetime.now(vault_timezone)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        fail("--created must be a valid ISO-8601 timestamp")
    if parsed.tzinfo is None:
        fail("--created must include a timezone offset")
    return parsed.astimezone(vault_timezone)


def read_capture_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        text = args.text
    elif args.text_file == "-":
        try:
            text = sys.stdin.buffer.read().decode("utf-8")
        except UnicodeError as error:
            fail(f"capture text must be UTF-8: {error}")
    else:
        try:
            text = Path(args.text_file).read_bytes().decode("utf-8")
        except (OSError, UnicodeError) as error:
            fail(f"unable to read capture text: {error}")
    if not text.strip():
        fail("capture text cannot be empty or whitespace-only")
    return text


def yaml_string(value: str) -> str:
    # JSON double-quoted strings are valid YAML and escape newlines safely.
    return json.dumps(value, ensure_ascii=False)


def read_utf8_verbatim(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def source_slug(source: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", source.casefold()).strip("-")
    return (slug[:32] or "unknown").rstrip("-")


def build_note(
    text: str,
    created: datetime,
    source: str,
    external_id: str | None,
    summary: str | None,
) -> str:
    fields = [
        "---",
        f"created: {created.date().isoformat()}",
        f"source: {yaml_string(source)}",
        "maturity: raw",
    ]
    if external_id is not None:
        fields.append(f"externalId: {yaml_string(external_id)}")
    if summary is not None:
        fields.append(f"summary: {yaml_string(summary)}")
    fields.extend(["---", ""])
    return "\n".join(fields) + "\n" + text


def same_external_capture(note: str, source: str, external_id: str) -> bool:
    return (
        f"source: {yaml_string(source)}\n" in note
        and f"externalId: {yaml_string(external_id)}\n" in note
    )


def choose_capture_path(
    inbox: Path,
    created: datetime,
    source: str,
    external_id: str | None,
    text: str,
    expected_note: str,
) -> tuple[Path, bool]:
    slug = source_slug(source)
    if external_id is not None:
        seed = f"external\0{source}\0{external_id}".encode("utf-8")
        prefix = f"Capture - {slug}-"
    else:
        seed = (
            f"content\0{source}\0{created.isoformat()}\0{text}"
        ).encode("utf-8")
        prefix = f"{created.strftime('%Y-%m-%d %H%M%S%f')} - Capture - {slug}-"
    digest = hashlib.sha256(seed).hexdigest()

    for length in range(20, 65, 4):
        path = inbox / f"{prefix}{digest[:length]}.md"
        if not path.exists():
            return path, False
        try:
            existing = read_utf8_verbatim(path)
        except (OSError, UnicodeError) as error:
            fail(f"unable to inspect existing capture {path}: {error}")
        if external_id is not None:
            if same_external_capture(existing, source, external_id):
                if existing == expected_note:
                    return path, True
                fail(
                    "external ID already exists with different content; "
                    "refusing to discard an edit or reuse an ID"
                )
        elif existing == expected_note:
            return path, True
    fail("SHA-256 filename collision could not be resolved")


def created_date_from_note(note: str, fallback: datetime) -> str:
    match = re.search(r"(?m)^created: (\d{4}-\d{2}-\d{2})\s*$", note)
    return match.group(1) if match else fallback.date().isoformat()


def atomic_write(path: Path, text: str, mode: int | None = None) -> None:
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
        if mode is not None:
            os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    except OSError as error:
        if temporary_name:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
        fail(f"unable to write {path}: {error}")


def acquire_vault_lock(vault: Path) -> TextIO:
    vault_digest = hashlib.sha256(str(vault).encode("utf-8")).hexdigest()[:20]
    lock_path = Path(tempfile.gettempdir()) / f"obsidian-capture-text-{vault_digest}.lock"
    try:
        lock_handle = lock_path.open("a+", encoding="utf-8")
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
    except OSError as error:
        fail(f"unable to lock capture workflow for {vault}: {error}")
    return lock_handle


def add_daily_link(daily_note: Path, capture_stem: str) -> str:
    if not daily_note.exists():
        return "daily_note_missing"
    try:
        original = read_utf8_verbatim(daily_note)
        mode = stat.S_IMODE(daily_note.stat().st_mode)
    except (OSError, UnicodeError) as error:
        fail(f"unable to read daily note {daily_note}: {error}")

    link_line = f"- [[{capture_stem}]]"
    without_crlf = original.replace("\r\n", "")
    newline = "\r\n" if "\r\n" in original and "\n" not in without_crlf else "\n"
    lines = original.splitlines(keepends=True)
    heading_index = next(
        (index for index, line in enumerate(lines) if line.rstrip("\r\n") == CAPTURE_HEADING),
        None,
    )

    if heading_index is not None:
        section_end = next(
            (
                index
                for index in range(heading_index + 1, len(lines))
                if lines[index].startswith("## ")
            ),
            len(lines),
        )
        if any(
            line.rstrip("\r\n") == link_line
            for line in lines[heading_index + 1 : section_end]
        ):
            return "already_linked"
        insert_at = section_end
        while insert_at > heading_index + 1 and not lines[insert_at - 1].strip():
            insert_at -= 1
        if insert_at == heading_index + 1:
            lines[insert_at:insert_at] = [newline, link_line + newline]
        else:
            lines.insert(insert_at, link_line + newline)
        updated = "".join(lines)
    else:
        block = (
            f"{CAPTURE_HEADING}{newline}{newline}"
            f"{link_line}{newline}{newline}"
        )
        synthesis_index = next(
            (
                index
                for index, line in enumerate(lines)
                if line.rstrip("\r\n") == SYNTHESIS_HEADING
            ),
            None,
        )
        if synthesis_index is None:
            separator = (
                "" if not original or original.endswith(("\n", "\r")) else newline
            )
            updated = original + separator + newline + block
        else:
            lines.insert(synthesis_index, block)
            updated = "".join(lines)

    atomic_write(daily_note, updated, mode)
    return "linked"


def main() -> None:
    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    inbox = vault / "00-Inbox"
    calendar = vault / "02-Calendar"
    if not inbox.is_dir() or not calendar.is_dir():
        fail("--vault must contain 00-Inbox/ and 02-Calendar/")
    lock_handle = acquire_vault_lock(vault)

    source = args.source.strip()
    if not source:
        fail("--source cannot be empty")
    if args.external_id is not None and not args.external_id:
        fail("--external-id cannot be empty")
    if args.summary is not None:
        summary = args.summary.strip()
        if not summary:
            fail("--summary cannot be empty")
        if "\n" in summary or "\r" in summary:
            fail("--summary must be one line")
    else:
        summary = None

    created = parse_created(args.created, args.timezone)
    text = read_capture_text(args)
    expected_note = build_note(text, created, source, args.external_id, summary)
    capture_path, duplicate = choose_capture_path(
        inbox,
        created,
        source,
        args.external_id,
        text,
        expected_note,
    )

    if duplicate:
        try:
            stored_note = read_utf8_verbatim(capture_path)
        except (OSError, UnicodeError) as error:
            fail(f"unable to read duplicate capture {capture_path}: {error}")
    else:
        try:
            with capture_path.open("x", encoding="utf-8", newline="") as capture_file:
                capture_file.write(expected_note)
                capture_file.flush()
                os.fsync(capture_file.fileno())
            stored_note = expected_note
        except FileExistsError:
            # Another process may have won an idempotent race. Re-run selection.
            capture_path, duplicate = choose_capture_path(
                inbox,
                created,
                source,
                args.external_id,
                text,
                expected_note,
            )
            if not duplicate:
                fail("concurrent filename collision; retry with the same inputs")
            stored_note = read_utf8_verbatim(capture_path)
        except OSError as error:
            fail(f"unable to create capture {capture_path}: {error}")

    capture_date = created_date_from_note(stored_note, created)
    daily_note = calendar / f"{capture_date}.md"
    # Do not read-modify-write a shared daily note from every capture device.
    # A single designated runner reconciles these links after Obsidian Sync lands.
    daily_link = "queued" if daily_note.exists() else "daily_note_missing"

    receipt = {
        "status": "duplicate" if duplicate else "created",
        "capture_path": capture_path.relative_to(vault).as_posix(),
        "source": source,
        "external_id": args.external_id,
        "created_date": capture_date,
        "daily_note": (
            daily_note.relative_to(vault).as_posix() if daily_note.exists() else None
        ),
        "daily_link": daily_link,
    }
    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
    lock_handle.close()
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
