#!/usr/bin/env python3
"""
Grade comparison script for any WorkSubmissions folder
Compares evaluator grades with actual grades from PDF files
"""

import sys
import os

# Add skills directory to path
sys.path.insert(0, '.claude/skills/grade-comparison/scripts')
import compare_grades

def main():
    """Main function with flexible submission handling"""

    if len(sys.argv) < 2:
        print("Usage: python compare_grades.py <submission_name>")
        print("Example: python compare_grades.py WorkSubmissions04")
        print()
        print("This will:")
        print("  1. Load grades from outputs/<submission_name>/grades.xlsx")
        print("  2. Find PDFs in tests/<submission_name>/")
        print("  3. Generate comparison at outputs/<submission_name>/grade_comparison.xlsx")
        sys.exit(1)

    submission_name = sys.argv[1]

    print("=" * 80)
    print(f"GRADE COMPARISON TOOL - {submission_name}")
    print("=" * 80)
    print()

    # Determine paths
    grades_path = f"outputs/{submission_name}/grades.xlsx"
    worksubmissions_path = f"tests/{submission_name}"
    output_path = f"outputs/{submission_name}/grade_comparison.xlsx"

    # Fallback to main outputs/ if submission folder doesn't exist
    if not os.path.exists(grades_path):
        grades_path = "outputs/grades.xlsx"
        print(f"Note: Using fallback grades path: {grades_path}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Check if grades file exists
    if not os.path.exists(grades_path):
        print(f"Error: Could not find {grades_path}")
        print("Please run evaluation first.")
        sys.exit(1)

    # Check if WorkSubmissions folder exists
    if not os.path.exists(worksubmissions_path):
        print(f"Error: Could not find {worksubmissions_path}")
        print("Please check the submission name.")
        sys.exit(1)

    # Load evaluator grades
    evaluator_grades = compare_grades.load_evaluator_grades(grades_path)

    # Find student folders
    student_folders = compare_grades.find_student_folders(worksubmissions_path)

    # Extract actual grades from PDFs
    results = compare_grades.extract_actual_grades(student_folders, evaluator_grades)

    # Calculate statistics
    stats = compare_grades.calculate_statistics(results)

    # Print summary
    compare_grades.print_summary(stats)

    # Generate Excel report
    compare_grades.generate_excel_report(results, stats, output_path)

    print()
    print(f"Comparison saved to: {output_path}")
    print()

if __name__ == "__main__":
    main()
