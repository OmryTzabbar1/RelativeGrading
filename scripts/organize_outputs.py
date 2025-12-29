#!/usr/bin/env python3
"""
Organize evaluation outputs into submission-specific folders
Run this after evaluation to move outputs from outputs/ to outputs/{submission_name}/
"""

import sys
import os
import shutil
from pathlib import Path

def organize_outputs(submission_name):
    """Move outputs from outputs/ to outputs/{submission_name}/"""

    source_dir = "outputs"
    dest_dir = f"outputs/{submission_name}"

    # Create destination directory
    os.makedirs(dest_dir, exist_ok=True)

    # Files to move
    files_to_move = [
        "criteria_graph_final.json",
        "grades.xlsx",
        "Student_Evaluation_Report.xlsx",
        "EVALUATION_SUMMARY.md",
        "README.md",
        "QUALITY_STANDARDS_REPORT.md",
        f"grade_comparison_{submission_name.lower()}.xlsx",
    ]

    moved_files = []

    for filename in files_to_move:
        source_path = os.path.join(source_dir, filename)
        if os.path.exists(source_path):
            dest_path = os.path.join(dest_dir, filename)
            shutil.move(source_path, dest_path)
            moved_files.append(filename)
            print(f"[OK] Moved: {filename}")

    if moved_files:
        print()
        print(f"Successfully organized {len(moved_files)} files into: {dest_dir}/")
    else:
        print(f"No files found to move in {source_dir}/")

    return dest_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: python organize_outputs.py <submission_name>")
        print("Example: python organize_outputs.py WorkSubmissions04")
        sys.exit(1)

    submission_name = sys.argv[1]

    print("=" * 80)
    print(f"ORGANIZING OUTPUTS FOR: {submission_name}")
    print("=" * 80)
    print()

    dest_dir = organize_outputs(submission_name)

    print()
    print("Output files are now in:")
    print(f"  {dest_dir}/")
    print()

if __name__ == "__main__":
    main()
