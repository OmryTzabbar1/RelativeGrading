"""
Student Project Evaluator - Main Script
Sliding Window Criteria Discovery Approach v2.0

Usage:
    python main.py <master_folder> [options]

Options:
    --window-size N     Window size for sliding window analysis (default: 3)
    --output-dir PATH   Output directory for results (default: ./outputs)
    --exclude FOLDER    Folders to exclude from evaluation (can be repeated)
"""

import sys
import os
import argparse
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts.sliding_window_analyzer import analyze_sliding_windows, save_discovered_criteria
from scripts.final_evaluator import evaluate_all_students
from scripts.output_generator import generate_csv, generate_markdown_report
from scripts.analyze_project import analyze_project
from scripts.utils import scan_student_folders


def main():
    """Main entry point for the student project evaluator."""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Student Project Evaluator - Sliding Window v2.0'
    )
    parser.add_argument(
        'master_folder',
        help='Path to folder containing student projects'
    )
    parser.add_argument(
        '--window-size',
        type=int,
        default=3,
        help='Window size for sliding window analysis (default: 3)'
    )
    parser.add_argument(
        '--output-dir',
        default='./outputs',
        help='Output directory for results (default: ./outputs)'
    )
    parser.add_argument(
        '--exclude',
        action='append',
        default=[],
        help='Folders to exclude from evaluation'
    )

    args = parser.parse_args()

    # Validate master folder
    if not os.path.exists(args.master_folder):
        print(f"[ERROR] Master folder not found: {args.master_folder}")
        sys.exit(1)

    if not os.path.isdir(args.master_folder):
        print(f"[ERROR] Not a directory: {args.master_folder}")
        sys.exit(1)

    # Display configuration
    print("=" * 70)
    print("Student Project Evaluator - Sliding Window v2.0")
    print("=" * 70)
    print(f"Master folder: {args.master_folder}")
    print(f"Window size: {args.window_size}")
    print(f"Output directory: {args.output_dir}")
    if args.exclude:
        print(f"Excluded folders: {', '.join(args.exclude)}")
    print("=" * 70)

    try:
        # Step 1: Scan student folders
        print("\n[1/5] Scanning student folders...")
        student_folders = scan_student_folders(args.master_folder, exclude=args.exclude)

        if not student_folders:
            print("[ERROR] No student folders found!")
            sys.exit(1)

        print(f"Found {len(student_folders)} student folders")

        # Step 2: Phase 1 - Criteria Discovery
        print("\n[2/5] Running Phase 1 - Criteria Discovery...")
        criteria = analyze_sliding_windows(student_folders, window_size=args.window_size)

        # Save discovered criteria
        criteria_path = os.path.join(args.output_dir, "discovered_criteria.yml")
        save_discovered_criteria(criteria, criteria_path)

        # Step 3: Analyze all projects
        print("\n[3/5] Analyzing all projects for final evaluation...")
        project_features_map = {}

        for i, student_path in enumerate(student_folders, 1):
            student_name = os.path.basename(student_path)
            print(f"  [{i}/{len(student_folders)}] {student_name}")

            features = analyze_project(student_path)
            project_features_map[student_path] = features

        # Step 4: Phase 2 - Final Evaluation
        print("\n[4/5] Running Phase 2 - Final Evaluation...")
        evaluations = evaluate_all_students(
            student_folders,
            criteria,
            project_features_map
        )

        print(f"\nEvaluated {len(evaluations)} students")
        print(f"Best grade: {evaluations[0].grade} ({evaluations[0].student_name})")
        print(f"Mean grade: {sum(e.grade for e in evaluations) / len(evaluations):.2f}")

        # Step 5: Generate Outputs
        print("\n[5/5] Generating outputs...")

        # Generate CSV
        csv_path = os.path.join(args.output_dir, "grades.csv")
        generate_csv(evaluations, csv_path)

        # Generate markdown report
        report_path = os.path.join(args.output_dir, "evaluation_report.md")
        generate_markdown_report(evaluations, criteria, report_path)

        # Final summary
        print("\n" + "=" * 70)
        print("Evaluation Complete!")
        print("=" * 70)
        print(f"\nOutput files:")
        print(f"  1. Discovered Criteria: {criteria_path}")
        print(f"  2. Grades CSV:          {csv_path}")
        print(f"  3. Evaluation Report:   {report_path}")
        print("\n" + "=" * 70)

    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Evaluation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
