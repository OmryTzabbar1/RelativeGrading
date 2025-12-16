"""
Project structure validation utility.

Pre-flight validation to identify problematic student folders before evaluation.
"""

from pathlib import Path
from typing import List, Dict

from scan_folders import scan_student_folders
from find_project_root import find_project_root
from analyze_repo import analyze_repository


def validate_student_folders(
    master_folder: str,
    exclude: List[str] = None
) -> Dict:
    """
    Validate all student folders for potential issues.

    Checks each student folder for:
    - Project detectability (can we find a project?)
    - Project type identification
    - Nested structure issues
    - Empty or malformed folders

    Args:
        master_folder: Path to directory containing student folders
        exclude: List of folder names to skip

    Returns:
        Dict containing:
        {
            'total_students': int,
            'valid': List[Dict],  # Students with detectable projects
            'warnings': List[Dict],  # Students with issues but might work
            'errors': List[Dict],  # Students that will likely fail
            'summary': str  # Human-readable summary
        }

    Example:
        >>> result = validate_student_folders('/Assignment1/')
        >>> print(result['summary'])
        "Found 36 students: 30 valid, 4 warnings, 2 errors"
    """
    # Scan for all student folders
    try:
        students = scan_student_folders(master_folder, exclude=exclude)
    except Exception as e:
        return {
            'total_students': 0,
            'valid': [],
            'warnings': [],
            'errors': [],
            'summary': f"Failed to scan master folder: {str(e)}"
        }

    # Validate each student
    valid = []
    warnings = []
    errors = []

    for student in students:
        result = _validate_single_student(student)

        if result['status'] == 'valid':
            valid.append(result)
        elif result['status'] == 'warning':
            warnings.append(result)
        else:  # error
            errors.append(result)

    # Generate summary
    total = len(students)
    summary = (
        f"Found {total} students: "
        f"{len(valid)} valid, {len(warnings)} warnings, {len(errors)} errors"
    )

    return {
        'total_students': total,
        'valid': valid,
        'warnings': warnings,
        'errors': errors,
        'summary': summary
    }


def _validate_single_student(student: Dict) -> Dict:
    """
    Validate a single student folder.

    Returns:
        Dict with 'status' ('valid', 'warning', or 'error'), 'student', 'message', 'details'
    """
    name = student['name']
    path = student['path']

    try:
        # Try to find project root
        root_info = find_project_root(path)

        # Check if project was found
        if not root_info['project_root'] or root_info['confidence'] == 'low':
            return {
                'status': 'error',
                'student': name,
                'message': 'No project detected',
                'details': f"Could not find project markers in {path}"
            }

        # Try to analyze the project
        analysis = analyze_repository(path, auto_find_root=True)

        # Check for unknown project type
        if analysis['project_type'] == 'unknown':
            return {
                'status': 'warning',
                'student': name,
                'message': 'Unknown project type',
                'details': f"Project found at {analysis['actual_project_path']} but type unclear"
            }

        # Check for nested structure (warning, not error)
        if analysis['actual_project_path'] != str(Path(path).absolute()):
            nesting = Path(analysis['actual_project_path']).relative_to(path)
            return {
                'status': 'warning',
                'student': name,
                'message': f'Nested structure: {nesting}',
                'details': f"Project found at: {analysis['actual_project_path']}"
            }

        # All good!
        return {
            'status': 'valid',
            'student': name,
            'message': f"Valid {analysis['project_type']} project",
            'details': f"Project at: {analysis['actual_project_path']}"
        }

    except Exception as e:
        return {
            'status': 'error',
            'student': name,
            'message': 'Validation failed',
            'details': f"Error: {str(e)}"
        }


def print_validation_report(validation_result: Dict) -> None:
    """
    Print a human-readable validation report.

    Args:
        validation_result: Output from validate_student_folders()
    """
    print("\n" + "=" * 70)
    print("STUDENT PROJECT STRUCTURE VALIDATION REPORT")
    print("=" * 70)
    print(f"\n{validation_result['summary']}\n")

    # Print errors first (most important)
    if validation_result['errors']:
        print("\n🔴 ERRORS (require manual intervention):")
        print("-" * 70)
        for err in validation_result['errors']:
            print(f"  • {err['student']}: {err['message']}")
            print(f"    {err['details']}")

    # Print warnings
    if validation_result['warnings']:
        print("\n⚠️  WARNINGS (may work but check manually):")
        print("-" * 70)
        for warn in validation_result['warnings']:
            print(f"  • {warn['student']}: {warn['message']}")
            print(f"    {warn['details']}")

    # Summary of valid projects
    if validation_result['valid']:
        print(f"\n✅ VALID ({len(validation_result['valid'])} projects)")

    print("\n" + "=" * 70)
    print()
