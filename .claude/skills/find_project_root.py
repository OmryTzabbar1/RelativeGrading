"""
Project root discovery utility.

Recursively searches for actual project directories within student folders,
handling arbitrary nesting levels and multiple project types.
"""

import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple


# Project type markers: (primary marker, optional markers)
# Primary marker MUST exist, optional markers are for confidence scoring
PROJECT_MARKERS = {
    'angular': (['angular.json'], ['package.json']),
    'javascript': (['package.json'], []),
    'python': (['requirements.txt', 'setup.py', 'pyproject.toml'], []),
    'java': (['pom.xml', 'build.gradle', 'build.gradle.kts'], [])
}


def find_project_root(
    student_folder: str,
    max_depth: int = 3
) -> Dict[str, Optional[str]]:
    """
    Find the actual project directory within a student folder.

    Recursively searches up to max_depth levels for project marker files
    (package.json, angular.json, requirements.txt, etc.) and returns the
    directory containing the most project markers.

    Args:
        student_folder: Path to student's top-level folder
        max_depth: Maximum depth to search (default: 3 levels)

    Returns:
        Dict containing:
        {
            'project_root': str | None,  # Path to actual project dir
            'project_type': str | None,  # Detected project type
            'confidence': str,  # 'high', 'medium', 'low'
            'markers_found': List[str]  # Project markers found
        }

    Example:
        >>> find_project_root('Participant_38951/')
        {
            'project_root': 'Participant_38951/LLM_course/ollama-chatbot-angular',
            'project_type': 'angular',
            'confidence': 'high',
            'markers_found': ['angular.json', 'package.json']
        }
    """
    folder = Path(student_folder)

    if not folder.exists() or not folder.is_dir():
        return {
            'project_root': None,
            'project_type': None,
            'confidence': 'low',
            'markers_found': []
        }

    # Search for project directories
    candidates = _search_project_directories(folder, max_depth)

    if not candidates:
        # No project found, return the original folder
        return {
            'project_root': str(folder.absolute()),
            'project_type': None,
            'confidence': 'low',
            'markers_found': []
        }

    # Select best candidate
    best = _select_best_candidate(candidates)

    return {
        'project_root': str(best['path']),
        'project_type': best['type'],
        'confidence': best['confidence'],
        'markers_found': best['markers']
    }


def _search_project_directories(
    root: Path,
    max_depth: int
) -> List[Dict]:
    """Search for directories containing project markers."""
    candidates = []

    def search_recursive(current: Path, depth: int):
        """Recursive search helper."""
        if depth > max_depth:
            return

        # Skip hidden directories and common non-project folders
        if current.name.startswith('.') or current.name in ['node_modules', '__pycache__', 'venv', 'dist', 'build']:
            return

        # Check if current directory has project markers
        markers_found = []
        detected_type = None
        best_marker_count = 0

        for proj_type, (primary_markers, optional_markers) in PROJECT_MARKERS.items():
            # Check if ANY primary marker exists
            primary_found = any((current / m).exists() for m in primary_markers)

            if not primary_found:
                continue  # Skip this project type if no primary marker found

            # Count all markers (primary + optional) for this type
            type_markers = []
            for marker in primary_markers + optional_markers:
                if (current / marker).exists():
                    type_markers.append(marker)

            # Select project type with most markers found
            if len(type_markers) > best_marker_count:
                detected_type = proj_type
                markers_found = type_markers
                best_marker_count = len(type_markers)

        # If markers found, add as candidate
        if markers_found:
            confidence = 'high' if len(markers_found) >= 2 else 'medium'
            candidates.append({
                'path': current.absolute(),
                'type': detected_type,
                'markers': markers_found,
                'confidence': confidence,
                'depth': depth
            })

        # Continue searching subdirectories
        try:
            for item in current.iterdir():
                if item.is_dir():
                    search_recursive(item, depth + 1)
        except (PermissionError, OSError):
            pass  # Skip inaccessible directories

    # Start search from root
    search_recursive(root, 0)

    return candidates


def _select_best_candidate(candidates: List[Dict]) -> Dict:
    """
    Select the best project directory from candidates.

    Priority:
    1. Highest confidence (most markers found)
    2. Shallowest depth (prefer less nesting)
    3. Most markers (more is better)
    """
    # Sort by confidence desc, depth asc, markers desc
    confidence_order = {'high': 3, 'medium': 2, 'low': 1}

    sorted_candidates = sorted(
        candidates,
        key=lambda x: (
            -confidence_order[x['confidence']],  # Negative for descending (high first)
            x['depth'],  # Ascending (shallow first)
            -len(x['markers'])  # Negative for descending (more first)
        )
    )

    return sorted_candidates[0]
