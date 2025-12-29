#!/usr/bin/env python3
"""Clone all repositories for WorkSubmissions05"""
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).parent

# Find all participant folders
folders = sorted([d for d in base_dir.iterdir()
                 if d.is_dir() and d.name.startswith('Participant_')])

clone_script = Path(__file__).parent.parent / ".claude" / "skills" / "tier2-orchestrator" / "clone_repo.py"

success = 0
already_exists = 0
failed = 0

for folder in folders:
    participant_id = folder.name.split('_')[1]
    print(f"Processing {participant_id}... ", end='', flush=True)

    try:
        result = subprocess.run(
            [sys.executable, str(clone_script), str(folder)],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            if "already exists" in result.stdout:
                print("OK (already exists)")
                already_exists += 1
            else:
                print("OK (cloned)")
                success += 1
        else:
            print(f"FAILED {result.stderr[:50]}")
            failed += 1
    except Exception as e:
        print(f"ERROR {str(e)[:50]}")
        failed += 1

print(f"\n{'='*60}")
print(f"Summary: {success} cloned, {already_exists} existing, {failed} failed")
print(f"{'='*60}")
