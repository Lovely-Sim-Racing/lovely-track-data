# Manifest Generator

Generates a single `manifest.json` at `data/` containing all tracks across supported sim game folders. This makes it easy for consuming applications to discover available tracks globally and filter by game.

## Usage

```bash
python3 scripts/generate_manifest.py
```

The script will:
- Scan all subdirectories in `data/`
- Read each track JSON file (ignoring any existing per-sim `manifest.json` files)
- Extract `trackName`, `trackId`, and filename (trackName is derived from the source `name` field when present)
- Generate a single `data/manifest.json` with entries including the game name
- Report any errors or invalid files per game folder

## Output Format

The root `data/manifest.json` contains:

```json
{
  "tracks": {
    "AssettoCorsa": [
      {
        "trackName": "Lime Rock Park",
        "trackId": "limerock",
        "path": "AssettoCorsa/limerock.json"
      }
    ],
    "AssettoCorsaCompetizione": [
      { "trackName": "Suzuka", "trackId": "suzuka", "path": "AssettoCorsaCompetizione/suzuka.json" }
    ]
  }
}
```

Notes:
- Top-level `tracks` is an object keyed by game folder name.
- Each game contains an array of track entries.
- `path` is relative to `data/` and includes the game folder.

## Testing

Run the test suite:

```bash
python3 scripts/test_generate_manifests.py
```

For verbose output:

```bash
python3 scripts/test_generate_manifests.py -v
```

## Requirements

- Python 3.6+
- No external dependencies

## Error Handling

The script will:
- Skip files with invalid JSON
- Skip files missing required `trackId` field
- Report all errors but continue processing, grouped per game folder
- Only create the root manifest if at least one valid track exists
