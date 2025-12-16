"""
Utility Functions
Helper functions for feature comparison, merging, and student name extraction.
"""

import os
from typing import Dict, List, Any
from pathlib import Path


def get_student_name(student_path: str) -> str:
    """
    Extract student name from folder path.

    Args:
        student_path: Full path to student project folder

    Returns:
        Student folder name
    """
    return Path(student_path).name


def find_new_features(features: Dict[str, Any], existing_dimensions: Dict[str, Any]) -> List[str]:
    """
    Find features that are new (not in existing dimensions).

    Args:
        features: Feature dictionary from analyze_project()
        existing_dimensions: Current criteria dimensions

    Returns:
        List of new feature/dimension names
    """
    new_features = []

    for feature_name in features.keys():
        if feature_name not in existing_dimensions:
            new_features.append(feature_name)

    return new_features


def compare_features(features1: Dict[str, Any], features2: Dict[str, Any]) -> Dict[str, str]:
    """
    Compare two feature dictionaries.

    Args:
        features1: First feature dictionary
        features2: Second feature dictionary

    Returns:
        Dictionary with comparison results
    """
    comparison = {
        'common': [],
        'only_in_first': [],
        'only_in_second': []
    }

    all_keys = set(features1.keys()) | set(features2.keys())

    for key in all_keys:
        if key in features1 and key in features2:
            comparison['common'].append(key)
        elif key in features1:
            comparison['only_in_first'].append(key)
        else:
            comparison['only_in_second'].append(key)

    return comparison


def merge_feature_data(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge new feature data into existing feature data.

    Args:
        existing: Existing feature data
        new: New feature data to merge

    Returns:
        Merged feature data
    """
    merged = existing.copy()
    merged.update(new)
    return merged


def has_new_features(features: Dict[str, Any], criteria_dimensions: Dict[str, Any]) -> bool:
    """
    Check if features contain any new dimensions not in criteria.

    Args:
        features: Feature dictionary from analyze_project()
        criteria_dimensions: Current criteria dimensions

    Returns:
        True if any new features found, False otherwise
    """
    return any(feature_name not in criteria_dimensions for feature_name in features.keys())


def scan_student_folders(master_folder: str, exclude: List[str] = None) -> List[str]:
    """
    Scan master folder for student project directories.

    Args:
        master_folder: Path to folder containing student projects
        exclude: List of folder names to exclude (optional)

    Returns:
        List of full paths to student folders
    """
    if not os.path.exists(master_folder):
        raise FileNotFoundError(f"Master folder not found: {master_folder}")

    if not os.path.isdir(master_folder):
        raise ValueError(f"Not a directory: {master_folder}")

    exclude = exclude or []
    student_folders = []

    for item in os.listdir(master_folder):
        item_path = os.path.join(master_folder, item)

        # Skip if not a directory
        if not os.path.isdir(item_path):
            continue

        # Skip hidden folders
        if item.startswith('.'):
            continue

        # Skip excluded folders
        if item in exclude:
            continue

        student_folders.append(item_path)

    # Sort alphabetically for consistent ordering
    student_folders.sort()

    return student_folders


def format_dimension_list(dimensions: List[str]) -> str:
    """
    Format list of dimension names for display.

    Args:
        dimensions: List of dimension names

    Returns:
        Formatted string
    """
    if not dimensions:
        return "None"

    if len(dimensions) == 1:
        return dimensions[0]

    return ", ".join(dimensions)


def calculate_window_count(total_students: int, window_size: int = 3) -> int:
    """
    Calculate number of sliding windows needed.

    Args:
        total_students: Total number of students
        window_size: Window size (default: 3)

    Returns:
        Number of windows
    """
    if total_students < window_size:
        return 1

    return total_students - window_size + 1
