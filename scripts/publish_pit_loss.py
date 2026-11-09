#!/usr/bin/env python3
"""Update the track files' pit loss from the Lovely API (the weekly GitHub Action, .github/workflows/pit-loss.yml).

The API combines what drivers' plugins upload from online races. Its export (GET /pit-loss-export) lists every
complete sim + track + class (enough races) in the track data's terms:
  pit / dt           whole seconds a normal stop / a drive-through loses   -> the class's "time" entries
  pitEntry / pitExit where on the lap (0-1) the pit lane starts / ends     -> the file's "pitentry" / "pitexit"
Names are the data repos' own: sim = the data folder, track = the track file's name (or found through the
manifest, as the API's track-data endpoint does), class = the car data's class (lower case).

- The API's values replace the file's when they differ.
- Tracks without a file in the repo are skipped (listed in the summary): a new file needs more than pit data.
- Files are written in the repo's own format (pre-commit pretty-format-json: 2 spaces, keys unsorted, non-ASCII kept).
- The summary (markdown) is the pull request's description: what changed, old -> new, and the evidence.

Usage:
  PIT_EXPORT_TOKEN=... python scripts/publish_pit_loss.py --summary summary.md
  python scripts/publish_pit_loss.py --export export.json --summary summary.md     (an export saved to a file)
  python scripts/publish_pit_loss.py --export export.json --dry-run               (show, change nothing)
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

EXPORT_URL = os.environ.get("PIT_EXPORT_URL", "https://api.lsr.gg/pit-loss-export")
DATA = Path(__file__).resolve().parent.parent / "data"

# A change this big is flagged in the summary, to check before merging
BIG_CHANGE_SECONDS = 5
BIG_CHANGE_SHARE = 0.15


def name_cleaner(name: str) -> str:
    """The data repos' "processed" form of a name, as the API's GitHubService::nameCleaner makes it."""
    name = str(name).lower()
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"[^a-z0-9]", "-", name)
    name = re.sub(r"-+", "-", name)
    return name.strip("-")


def load_export(path):
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    token = os.environ.get("PIT_EXPORT_TOKEN", "")
    if not token:
        sys.exit("PIT_EXPORT_TOKEN is not set (the repository secret)")
    request = urllib.request.Request(EXPORT_URL, headers={"Authorization": "Bearer " + token, "User-Agent": "lovely-track-data-action"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def find_track_file(sim: str, track: str, manifest: dict):
    """data/<sim>/<track>.json, else the file the manifest lists for that track id or name; None when there's none."""
    direct = DATA / sim / (track + ".json")
    if direct.is_file():
        return direct
    for entry in manifest.get("tracks", {}).get(sim, []):
        if name_cleaner(entry.get("trackId", "")) == track or name_cleaner(entry.get("trackName", "")) == track:
            candidate = DATA / entry.get("path", "")
            if candidate.is_file():
                return candidate
    return None


def time_block(data: dict) -> dict:
    """The file's "time" object (a list holding one object in the v2 format); created when missing."""
    time = data.get("time")
    if isinstance(time, list):
        if not time or not isinstance(time[0], dict):
            data["time"] = time = [{}]
        return time[0]
    if isinstance(time, dict):
        return time
    data["time"] = [{}]
    return data["time"][0]


def set_class_delays(block: dict, car_class: str, values: dict) -> dict:
    """Write pit / dt for a class (its key: the car data's class). Returns {name: old value} for what changed."""
    key = next((k for k in block if k == car_class), None) or next((k for k in block if k.lower() == car_class), None)
    if key is None:
        block[car_class] = []
        key = car_class
    elif key != car_class:
        # Another spelling of the class: renamed in place to the car data's (keys keep their order)
        items = list(block.items())
        block.clear()
        block.update((car_class if k == key else k, v) for k, v in items)
        key = car_class
    entries = block[key]
    changed = {}
    for name in ("pit", "dt"):
        value = values.get(name)
        if value is None:
            continue
        entry = next((e for e in entries if isinstance(e, dict) and e.get("name") == name), None)
        if entry is None:
            entries.append({"name": name, "time": value})
            changed[name] = None
        elif entry.get("time") != value:
            changed[name] = entry.get("time")
            entry["time"] = value
    return changed


