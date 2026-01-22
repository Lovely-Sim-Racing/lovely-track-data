#!/usr/bin/env python3
"""Generate a single manifest.json at data/ containing all tracks across sims.

Each track entry includes the source game folder name to enable filtering.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


def load_track_data(track_file: Path) -> Dict[str, str]:
    """Load track data from JSON file and extract required fields.

    Returns minimal fields; game and full relative path are added by the generator.
    """
    with open(track_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    track_name = data.get("name") or data.get("trackName") or ""
    track_id = data.get("trackId") or ""
    
    if not track_id:
        raise ValueError(f"Missing trackId in {track_file}")
    
    return {
        "trackName": track_name,
        "trackId": track_id,
        "path": track_file.name,
    }


def generate_manifest(data_dir: Path) -> int:
    """Generate a single manifest.json in data_dir covering all sim folders.
    
    Structure:
    {
            "tracks": {
                "AssettoCorsa": [ { "trackName", "trackId", "path" }, ... ],
        "AssettoCorsaCompetizione": [ ... ],
        ...
      }
    }
    
    Returns the total number of tracks included. If no valid tracks are found,
    no manifest file is created and 0 is returned.
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    tracks_by_game: Dict[str, List[Dict[str, str]]] = {}
    errors_by_sim: Dict[str, List[str]] = {}

    # Iterate deterministic: sort sim folders then files within
    for sim_folder in sorted([p for p in data_dir.iterdir() if p.is_dir() and not p.name.startswith('.')], key=lambda p: p.name):
        sim_errors: List[str] = []
        sim_tracks: List[Dict[str, str]] = []
        for track_file in sorted(sim_folder.glob("*.json"), key=lambda p: p.name):
            if track_file.name == "manifest.json":
                # Ignore any existing per-sim manifests
                continue
            try:
                base = load_track_data(track_file)
                sim_tracks.append({
                    "trackName": base["trackName"],
                    "trackId": base["trackId"],
                    "path": f"{sim_folder.name}/{base['path']}",
                })
            except (json.JSONDecodeError, ValueError) as e:
                sim_errors.append(f"  {track_file.name}: {e}")
        if sim_errors:
            errors_by_sim[sim_folder.name] = sim_errors
        if sim_tracks:
            tracks_by_game[sim_folder.name] = sim_tracks

    # Print errors grouped by sim for visibility
    for sim_name, errs in errors_by_sim.items():
        print(f"⚠️  {sim_name}: Skipped {len(errs)} file(s)")
        for error in errs:
            print(error)

    total = sum(len(v) for v in tracks_by_game.values())
    if total == 0:
        return 0

    manifest = {"tracks": tracks_by_game}
    manifest_path = data_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"✓ Generated manifest with {total} total track(s) across sims")
    return total


def main() -> int:
    """Main entry point."""
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"

    try:
        count = generate_manifest(data_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # No tracks found is not considered an error for CLI purposes
    return 0


if __name__ == "__main__":
    sys.exit(main())
