"""
Repository analysis utility.

Detects project type and extracts metadata from student project folders.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional


def analyze_repository(folder_path: str) -> Dict:
    """
    Analyze a student repository to extract metadata and project type.

    Args:
        folder_path: Path to student project folder

    Returns:
        Dict containing:
        {
            'project_type': str,  # 'javascript_web', 'python_app', 'java_app', 'unknown'
            'key_files': List[str],  # Important files found
            'metadata': Dict,  # team_name, student_id if found
            'size_mb': float,  # Folder size in MB
            'file_count': int  # Total number of files
        }

    Raises:
        FileNotFoundError: If folder doesn't exist
        ValueError: If folder is empty

    Example:
        >>> analyze_repository('/path/to/student_bob/')
        {
            'project_type': 'javascript_web',
            'key_files': ['README.md', 'src/index.js', 'package.json'],
            'metadata': {'team_name': 'Team Alpha', 'student_id': '12345'},
            'size_mb': 3.5,
            'file_count': 89
        }
    """
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder.is_dir():
        raise ValueError(f"Not a directory: {folder_path}")

    # Detect project type and key files
    project_type, key_files = _detect_project_type(folder)

    # Extract metadata from README or folder name
    metadata = _extract_metadata(folder)

    # Calculate folder size and file count
    size_mb, file_count = _calculate_folder_stats(folder)

    return {
        'project_type': project_type,
        'key_files': key_files,
        'metadata': metadata,
        'size_mb': size_mb,
        'file_count': file_count
    }


def _detect_project_type(folder: Path) -> tuple[str, List[str]]:
    """Detect project type based on marker files."""
    key_files = []

    # Check for JavaScript/Node project
    if (folder / 'package.json').exists():
        key_files.append('package.json')
        if (folder / 'src' / 'index.js').exists() or (folder / 'app.js').exists():
            key_files.append('src/index.js' if (folder / 'src' / 'index.js').exists() else 'app.js')
        if (folder / 'README.md').exists():
            key_files.append('README.md')
        return 'javascript_web', key_files

    # Check for Python project
    if (folder / 'requirements.txt').exists() or (folder / 'setup.py').exists():
        if (folder / 'requirements.txt').exists():
            key_files.append('requirements.txt')
        if (folder / 'main.py').exists() or (folder / 'app.py').exists():
            key_files.append('main.py' if (folder / 'main.py').exists() else 'app.py')
        if (folder / 'README.md').exists():
            key_files.append('README.md')
        return 'python_app', key_files

    # Check for Java project
    if (folder / 'pom.xml').exists() or (folder / 'build.gradle').exists():
        key_files.append('pom.xml' if (folder / 'pom.xml').exists() else 'build.gradle')
        if (folder / 'README.md').exists():
            key_files.append('README.md')
        return 'java_app', key_files

    # Unknown project type - just look for README
    if (folder / 'README.md').exists():
        key_files.append('README.md')

    return 'unknown', key_files


def _extract_metadata(folder: Path) -> Dict[str, Optional[str]]:
    """Extract metadata from README or folder name."""
    metadata = {'team_name': None, 'student_id': None}

    # Try to extract from README.md
    readme_path = folder / 'README.md'
    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding='utf-8', errors='ignore')

            # Look for team name patterns
            team_match = re.search(r'Team:\s*(.+)', content, re.IGNORECASE)
            if team_match:
                metadata['team_name'] = team_match.group(1).strip()

            # Look for student ID patterns
            id_match = re.search(r'Student\s*ID:\s*(\w+)', content, re.IGNORECASE)
            if id_match:
                metadata['student_id'] = id_match.group(1).strip()

        except Exception:
            pass  # If README can't be read, continue without metadata

    # Try to extract student ID from folder name (e.g., "12345_john_doe")
    if not metadata['student_id']:
        folder_name = folder.name
        id_match = re.match(r'(\d{4,})', folder_name)
        if id_match:
            metadata['student_id'] = id_match.group(1)

    return metadata


def _calculate_folder_stats(folder: Path) -> tuple[float, int]:
    """Calculate folder size in MB and file count."""
    total_size = 0
    file_count = 0

    for item in folder.rglob('*'):
        if item.is_file():
            try:
                total_size += item.stat().st_size
                file_count += 1
            except (PermissionError, OSError):
                continue  # Skip files we can't access

    size_mb = total_size / (1024 * 1024)  # Convert bytes to MB
    return round(size_mb, 2), file_count
