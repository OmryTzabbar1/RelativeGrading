#!/usr/bin/env python3
"""Grade all submissions in WorkSubmissions05"""
import subprocess
import sys
from pathlib import Path

base_dir = Path(__file__).parent
orchestrator = base_dir.parent / ".claude" / "skills" / "tier2-orchestrator" / "orchestrate.py"

# List all folders with their repos
submissions = []
for folder in sorted(base_dir.glob("Participant_*")):
    participant_id = folder.name.split('_')[1]

    # Find the cloned repo (look for directories, skip PDF and Excel)
    repos = [d for d in folder.iterdir() if d.is_dir()]

    if repos:
        repo_path = repos[0]  # Take first repo folder
        submissions.append((participant_id, str(repo_path)))

print(f"Found {len(submissions)} submissions to grade\n")

success = 0
failed = 0

for i, (participant_id, repo_path) in enumerate(submissions, 1):
    print(f"[{i}/{len(submissions)}] Grading {participant_id}... ", end='', flush=True)

    try:
        result = subprocess.run(
            [sys.executable, str(orchestrator), repo_path, participant_id, "Assignment 5"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            # Extract score from output
            for line in result.stdout.split('\n'):
                if "Total Score:" in line:
                    score = line.split(':')[1].split('/')[0].strip()
                    print(f"OK ({score}/100)")
                    break
            success += 1
        else:
            print(f"FAILED")
            failed += 1
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        failed += 1
    except Exception as e:
        print(f"ERROR: {str(e)[:30]}")
        failed += 1

print(f"\n{'='*60}")
print(f"Grading complete!")
print(f"  Success: {success}")
print(f"  Failed: {failed}")
print(f"{'='*60}")
