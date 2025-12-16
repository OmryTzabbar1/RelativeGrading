"""
Project Analysis Module
Analyzes student projects and extracts quality features.
"""

import os
from pathlib import Path
from typing import Dict, Any, List


def analyze_project(project_path: str) -> Dict[str, Any]:
    """
    Analyze student project and extract comprehensive features.

    Args:
        project_path: Path to student project folder

    Returns:
        Dictionary with all discovered features organized by dimension
    """
    if not os.path.exists(project_path):
        return {'error': 'project_not_found', 'path': project_path}

    features = {
        'documentation': analyze_documentation(project_path),
        'testing': analyze_testing(project_path),
        'graphics': analyze_graphics(project_path),
        'research': analyze_research(project_path),
        'code_quality': analyze_code_quality(project_path)
    }

    return features


def analyze_documentation(project_path: str) -> Dict[str, Any]:
    """
    Analyze documentation quality.

    Args:
        project_path: Path to project folder

    Returns:
        Documentation metrics
    """
    docs = {}
    path = Path(project_path)

    # Check for README
    readme_files = list(path.glob('**/README.md')) + list(path.glob('**/readme.md'))
    if readme_files:
        readme_path = readme_files[0]
        line_count = sum(1 for _ in open(readme_path, 'r', encoding='utf-8', errors='ignore'))
        docs['readme'] = {'present': True, 'lines': line_count}

    # Check for PRD
    prd_files = list(path.glob('**/PRD.md')) + list(path.glob('**/prd.md'))
    if prd_files:
        docs['prd'] = {'present': True, 'weight': 5}

    # Check for Architecture docs
    arch_files = list(path.glob('**/ARCHITECTURE.md')) + list(path.glob('**/architecture.md'))
    if arch_files:
        docs['architecture'] = {'present': True, 'weight': 10}

    # Check for PROMPT_BOOK
    prompt_files = list(path.glob('**/PROMPT_BOOK.md')) + list(path.glob('**/prompt_book.md'))
    if prompt_files:
        docs['prompt_book'] = {'present': True, 'weight': 8}

    return docs if docs else {'present': False}


def analyze_testing(project_path: str) -> Dict[str, Any]:
    """
    Analyze testing presence and quality.

    Args:
        project_path: Path to project folder

    Returns:
        Testing metrics
    """
    path = Path(project_path)
    test_files = []

    # Common test file patterns
    patterns = ['**/test_*.py', '**/*_test.py', '**/*.test.js', '**/*.spec.js']

    for pattern in patterns:
        test_files.extend(path.glob(pattern))

    if test_files:
        return {'present': True, 'test_file_count': len(test_files), 'weight': 15}

    return {'present': False}


def analyze_graphics(project_path: str) -> Dict[str, Any]:
    """
    Analyze visual elements (images, diagrams, charts).

    Args:
        project_path: Path to project folder

    Returns:
        Graphics metrics
    """
    path = Path(project_path)
    image_files = []

    # Image file patterns
    patterns = ['**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.gif', '**/*.svg']

    for pattern in patterns:
        image_files.extend(path.glob(pattern))

    if image_files:
        return {'present': True, 'image_count': len(image_files), 'weight': 10}

    return {'present': False}


def analyze_research(project_path: str) -> Dict[str, Any]:
    """
    Analyze research artifacts (notebooks, analysis docs).

    Args:
        project_path: Path to project folder

    Returns:
        Research metrics
    """
    path = Path(project_path)
    research = {}

    # Check for Jupyter notebooks
    notebooks = list(path.glob('**/*.ipynb'))
    if notebooks:
        research['notebooks'] = {'present': True, 'count': len(notebooks), 'weight': 10}

    # Check for analysis documents
    analysis_docs = list(path.glob('**/ANALYSIS.md')) + list(path.glob('**/analysis.md'))
    if analysis_docs:
        research['analysis_docs'] = {'present': True, 'weight': 10}

    return research if research else {'present': False}


def analyze_code_quality(project_path: str) -> Dict[str, Any]:
    """
    Analyze code quality indicators.

    Args:
        project_path: Path to project folder

    Returns:
        Code quality metrics
    """
    path = Path(project_path)
    code_files = []

    # Common code file patterns
    patterns = ['**/*.py', '**/*.js', '**/*.ts', '**/*.java', '**/*.cpp']

    for pattern in patterns:
        code_files.extend(path.glob(pattern))

    if code_files:
        return {'present': True, 'file_count': len(code_files), 'weight': 20}

    return {'present': False}