def big_change(old, new) -> bool:
    if old is None or new is None:
        return False
    return abs(new - old) >= BIG_CHANGE_SECONDS or (old > 0 and abs(new - old) / old >= BIG_CHANGE_SHARE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--export", help="read the export from this file instead of the API")
    parser.add_argument("--summary", help="write the pull request's description (markdown) here")
    parser.add_argument("--dry-run", action="store_true", help="show the changes, write no files")
    args = parser.parse_args()

    export = load_export(args.export)
    combos = export.get("combos", [])
    with open(DATA / "manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Combos by track file
    by_file = {}
    missing = []
    for combo in combos:
        path = find_track_file(combo["sim"], combo["track"], manifest)
        if path is None:
            missing.append(combo)
        else:
            by_file.setdefault(path, []).append(combo)

    rows = []
    written = []
    for path, file_combos in sorted(by_file.items()):
        original = path.read_text(encoding="utf-8")
        data = json.loads(original)
        block = time_block(data)
        file_changed = False
        for combo in file_combos:
            changed = set_class_delays(block, combo["class"], {"pit": combo.get("pit"), "dt": combo.get("dt")})
            if changed:
                file_changed = True
                rows.append((path, combo, changed))

        # The pit lane's ends: from the class with the most races
        with_points = [c for c in file_combos if c.get("pitEntry") is not None and c.get("pitExit") is not None]
        if with_points:
            best = max(with_points, key=lambda c: c.get("races", 0))
            for field, value in (("pitentry", best["pitEntry"]), ("pitexit", best["pitExit"])):
                old = data.get(field)
                if not isinstance(old, (int, float)) or abs(old - value) > 0.0005:
                    data[field] = value
                    file_changed = True
                    rows.append((path, {"class": "(track)", field: value, "source": best["class"], "races": best.get("races")}, {field: old}))

        if file_changed:
            text = json.dumps(data, indent=2, ensure_ascii=False) + ("\n" if original.endswith("\n") else "")
            if not args.dry_run:
                path.write_text(text, encoding="utf-8")
            written.append(path)

    summary = build_summary(export, rows, written, missing)
    if args.summary:
        Path(args.summary).write_text(summary, encoding="utf-8")
    print(summary)

    # For the workflow: whether there's anything to propose
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as f:
            f.write("changed=%s\n" % ("true" if written else "false"))
    return 0


def build_summary(export, rows, written, missing) -> str:
    lines = ["Pit loss from the Lovely API (export %s)." % export.get("generated", "?"), ""]
    if not written:
        lines.append("Nothing changed: every complete combo already matches the track files.")
    else:
        lines += [
            "Values combined from drivers' online races (one vote per race): **pit** = a normal stop, **dt** = a "
            "drive-through, in whole seconds lost; **pitentry / pitexit** = where on the lap the pit lane starts and ends.",
            "",
            "| File | Class | Value | Old | New | Races | Spread (lane / standing) | Notes |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for path, combo, changed in rows:
            rel = path.relative_to(DATA).as_posix()
            for name, old in changed.items():
                if name in ("pit", "dt"):
                    new = combo.get(name)
                    spread = "%s / %s" % (combo.get("laneSpread"), combo.get("standingSpread"))
                    notes = []
                    if name == "dt":
                        notes.append("%s (%s races)" % (combo.get("dtSource"), combo.get("dtRaces")))
                    if big_change(old, new):
                        notes.append("**big change, check**")
                    if old is None:
                        notes.append("new")
                    lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                        rel, combo["class"], name, "-" if old is None else old, new, combo.get("races"), spread, ", ".join(notes)))
                else:
                    lines.append("| %s | %s | %s | %s | %s | %s | | from %s |" % (
                        rel, combo["class"], name, "-" if old is None else old, combo.get(name), combo.get("races"), combo.get("source")))
        lines += ["", "%d file(s) updated." % len(written)]
    if missing:
        lines += ["", "Not in the repo (skipped, a new track file needs more than pit data):", ""]
        for combo in missing:
            lines.append("- %s / %s, class %s (%s races): pit %s, dt %s" % (
                combo["sim"], combo["track"], combo["class"], combo.get("races"), combo.get("pit"), combo.get("dt")))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
