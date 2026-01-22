#!/usr/bin/env python3
"""Tests for track manifest generation."""

import json
import tempfile
import unittest
from pathlib import Path

import generate_manifest


class TestGenerateManifest(unittest.TestCase):
    """Test suite for single root manifest generation."""
    
    def setUp(self):
        """Create temporary test directory structure."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name) / "data"
        self.data_dir.mkdir()
    
    def tearDown(self):
        """Clean up temporary directory."""
        self.temp_dir.cleanup()
    
    def create_track_file(self, sim_name: str, filename: str, track_data: dict):
        """Helper to create a track JSON file."""
        sim_dir = self.data_dir / sim_name
        sim_dir.mkdir(exist_ok=True)
        track_file = sim_dir / filename
        with open(track_file, 'w', encoding='utf-8') as f:
            json.dump(track_data, f)
        return track_file
    
    def test_load_track_data_valid(self):
        """Test loading valid track data."""
        track_file = self.create_track_file("TestSim", "test_track.json", {
            "name": "Test Track",
            "trackId": "test_track",
            "year": 2025
        })
        
        result = generate_manifest.load_track_data(track_file)
        
        self.assertEqual(result["trackName"], "Test Track")
        self.assertEqual(result["trackId"], "test_track")
        self.assertEqual(result["path"], "test_track.json")
    
    def test_load_track_data_missing_track_name(self):
        """Test loading track data with missing name (should use empty string)."""
        track_file = self.create_track_file("TestSim", "test_track.json", {
            "trackId": "test_track"
        })
        
        result = generate_manifest.load_track_data(track_file)
        
        self.assertEqual(result["trackName"], "")
        self.assertEqual(result["trackId"], "test_track")
    
    def test_load_track_data_missing_track_id(self):
        """Test loading track data with missing trackId (should raise error)."""
        track_file = self.create_track_file("TestSim", "test_track.json", {
            "name": "Test Track"
        })
        
        with self.assertRaises(ValueError):
            generate_manifest.load_track_data(track_file)
    
    def test_load_track_data_unicode(self):
        """Test loading track data with unicode characters."""
        track_file = self.create_track_file("TestSim", "test_track.json", {
            "name": "Autódromo José Carlos Pace",
            "trackId": "interlagos"
        })
        
        result = generate_manifest.load_track_data(track_file)
        
        self.assertEqual(result["trackName"], "Autódromo José Carlos Pace")
    
    def test_generate_manifest_single_track(self):
        """Generate single root manifest with one track in one sim."""
        self.create_track_file("TestSim", "track1.json", {
            "name": "Track 1",
            "trackId": "track_1"
        })

        count = generate_manifest.generate_manifest(self.data_dir)

        self.assertEqual(count, 1)

        manifest_file = self.data_dir / "manifest.json"
        self.assertTrue(manifest_file.exists())

        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        self.assertIn("TestSim", manifest["tracks"])
        self.assertEqual(len(manifest["tracks"]["TestSim"]), 1)
        self.assertEqual(manifest["tracks"]["TestSim"][0]["trackName"], "Track 1")
        self.assertEqual(manifest["tracks"]["TestSim"][0]["path"], "TestSim/track1.json")
    
    def test_generate_manifest_multiple_tracks_across_sims(self):
        """Generate root manifest with multiple tracks across sims and sorted."""
        self.create_track_file("TestSimA", "track2.json", {
            "name": "Track 2",
            "trackId": "track_2"
        })
        self.create_track_file("TestSimA", "track1.json", {
            "name": "Track 1",
            "trackId": "track_1"
        })
        self.create_track_file("TestSimB", "alpha.json", {
            "name": "Alpha",
            "trackId": "alpha"
        })

        count = generate_manifest.generate_manifest(self.data_dir)
        self.assertEqual(count, 3)

        with open(self.data_dir / "manifest.json", 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        tracks = manifest["tracks"]
        self.assertIn("TestSimA", tracks)
        self.assertIn("TestSimB", tracks)
        self.assertEqual([c["path"] for c in tracks["TestSimA"]], ["TestSimA/track1.json", "TestSimA/track2.json"])
        self.assertEqual([c["path"] for c in tracks["TestSimB"]], ["TestSimB/alpha.json"])
    
    def test_generate_manifest_sorted_order_within_sims(self):
        """Tracks are sorted alphabetically by filename within each sim and sims are sorted."""
        self.create_track_file("SimZ", "zebra.json", {"name": "Zebra", "trackId": "zebra"})
        self.create_track_file("SimZ", "alpha.json", {"name": "Alpha", "trackId": "alpha"})
        self.create_track_file("SimA", "beta.json", {"name": "Beta", "trackId": "beta"})

        generate_manifest.generate_manifest(self.data_dir)

        with open(self.data_dir / "manifest.json", 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        tracks = manifest["tracks"]
        self.assertIn("SimA", tracks)
        self.assertIn("SimZ", tracks)
        self.assertEqual([c["path"] for c in tracks["SimA"]], ["SimA/beta.json"])
        self.assertEqual([c["path"] for c in tracks["SimZ"]], ["SimZ/alpha.json", "SimZ/zebra.json"])
    
    def test_generate_manifest_skips_invalid_files(self):
        """Invalid files are skipped and only valid tracks are output."""
        self.create_track_file("TestSim", "valid.json", {"name": "Valid", "trackId": "valid"})
        self.create_track_file("TestSim", "invalid.json", {"name": "Invalid"})

        count = generate_manifest.generate_manifest(self.data_dir)

        self.assertEqual(count, 1)

        with open(self.data_dir / "manifest.json", 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        self.assertIn("TestSim", manifest["tracks"])
        self.assertEqual(len(manifest["tracks"]["TestSim"]), 1)
        self.assertEqual(manifest["tracks"]["TestSim"][0]["trackId"], "valid")
    
    def test_generate_manifest_empty_data_dir(self):
        """No manifest is created when there are no tracks across sims."""
        (self.data_dir / "EmptySim").mkdir()

        count = generate_manifest.generate_manifest(self.data_dir)

        self.assertEqual(count, 0)
        self.assertFalse((self.data_dir / "manifest.json").exists())
    
    def test_generate_manifest_ignores_existing_per_sim_manifest(self):
        """Existing per-sim manifest files are ignored during aggregation."""
        self.create_track_file("TestSim", "track1.json", {"name": "Track 1", "trackId": "track_1"})

        sim_dir = self.data_dir / "TestSim"
        with open(sim_dir / "manifest.json", 'w') as f:
            json.dump({"tracks": []}, f)

        count = generate_manifest.generate_manifest(self.data_dir)
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
