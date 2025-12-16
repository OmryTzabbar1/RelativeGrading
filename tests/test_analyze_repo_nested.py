"""
Unit tests for analyze_repo with nested structure support.

Tests Angular detection and auto_find_root functionality.
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / '.claude' / 'skills'))

from analyze_repo import analyze_repository


def test_angular_detection_at_root(tmp_path):
    """Test that Angular projects are correctly detected."""
    project = tmp_path / "angular_app"
    project.mkdir()

    (project / "angular.json").write_text('{"version": 1}')
    (project / "package.json").write_text('{"name": "my-app"}')
    (project / "README.md").write_text("# Angular App")

    result = analyze_repository(str(project), auto_find_root=False)

    assert result['project_type'] == 'angular'
    assert 'angular.json' in result['key_files']
    assert 'package.json' in result['key_files']


def test_auto_find_root_nested_angular(tmp_path):
    """Test auto_find_root finds nested Angular project."""
    student = tmp_path / "Participant_123"
    project = student / "LLM_course" / "my-angular-app"
    project.mkdir(parents=True)

    (project / "angular.json").write_text("{}")
    (project / "package.json").write_text("{}")

    result = analyze_repository(str(student), auto_find_root=True)

    assert result['project_type'] == 'angular'
    assert str(project) in result['actual_project_path']


def test_auto_find_root_disabled(tmp_path):
    """Test that auto_find_root=False doesn't search subdirectories."""
    student = tmp_path / "student_nested"
    project = student / "actual_project"
    project.mkdir(parents=True)

    # Project is nested
    (project / "package.json").write_text("{}")

    # Analyze without auto_find_root
    result = analyze_repository(str(student), auto_find_root=False)

    # Should return unknown since no project at root
    assert result['project_type'] == 'unknown'
    assert result['actual_project_path'] == str(student.absolute())


def test_actual_project_path_tracking(tmp_path):
    """Test that actual_project_path is correctly returned."""
    student = tmp_path / "student"
    nested = student / "code" / "project"
    nested.mkdir(parents=True)

    (nested / "package.json").write_text("{}")

    result = analyze_repository(str(student), auto_find_root=True)

    assert result['actual_project_path'] == str(nested.absolute())
    assert result['project_type'] == 'javascript_web'


def test_angular_takes_precedence_over_javascript(tmp_path):
    """Test that Angular is detected before generic JavaScript."""
    project = tmp_path / "project"
    project.mkdir()

    # Both Angular and JavaScript markers present
    (project / "angular.json").write_text("{}")
    (project / "package.json").write_text("{}")
    (project / "app.js").write_text("// JavaScript")

    result = analyze_repository(str(project), auto_find_root=False)

    # Should be detected as Angular, not JavaScript
    assert result['project_type'] == 'angular'


def test_metadata_extraction_from_nested_project(tmp_path):
    """Test that metadata is extracted from the actual project, not parent."""
    student = tmp_path / "12345_john_doe"
    project = student / "assignment" / "code"
    project.mkdir(parents=True)

    (project / "package.json").write_text("{}")
    (project / "README.md").write_text("Team: Alpha Squad\nStudent ID: 67890")

    result = analyze_repository(str(student), auto_find_root=True)

    # Should extract metadata from nested project's README
    assert result['metadata']['team_name'] == 'Alpha Squad'
    assert result['metadata']['student_id'] == '67890'


def test_file_count_for_nested_project(tmp_path):
    """Test that file count is for the actual project directory."""
    student = tmp_path / "student"
    project = student / "app"
    project.mkdir(parents=True)

    # Add files to project
    (project / "package.json").write_text("{}")
    (project / "index.js").write_text("// code")
    (project / "README.md").write_text("# App")

    # Add decoy file in parent (should not be counted)
    (student / "notes.txt").write_text("random notes")

    result = analyze_repository(str(student), auto_find_root=True)

    # File count should be for project directory only
    assert result['file_count'] == 3  # package.json, index.js, README.md
