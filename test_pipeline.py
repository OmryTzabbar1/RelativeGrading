"""
Full Pipeline Test
Tests the complete sliding window evaluation pipeline.
"""

import sys
import os
sys.path.insert(0, '.claude/skills/student-evaluator-v2')

from scripts.sliding_window_analyzer import analyze_sliding_windows, save_discovered_criteria
from scripts.final_evaluator import evaluate_all_students
from scripts.output_generator import generate_csv, generate_markdown_report
from scripts.analyze_project import analyze_project
from scripts.utils import scan_student_folders


def test_full_pipeline():
    """Test the complete evaluation pipeline."""

    # Configuration
    master_folder = "E:\\Projects\\student-project-evaluator\\tests\\WorkSubmissions01"
    window_size = 3
    output_dir = "E:\\Projects\\student-project-evaluator\\outputs"

    print("=" * 60)
    print("Full Pipeline Test - Sliding Window Evaluation")
    print("=" * 60)

    # Step 1: Scan student folders
    print("\nStep 1: Scanning student folders...")
    student_folders = scan_student_folders(
        master_folder,
        exclude=['evaluation_relative.json', 'evaluation_summary_relative.md',
                'grades_relative.csv', 'grades_relative.xlsx', 'nul']
    )

    # Limit to first 10 students for testing
    student_folders = student_folders[:10]

    print(f"Found {len(student_folders)} student folders")
    for i, folder in enumerate(student_folders, 1):
        folder_name = os.path.basename(folder)
        print(f"  {i}. {folder_name}")

    # Step 2: Phase 1 - Criteria Discovery
    print("\nStep 2: Running Phase 1 - Criteria Discovery...")
    criteria = analyze_sliding_windows(student_folders, window_size=window_size)

    # Save discovered criteria
    criteria_path = os.path.join(output_dir, "discovered_criteria.yml")
    save_discovered_criteria(criteria, criteria_path)

    # Step 3: Analyze all projects (for Phase 2)
    print("\nStep 3: Analyzing all projects for final evaluation...")
    project_features_map = {}

    for student_path in student_folders:
        student_name = os.path.basename(student_path)
        print(f"  Analyzing {student_name}...")

        features = analyze_project(student_path)
        project_features_map[student_path] = features

    # Step 4: Phase 2 - Final Evaluation
    print("\nStep 4: Running Phase 2 - Final Evaluation...")
    print("=" * 60)

    evaluations = evaluate_all_students(
        student_folders,
        criteria,
        project_features_map
    )

    print(f"\nEvaluated {len(evaluations)} students")
    print(f"Best grade: {evaluations[0].grade} (Rank 1)")
    print(f"Lowest grade: {evaluations[-1].grade} (Rank {len(evaluations)})")

    # Step 5: Generate Outputs
    print("\nStep 5: Generating outputs...")

    # Generate CSV
    csv_path = os.path.join(output_dir, "grades.csv")
    generate_csv(evaluations, csv_path)

    # Generate markdown report
    report_path = os.path.join(output_dir, "evaluation_report.md")
    generate_markdown_report(evaluations, criteria, report_path)

    # Final summary
    print("\n" + "=" * 60)
    print("Pipeline Test Complete!")
    print("=" * 60)
    print(f"\nOutput files:")
    print(f"  - Criteria: {criteria_path}")
    print(f"  - Grades CSV: {csv_path}")
    print(f"  - Report: {report_path}")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    try:
        test_full_pipeline()
    except Exception as e:
        print(f"\n[ERROR] Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
