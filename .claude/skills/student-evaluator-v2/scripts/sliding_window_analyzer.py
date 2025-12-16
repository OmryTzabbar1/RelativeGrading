"""
Sliding Window Analyzer Module
Implements Phase 1 of evaluation: criteria discovery through sliding windows.
"""

from typing import List, Dict, Any
from scripts.criteria_builder import DiscoveredCriteria
from scripts.analyze_project import analyze_project
from scripts.utils import get_student_name, find_new_features, format_dimension_list


def analyze_sliding_windows(student_folders: List[str], window_size: int = 3) -> DiscoveredCriteria:
    """
    Analyze students in sliding windows to discover criteria.

    Args:
        student_folders: List of paths to student project folders
        window_size: Number of students per window (default: 3)

    Returns:
        DiscoveredCriteria object with all discovered quality dimensions
    """
    if not student_folders:
        raise ValueError("student_folders cannot be empty")

    if window_size < 1:
        raise ValueError("window_size must be at least 1")

    criteria = DiscoveredCriteria()
    total_students = len(student_folders)

    # Cache for analyzed projects to avoid re-analysis
    project_cache: Dict[str, Dict[str, Any]] = {}

    # Calculate number of windows
    if total_students < window_size:
        num_windows = 1
        window_size = total_students
    else:
        num_windows = total_students - window_size + 1

    print(f"\n{'='*60}")
    print(f"Phase 1: Sliding Window Criteria Discovery")
    print(f"{'='*60}")
    print(f"Total students: {total_students}")
    print(f"Window size: {window_size}")
    print(f"Number of windows: {num_windows}")
    print(f"{'='*60}\n")

    # Iterate through sliding windows
    for i in range(num_windows):
        window = student_folders[i:i+window_size]
        window_num = i + 1

        # Display window information
        student_names = [get_student_name(path) for path in window]
        print(f"Window {window_num}/{num_windows}: Analyzing {student_names}")

        # Analyze each student in the window
        for student_path in window:
            student_name = get_student_name(student_path)

            # Check cache first
            if student_path in project_cache:
                features = project_cache[student_path]
            else:
                # Analyze project and cache results
                features = analyze_project(student_path)
                project_cache[student_path] = features

            # Skip if error occurred
            if 'error' in features:
                print(f"  [SKIP] {student_name}: {features.get('error', 'unknown error')}")
                continue

            # Find new features not in criteria
            new_dimensions = find_new_features(features, criteria.dimensions)

            if new_dimensions:
                formatted_dims = format_dimension_list(new_dimensions)
                print(f"  [NEW] {student_name} added: {formatted_dims}")

            # Merge features into criteria
            criteria.merge_features(features, student_name)

        print()  # Blank line between windows

    # Final summary
    print(f"{'='*60}")
    print(f"Criteria Discovery Complete")
    print(f"{'='*60}")
    print(f"Total dimensions discovered: {criteria.get_dimension_count()}")
    print(f"Dimensions: {format_dimension_list(criteria.get_dimension_names())}")
    print(f"{'='*60}\n")

    return criteria


def save_discovered_criteria(criteria: DiscoveredCriteria, output_path: str) -> None:
    """
    Save discovered criteria to YAML file.

    Args:
        criteria: DiscoveredCriteria object to save
        output_path: Path to output YAML file
    """
    import os

    # Create output directory if needed
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write YAML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(criteria.to_yaml())

    print(f"Saved discovered criteria to: {output_path}")


def load_discovered_criteria(yaml_path: str) -> DiscoveredCriteria:
    """
    Load discovered criteria from YAML file.

    Args:
        yaml_path: Path to YAML file

    Returns:
        DiscoveredCriteria object
    """
    import yaml

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    criteria = DiscoveredCriteria()
    criteria.dimensions = data.get('criteria', {})
    criteria.evolution_log = data.get('evolution', [])

    return criteria
