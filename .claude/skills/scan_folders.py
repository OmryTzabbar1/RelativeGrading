"""
Student folder scanning utility.

Auto-detects student project folders in a master directory for batch evaluation.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional


def scan_student_folders(
    master_folder: str,
    exclude: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    """
    Scan master folder for student subdirectories.

    Finds all subdirectories in the master folder and returns metadata about each.
    Hidden folders (starting with '.') and explicitly excluded folders are filtered out.

    Args:
        master_folder: Absolute path to directory containing student project folders
        exclude: List of folder names to exclude (e.g., ['baseline_student', '.git'])

    Returns:
        List of dicts, each containing:
            - 'name': Folder name (str)
            - 'path': Full absolute path (str)
        Sorted alphabetically by folder name.

    Raises:
        ValueError: If master_folder is empty or not a directory
        FileNotFoundError: If master_folder does not exist
        PermissionError: If master_folder is not readable

    Example:
        >>> scan_student_folders('/Assignments/A1/', exclude=['student_alice'])
        [
            {'name': 'student_bob', 'path': '/Assignments/A1/student_bob'},
            {'name': 'student_carol', 'path': '/Assignments/A1/student_carol'}
        ]
    """
    # Validate inputs
    if not master_folder:
        raise ValueError("master_folder cannot be empty")

    master_path = Path(master_folder)

    if not master_path.exists():
        raise FileNotFoundError(
            f"Directory not found: {master_folder}\n"
            f"Please check that the path is correct and the folder exists."
        )

    if not master_path.is_dir():
        raise ValueError(
            f"Not a directory: {master_folder}\n"
            f"Please provide a path to a directory, not a file."
        )

    # Initialize exclude list
    exclude_set = set(exclude) if exclude else set()

    # Scan for subdirectories
    student_folders = []

    try:
        for item in master_path.iterdir():
            # Skip if not a directory
            if not item.is_dir():
                continue

            folder_name = item.name

            # Skip hidden folders (start with '.')
            if folder_name.startswith('.'):
                continue

            # Skip explicitly excluded folders
            if folder_name in exclude_set:
                continue

            student_folders.append({
                'name': folder_name,
                'path': str(item.absolute())
            })

    except PermissionError:
        raise PermissionError(
            f"Permission denied: Cannot read directory {master_folder}\n"
            f"Please check that you have read permissions for this folder."
        )

    # Sort alphabetically by folder name
    student_folders.sort(key=lambda x: x['name'])

    return student_folders
