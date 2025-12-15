# Claude Development Rules and Conventions
# Student Project Evaluator

**Project**: Student Project Evaluator
**Version**: 1.0
**Last Updated**: 2024-12-15

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Development Environment](#2-development-environment)
3. [Project Structure](#3-project-structure)
4. [Coding Standards](#4-coding-standards)
5. [Configuration Management](#5-configuration-management)
6. [Security Practices](#6-security-practices)
7. [Testing Requirements](#7-testing-requirements)
8. [Git Workflow](#8-git-workflow)
9. [Documentation Standards](#9-documentation-standards)
10. [Prompt Engineering Log](#10-prompt-engineering-log)

---

## 1. Project Overview

### 1.1 What This Project Does

A Claude Code skill that performs **comparative evaluation** of student coding projects. It:
- Compares student projects against a dynamically-updated baseline
- Assesses assignment relevance and functionality
- Outputs CSV grades and markdown reports
- Generates assignment-specific configuration files

### 1.2 Target Audience (Developers)

- **Primary Developer**: Building the MVP (you, Claude Code)
- **Maintainers**: Future developers extending the skill
- **Contributors**: Other educators who may customize evaluation criteria

### 1.3 Development Principles

1. **Fail-Safe**: Skip errors, don't crash - instructor needs results even if some students have issues
2. **Transparency**: Every grade must have clear reasoning
3. **Configurability**: Use YAML configs, not hardcoded values
4. **Modularity**: Separate orchestration (SKILL.md) from file operations (scripts)
5. **Simplicity**: Minimal dependencies, standard library preferred

---

## 2. Development Environment

### 2.1 Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| **Claude Code** | Latest | Execution platform |
| **Python** | 3.8+ | Helper scripts |
| **Git** | 2.0+ | Version control |
| **Text Editor** | Any | Markdown/YAML editing (VS Code recommended) |

### 2.2 Setup Instructions

```bash
# 1. Navigate to skills directory
cd ~/.claude/skills/

# 2. Create project directory
mkdir student-project-evaluator
cd student-project-evaluator

# 3. Initialize structure
mkdir -p scripts examples docs

# 4. Create virtual environment (for testing scripts independently)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Install dependencies
pip install pyyaml>=6.0
```

### 2.3 Environment Variables

**For Development**:
```bash
# .env (for testing, not needed in production)
TEST_DATA_PATH=/path/to/sample/student/projects
```

**For Production**:
No environment variables required - skill uses instructor-provided paths at runtime.

---

## 3. Project Structure

### 3.1 Directory Layout

```
student-project-evaluator/
├── SKILL.md                          # Main Claude Code skill (orchestration logic)
├── README.md                         # User-facing documentation
├── PROJECT-BRIEF.md                  # Full project requirements (reference)
├── docs/
│   ├── PRD.md                        # Product Requirements Document
│   ├── PLANNING.md                   # Architecture and technical planning
│   ├── CLAUDE.md                     # This file (development rules)
│   └── TASKS.md                      # Implementation task breakdown
├── scripts/
│   ├── scan_folders.py               # Auto-detect student folders
│   ├── analyze_repo.py               # Repository analysis helpers
│   └── __init__.py                   # Make it a package (empty file)
├── examples/
│   ├── assignment-config.yml         # Example configuration
│   └── sample_evaluation_summary.md  # Example output
├── tests/                            # Unit tests (create in Phase 5)
│   ├── test_scan_folders.py
│   ├── test_analyze_repo.py
│   └── fixtures/                     # Sample student repos for testing
│       ├── student_sample1/
│       └── student_sample2/
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── LICENSE                           # MIT License

```

**CRITICAL RULE**: **Maximum 150 lines per file** (strictly enforced)

### 3.2 File Responsibility Matrix

| File | Responsibility | Max Lines |
|------|---------------|-----------|
| `SKILL.md` | Orchestration workflow, Claude instructions | 150 |
| `scan_folders.py` | Folder scanning logic | 80 |
| `analyze_repo.py` | Project type detection, metadata extraction | 100 |
| `README.md` | User documentation, installation, usage | No limit (docs) |
| `tests/*.py` | Unit tests | 150 per file |

**When file exceeds 150 lines**: Refactor into smaller modules.

Example:
```python
# Instead of one 200-line analyze_repo.py
analyze_repo.py          (50 lines - main interface)
└── analyzers/
    ├── javascript.py    (80 lines)
    ├── python.py        (70 lines)
    └── java.py          (60 lines)
```

---

## 4. Coding Standards

### 4.1 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| **Files (Python)** | `snake_case.py` | `scan_folders.py` |
| **Files (Markdown)** | `UPPERCASE.md` or `kebab-case.md` | `SKILL.md`, `assignment-config.yml` |
| **Functions** | `snake_case()` | `scan_student_folders()` |
| **Classes** | `PascalCase` | `SubmissionAnalyzer` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_REPO_SIZE_MB` |
| **Variables** | `snake_case` | `baseline_grade` |

### 4.2 Python Code Style

**Follow PEP 8** with these additions:

#### 4.2.1 Imports
```python
# Standard library first
import os
import sys
from pathlib import Path

# Third-party packages
import yaml

# Local modules
from scripts.analyze_repo import analyze_repository
```

#### 4.2.2 Function Docstrings (Required for ALL functions)

```python
def scan_student_folders(master_folder: str, exclude: list[str] = None) -> list[dict]:
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

    Raises:
        FileNotFoundError: If master_folder does not exist
        PermissionError: If master_folder is not readable

    Example:
        >>> scan_student_folders('/Assignments/A1/', exclude=['student_alice'])
        [
            {'name': 'student_bob', 'path': '/Assignments/A1/student_bob'},
            {'name': 'student_carol', 'path': '/Assignments/A1/student_carol'}
        ]
    """
```

#### 4.2.3 Type Hints (Required)

```python
# Always use type hints for function signatures
def calculate_grade(relevance: int, functionality: int, baseline: int) -> int:
    """Calculate final grade based on scores."""
    return min(100, baseline + relevance + functionality)
```

#### 4.2.4 Error Handling

**Defensive Programming** - validate inputs:

```python
def scan_student_folders(master_folder: str, exclude: list[str] = None) -> list[dict]:
    """Scan for student folders."""

    # Validate inputs
    if not master_folder:
        raise ValueError("master_folder cannot be empty")

    if not os.path.exists(master_folder):
        raise FileNotFoundError(f"Directory not found: {master_folder}")

    if not os.path.isdir(master_folder):
        raise ValueError(f"Not a directory: {master_folder}")

    # Continue with logic...
```

**User-Friendly Error Messages**:

```python
# Bad
raise Exception("Error")

# Good
raise FileNotFoundError(
    f"Student folder not found: {folder_path}\n"
    f"Please check that the path is correct and the folder exists."
)
```

### 4.3 SKILL.md Conventions

**Structure**:
```markdown
---
name: student-project-evaluator
description: [One-line description]
---

# Student Project Evaluator Skill

## When to Use This Skill
[Trigger conditions]

## Execution Flow
[Step-by-step workflow]

### Step 1: [Name]
[Detailed instructions for Claude]

### Step 2: [Name]
...
```

**Best Practices**:
- Use clear section headings (`##`, `###`)
- Include examples in code blocks with language tags
- Use tables for structured data
- Provide explicit error handling instructions

---

## 5. Configuration Management

### 5.1 Configuration Separation Principle

**CRITICAL RULE**: Configuration MUST be separated from code.

**Bad** ❌:
```python
# Hardcoded in code
GRADING_WEIGHTS = {
    'relevance': 50,
    'functionality': 50
}
```

**Good** ✅:
```python
# Read from config file
import yaml

with open('assignment-config.yml') as f:
    config = yaml.safe_load(f)

grading_weights = config['grading_weights']
```

### 5.2 Configuration Files

#### assignment-config.yml

**Purpose**: Assignment-specific evaluation criteria, generated after baseline calibration.

**Format**:
```yaml
assignment:
  name: "Web Development - Assignment 1"
  description: "Create a todo list web app..."
  evaluated_date: "2024-12-15"

baseline:
  student: "student_alice"
  grade: 85
  features_observed:
    - "CRUD operations"
    - "LocalStorage persistence"

grading_weights:
  assignment_relevance: 50  # Can be adjusted by instructor
  functionality: 50

focus_files:
  - "src/**/*.js"
  - "README.md"
  - "package.json"

project_type: "javascript_web"

evaluation_criteria:
  - "CRUD operations implemented"
  - "LocalStorage persistence working"
  - "Responsive design"
```

**Loading in Code**:
```python
import yaml
from pathlib import Path

def load_config(config_path: str) -> dict:
    """Load assignment configuration."""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Validate required fields
    required = ['assignment', 'grading_weights', 'focus_files']
    for field in required:
        if field not in config:
            raise ValueError(f"Config missing required field: {field}")

    return config
```

### 5.3 No Hardcoded Values

**Forbidden**:
- Hardcoded file paths
- Hardcoded grading weights
- Hardcoded file patterns
- Hardcoded API keys (N/A for this project, but general rule)

**Allowed**:
- Physical constants (e.g., `MAX_FILE_SIZE_MB = 100`)
- Default values with override capability

```python
# Good: Default with override
def scan_folders(master_folder, max_size_mb=100):
    """Scan folders, skip if larger than max_size_mb."""
```

---

## 6. Security Practices

### 6.1 Data Privacy

**Student Data is Sensitive**:
- Student names, IDs, grades are PII (Personally Identifiable Information)
- Must comply with FERPA (US) or equivalent regulations

**Security Measures**:
1. **Local Storage Only**: Never send student data to cloud services (except Claude Code which is authorized)
2. **File Permissions**: Output files (CSV, markdown) should be readable only by instructor
3. **No Logging of Grades**: Do not log student grades to console in production mode

**Implementation**:
```python
import os

def save_grades_csv(data: list, output_path: str):
    """Save grades with restricted permissions."""

    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data)

    # Set file permissions (Unix/Mac: owner read/write only)
    if os.name != 'nt':  # Not Windows
        os.chmod(output_path, 0o600)  # -rw------- (owner only)
```

### 6.2 API Key Security (General Rule)

**This project doesn't use external APIs**, but for future extensions:

**Bad** ❌:
```python
API_KEY = "sk-1234567890abcdef"  # NEVER hardcode API keys
```

**Good** ✅:
```python
import os

API_KEY = os.environ.get("CLAUDE_API_KEY")
if not API_KEY:
    raise ValueError("CLAUDE_API_KEY environment variable not set")
```

### 6.3 .gitignore Configuration

**Must exclude**:
```gitignore
# Environment
venv/
.env

# Test data (may contain student info)
tests/fixtures/*.csv
tests/fixtures/*.md

# Sensitive outputs (if testing with real data)
**/grades.csv
**/evaluation_summary.md

# Python
__pycache__/
*.pyc
*.pyo

# OS
.DS_Store
Thumbs.db
```

---

## 7. Testing Requirements

### 7.1 Coverage Target

**Minimum 70% code coverage** for Python scripts.

**Priority**:
1. **Critical paths**: `scan_folders.py`, `analyze_repo.py` (aim for 80%+)
2. **Error handling**: Test all error cases
3. **Edge cases**: Empty folders, missing files, large repos

### 7.2 Testing Framework

**Use pytest**:
```bash
pip install pytest pytest-cov
```

**Run tests**:
```bash
# All tests
pytest tests/

# With coverage report
pytest --cov=scripts --cov-report=term-missing tests/
```

### 7.3 Test Structure

**tests/test_scan_folders.py**:
```python
import pytest
from scripts.scan_folders import scan_student_folders

def test_scan_folders_basic(tmp_path):
    """Test scanning a directory with student folders."""

    # Setup: Create test directories
    (tmp_path / "student_alice").mkdir()
    (tmp_path / "student_bob").mkdir()
    (tmp_path / ".git").mkdir()  # Should be excluded

    # Execute
    result = scan_student_folders(str(tmp_path))

    # Assert
    assert len(result) == 2
    assert result[0]['name'] in ['student_alice', 'student_bob']
    assert all('.git' not in r['name'] for r in result)


def test_scan_folders_empty_directory(tmp_path):
    """Test scanning an empty directory."""

    result = scan_student_folders(str(tmp_path))

    assert result == []


def test_scan_folders_nonexistent_path():
    """Test error handling for nonexistent path."""

    with pytest.raises(FileNotFoundError):
        scan_student_folders("/nonexistent/path")


def test_scan_folders_with_exclusion(tmp_path):
    """Test excluding specific folders."""

    (tmp_path / "student_alice").mkdir()
    (tmp_path / "student_bob").mkdir()

    result = scan_student_folders(str(tmp_path), exclude=['student_alice'])

    assert len(result) == 1
    assert result[0]['name'] == 'student_bob'
```

### 7.4 Test Fixtures

**Create sample student projects**:
```
tests/fixtures/
├── student_sample1/        # Minimal valid project
│   ├── README.md
│   ├── src/
│   │   └── index.js
│   └── package.json
├── student_sample2/        # Complex project
│   ├── README.md
│   ├── src/
│   │   ├── app.js
│   │   ├── utils.js
│   │   └── config.js
│   ├── tests/
│   │   └── app.test.js
│   └── package.json
└── student_sample3/        # Edge case: empty project
    └── README.md           (contains "WIP - not completed")
```

---

## 8. Git Workflow

### 8.1 Commit Message Format

**Standard**: `<type>(<scope>): <description> [TaskID]`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding/updating tests
- `refactor`: Code restructuring
- `chore`: Maintenance tasks

**Examples**:
```
feat(skill): Add baseline calibration logic [P2.1]
fix(scan): Handle folders with spaces in names [P1.2]
docs(readme): Add installation instructions
test(analyze): Add tests for project type detection [P3.1]
refactor(skill): Split evaluation into separate function [P2.3]
```

### 8.2 Commit Requirements

**Minimum 10-20 commits** showing clear development progression.

**Bad Practice** ❌:
```
commit 1: "Initial commit"
commit 2: "All code"
commit 3: "Done"
```

**Good Practice** ✅:
```
commit 1: "feat(structure): Initialize project structure [P1.1]"
commit 2: "feat(scan): Implement folder scanning script [P1.2]"
commit 3: "test(scan): Add tests for folder scanning [P1.2]"
commit 4: "feat(analyze): Add project type detection [P1.3]"
commit 5: "feat(skill): Add baseline calibration step [P2.1]"
...
```

### 8.3 Branching Strategy

**For MVP (simple project)**:
- **main**: Production-ready code
- **feature/[task-id]**: Feature branches (optional for small team)

**Workflow**:
```bash
# Work directly on main for MVP (single developer)
git checkout main
git add [files]
git commit -m "feat(skill): Add baseline logic [P2.1]"
git push origin main
```

**For multi-developer (v1.1+)**:
```bash
# Create feature branch
git checkout -b feature/P2.1-baseline-calibration

# Make changes, commit
git add [files]
git commit -m "feat(skill): Add baseline calibration [P2.1]"

# Push and create PR
git push origin feature/P2.1-baseline-calibration
```

### 8.4 Git Hooks (Future Enhancement)

**pre-commit** (not required for MVP):
```bash
#!/bin/bash
# Run tests before commit
pytest tests/
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

---

## 9. Documentation Standards

### 9.1 README.md Structure

**Required Sections**:
1. **Project Overview**: What it does, who it's for
2. **Installation**: Step-by-step setup
3. **Usage**: How to run the skill
4. **Configuration**: How to customize evaluation criteria
5. **Output**: What files are generated
6. **Troubleshooting**: Common issues and solutions
7. **License**: MIT License

**Example**:
```markdown
# Student Project Evaluator

## Overview
A Claude Code skill for comparative evaluation of student coding projects.

## Installation
\`\`\`bash
cd ~/.claude/skills/
git clone [repo-url] student-project-evaluator
cd student-project-evaluator
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`
I need to grade student projects in /path/to/Assignment1/
\`\`\`

[Continue with detailed usage examples...]
```

### 9.2 Inline Code Comments

**Comment Philosophy**: Explain "WHY", not "WHAT"

**Bad** ❌:
```python
# Loop through folders
for folder in folders:
    # Check if folder exists
    if os.path.exists(folder):
        # Process the folder
        process(folder)
```

**Good** ✅:
```python
# Skip hidden folders and system directories to avoid processing .git, __pycache__, etc.
for folder in folders:
    if folder.startswith('.') or folder.startswith('__'):
        continue
    process(folder)
```

### 9.3 YAML Comments

**assignment-config.yml**:
```yaml
grading_weights:
  assignment_relevance: 50  # Assesses how well project addresses assignment requirements
  functionality: 50         # Evaluates implementation quality and completeness

focus_files:
  - "src/**/*.js"    # Main source code
  - "README.md"      # Documentation
  - "package.json"   # Dependencies and project metadata
```

---

## 10. Prompt Engineering Log

### 10.1 Purpose

Document all prompts used to generate code, diagnose issues, and make architectural decisions. This is **required for academic M.Sc. projects**.

### 10.2 Directory Structure

```
prompts/
├── README.md                # Overview, lessons learned, best practices
├── architecture/
│   ├── 001-system-design.md       # Initial architecture planning
│   └── 002-adr-baseline.md        # ADR: Dynamic baseline decision
├── code-generation/
│   ├── 001-scan-folders.md        # Generate folder scanning script
│   ├── 002-analyze-repo.md        # Generate repository analyzer
│   └── 003-skill-logic.md         # Generate SKILL.md
├── testing/
│   ├── 001-test-strategy.md       # Overall testing approach
│   └── 002-test-generation.md     # Generate unit tests
└── documentation/
    ├── 001-readme.md              # Generate README
    └── 002-prd.md                 # Generate PRD
```

### 10.3 Prompt Log Template

**prompts/code-generation/001-scan-folders.md**:
```markdown
# Prompt: Generate Folder Scanning Script

**Date**: 2024-12-15
**Task ID**: P1.2
**Goal**: Create a Python script to auto-detect student folders

## Prompt

\`\`\`
Create a Python script called scan_folders.py that:

1. Takes a master folder path as input
2. Returns a list of all subdirectories (student folders)
3. Excludes hidden folders (starting with '.')
4. Accepts an optional exclude list (e.g., baseline student folder)
5. Returns data as list of dicts: [{'name': 'student_bob', 'path': '/full/path'}]
6. Includes full docstrings and type hints
7. Handles errors gracefully (FileNotFoundError, PermissionError)

Requirements:
- Python 3.8+
- No external dependencies (use stdlib only)
- Maximum 80 lines
\`\`\`

## Response

[Full generated code or summary]

## Evaluation

**What worked well**:
- Generated clean, readable code
- Error handling was comprehensive

**What needed adjustment**:
- Initial version didn't sort results alphabetically
- Added sorting after manual review

## Lessons Learned

- Always specify sorting requirements upfront
- Type hints improve code clarity significantly
```

### 10.4 README for Prompt Log

**prompts/README.md**:
```markdown
# Prompt Engineering Log

## Overview

This directory documents all AI-assisted development for the Student Project Evaluator project.

## Categories

- **architecture/**: System design, ADRs, architectural decisions
- **code-generation/**: Scripts, SKILL.md logic, utilities
- **testing/**: Test strategy, test generation
- **documentation/**: README, PRD, planning documents

## Lessons Learned

### Best Practices

1. **Be specific**: Specify line limits, dependencies, error handling requirements upfront
2. **Request type hints**: Always ask for full type annotations
3. **Iterative refinement**: Generate, evaluate, refine in multiple rounds
4. **Context preservation**: Reference previous prompts when building on existing code

### Common Pitfalls

1. **Vague requirements**: "Create a script" → too generic, results in missing features
2. **No examples**: Providing input/output examples dramatically improves quality
3. **Ignoring constraints**: Forgetting to mention 150-line limit led to refactoring later

## Statistics

- Total prompts: 12
- Categories: 4 (architecture, code, testing, docs)
- Average iterations per component: 1.5
- Most refined component: SKILL.md (3 iterations)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-15 | Initial development rules for MVP |

---

**End of Claude Development Rules**
