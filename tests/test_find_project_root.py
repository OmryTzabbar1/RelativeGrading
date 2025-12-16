"""
Unit tests for find_project_root module.

Tests recursive project discovery, Angular detection, and nested structures.
"""

import pytest
from pathlib import Path
import sys

# Add .claude/skills to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / '.claude' / 'skills'))

from find_project_root import find_project_root, _search_project_directories


def test_find_angular_project_nested(tmp_path):
    """Test finding Angular project 2 levels deep."""
    # Create nested structure: student/LLM_course/ollama-chatbot-angular/
    student = tmp_path / "Participant_38951"
    project = student / "LLM_course" / "ollama-chatbot-angular"
    project.mkdir(parents=True)

    # Create Angular markers
    (project / "angular.json").write_text("{}")
    (project / "package.json").write_text("{}")
    (project / "README.md").write_text("# Angular Project")

    # Find project root
    result = find_project_root(str(student))

    assert result['project_root'] == str(project)
    assert result['project_type'] == 'angular'
    assert result['confidence'] == 'high'
    assert 'angular.json' in result['markers_found']


def test_find_javascript_project_shallow(tmp_path):
    """Test finding JavaScript project at top level."""
    student = tmp_path / "student_bob"
    student.mkdir()

    # Create JavaScript markers
    (student / "package.json").write_text("{}")
    (student / "index.js").write_text("console.log('hello');")

    result = find_project_root(str(student))

    assert result['project_root'] == str(student)
    assert result['project_type'] == 'javascript'
    assert result['confidence'] in ['high', 'medium']


def test_no_project_found(tmp_path):
    """Test folder with no project markers."""
    student = tmp_path / "student_empty"
    student.mkdir()

    # Just a README, no project files
    (student / "README.md").write_text("Empty project")

    result = find_project_root(str(student))

    assert result['project_root'] == str(student)
    assert result['project_type'] is None
    assert result['confidence'] == 'low'


def test_multiple_nested_projects_selects_best(tmp_path):
    """Test selection when multiple project directories exist."""
    student = tmp_path / "student_multi"
    student.mkdir()

    # Create two potential projects
    proj1 = student / "old_version"
    proj1.mkdir()
    (proj1 / "package.json").write_text("{}")  # Medium confidence

    proj2 = student / "current" / "app"
    proj2.mkdir(parents=True)
    (proj2 / "angular.json").write_text("{}")
    (proj2 / "package.json").write_text("{}")  # High confidence

    result = find_project_root(str(student))

    # Should select high-confidence Angular project
    assert result['project_root'] == str(proj2)
    assert result['confidence'] == 'high'


def test_max_depth_limit(tmp_path):
    """Test that search respects max_depth parameter."""
    student = tmp_path / "student_deep"

    # Create very deep nesting
    deep_project = student / "a" / "b" / "c" / "d" / "project"
    deep_project.mkdir(parents=True)
    (deep_project / "package.json").write_text("{}")

    # Search with max_depth=3 (should not find project at level 5)
    result = find_project_root(str(student), max_depth=3)

    assert result['confidence'] == 'low'  # Should not find the deep project


def test_skip_hidden_and_common_folders(tmp_path):
    """Test that hidden and node_modules folders are skipped."""
    student = tmp_path / "student_messy"
    student.mkdir()

    # Create decoy in node_modules (should be ignored)
    decoy = student / "node_modules" / "some-package"
    decoy.mkdir(parents=True)
    (decoy / "package.json").write_text("{}")

    # Real project at top level
    (student / "package.json").write_text("{}")

    result = find_project_root(str(student))

    # Should find top-level project, not the one in node_modules
    assert result['project_root'] == str(student)


def test_python_project_detection(tmp_path):
    """Test detection of Python projects."""
    student = tmp_path / "student_python"
    project = student / "my_app"
    project.mkdir(parents=True)

    (project / "requirements.txt").write_text("flask==2.0.0")
    (project / "main.py").write_text("print('hello')")

    result = find_project_root(str(student))

    assert result['project_type'] == 'python'
    assert result['project_root'] == str(project)


def test_java_project_detection(tmp_path):
    """Test detection of Java projects."""
    student = tmp_path / "student_java"
    project = student / "maven_project"
    project.mkdir(parents=True)

    (project / "pom.xml").write_text("<project></project>")

    result = find_project_root(str(student))

    assert result['project_type'] == 'java'
    assert result['project_root'] == str(project)


def test_nonexistent_folder(tmp_path):
    """Test handling of nonexistent folder."""
    result = find_project_root(str(tmp_path / "does_not_exist"))

    assert result['project_root'] is None
    assert result['confidence'] == 'low'


def test_prefer_shallower_when_equal_confidence(tmp_path):
    """Test that shallower projects are preferred when confidence is equal."""
    student = tmp_path / "student_shallow_vs_deep"
    student.mkdir()

    # Shallow project (1 marker)
    (student / "package.json").write_text("{}")

    # Deep project (1 marker, same confidence)
    deep = student / "subfolder" / "project"
    deep.mkdir(parents=True)
    (deep / "package.json").write_text("{}")

    result = find_project_root(str(student))

    # Should prefer the shallower one
    assert result['project_root'] == str(student)
