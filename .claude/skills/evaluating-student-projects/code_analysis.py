#!/usr/bin/env python3
"""
Code Analysis Utilities for Student Project Evaluation

Provides functions to verify implementation beyond markdown documentation:
- Git repository analysis (commits, PROMPT_BOOK.md, branching)
- Security scanning (hardcoded secrets, .env, .gitignore)
- Code quality verification (linting configs, test frameworks)
"""

import os
import re
import subprocess
from pathlib import Path
import glob
import json


def analyze_git_repository(student_folder):
    """
    Extract git-based criteria from repository

    Returns dict with:
    - Git_Commits_10Plus: bool (2 points in actual grading)
    - Meaningful_Commit_Messages: bool (2 points)
    - Prompt_Book: bool (5 points!)
    - Branching_Strategy: bool (1 point)
    - Total_Commits: int
    - Avg_Message_Length: int
    """

    student_path = Path(student_folder)
    criteria = {}

    # Check if it's a git repository
    if not (student_path / ".git").exists():
        return {
            "Git_Commits_10Plus": False,
            "Meaningful_Commit_Messages": False,
            "Prompt_Book": False,
            "Branching_Strategy": False,
            "Total_Commits": 0,
            "Is_Git_Repo": False
        }

    try:
        # Count commits
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=student_folder,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            total_commits = int(result.stdout.strip())
            criteria["Total_Commits"] = total_commits
            criteria["Git_Commits_10Plus"] = total_commits >= 10
        else:
            criteria["Total_Commits"] = 0
            criteria["Git_Commits_10Plus"] = False

        # Analyze commit message quality
        result = subprocess.run(
            ["git", "log", "--format=%s"],
            cwd=student_folder,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            messages = [m for m in result.stdout.strip().split('\n') if m]
            if messages:
                avg_length = sum(len(m) for m in messages) / len(messages)
                criteria["Avg_Message_Length"] = int(avg_length)
                # Meaningful = average length >= 20 characters
                criteria["Meaningful_Commit_Messages"] = avg_length >= 20
            else:
                criteria["Avg_Message_Length"] = 0
                criteria["Meaningful_Commit_Messages"] = False
        else:
            criteria["Avg_Message_Length"] = 0
            criteria["Meaningful_Commit_Messages"] = False

        # Check for PROMPT_BOOK.md (worth 5 points!)
        prompt_book_patterns = [
            "PROMPT_BOOK.md",
            "PROMPTBOOK.md",
            "prompt_book.md",
            "promptbook.md",
            "docs/PROMPT_BOOK.md",
            "docs/PROMPTBOOK.md"
        ]

        criteria["Prompt_Book"] = any(
            (student_path / pattern).exists() for pattern in prompt_book_patterns
        )

        # Check branching strategy
        result = subprocess.run(
            ["git", "branch", "-a"],
            cwd=student_folder,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            branches = [b for b in result.stdout.strip().split('\n') if b]
            # Has branching strategy if more than just main/master
            criteria["Branching_Strategy"] = len(branches) > 1
        else:
            criteria["Branching_Strategy"] = False

        criteria["Is_Git_Repo"] = True

    except subprocess.TimeoutExpired:
        return {
            "Git_Commits_10Plus": False,
            "Meaningful_Commit_Messages": False,
            "Prompt_Book": False,
            "Branching_Strategy": False,
            "Total_Commits": 0,
            "Is_Git_Repo": True,
            "Error": "Git command timeout"
        }
    except Exception as e:
        return {
            "Git_Commits_10Plus": False,
            "Meaningful_Commit_Messages": False,
            "Prompt_Book": False,
            "Branching_Strategy": False,
            "Total_Commits": 0,
            "Is_Git_Repo": True,
            "Error": str(e)
        }

    return criteria


def scan_for_secrets(student_folder):
    """
    Scan for hardcoded secrets in code files

    Returns dict with:
    - No_Hardcoded_Secrets: bool (5 points - CRITICAL)
    - Env_Example_Exists: bool (2 points)
    - Gitignore_Exists: bool (1 point)
    - Gitignore_Properly_Configured: bool (2 points)
    - Secrets_Found: list of file paths
    """

    student_path = Path(student_folder)
    criteria = {}

    # Patterns for common secrets
    secret_patterns = [
        (r'api[_-]?key\s*=\s*["\'][\w\-]{20,}["\']', "API key"),
        (r'password\s*=\s*["\'][^"\']{8,}["\']', "Password"),
        (r'token\s*=\s*["\'][\w\-]{20,}["\']', "Token"),
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI key"),
        (r'ghp_[a-zA-Z0-9]{36,}', "GitHub token"),
        (r'xox[baprs]-[a-zA-Z0-9-]{10,}', "Slack token"),
        (r'AIza[0-9A-Za-z\-_]{35}', "Google API key"),
        (r'AKIA[0-9A-Z]{16}', "AWS key"),
    ]

    # Scan code files (not node_modules, venv, etc.)
    exclude_dirs = {
        "node_modules", "venv", ".venv", "env", ".env",
        "__pycache__", ".git", "dist", "build", ".next"
    }

    code_extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs"}
    secrets_found = []

    try:
        for root, dirs, files in os.walk(student_folder):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if Path(file).suffix in code_extensions:
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')

                        for pattern, secret_type in secret_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                secrets_found.append({
                                    "file": str(file_path.relative_to(student_path)),
                                    "type": secret_type,
                                    "count": len(matches)
                                })
                    except Exception:
                        continue
    except Exception as e:
        criteria["Error"] = str(e)

    criteria["No_Hardcoded_Secrets"] = len(secrets_found) == 0
    criteria["Secrets_Found"] = secrets_found

    # Check for .env.example
    env_example_patterns = [".env.example", ".env.sample", "env.example", ".env.template"]
    criteria["Env_Example_Exists"] = any(
        (student_path / pattern).exists() for pattern in env_example_patterns
    )

    # Check for .gitignore
    criteria["Gitignore_Exists"] = (student_path / ".gitignore").exists()

    # Check if .gitignore properly configured (has .env entry)
    if criteria["Gitignore_Exists"]:
        try:
            gitignore_content = (student_path / ".gitignore").read_text()
            # Check for .env pattern
            has_env = bool(re.search(r'^\.env$|^\.env\s|^\*\.env', gitignore_content, re.MULTILINE))
            criteria["Gitignore_Properly_Configured"] = has_env
        except Exception:
            criteria["Gitignore_Properly_Configured"] = False
    else:
        criteria["Gitignore_Properly_Configured"] = False

    return criteria


def check_code_quality_tools(student_folder):
    """
    Check for code quality tool configurations

    Returns dict with:
    - ESLint_Configured: bool
    - Pylint_Configured: bool
    - Ruff_Configured: bool
    - Flake8_Configured: bool
    - Black_Configured: bool
    - Prettier_Configured: bool
    - MyPy_Configured: bool
    - TypeScript_Configured: bool
    - Pre_Commit_Configured: bool
    - Test_Framework_Configured: bool
    - Quality_Tools_Count: int
    """

    student_path = Path(student_folder)
    criteria = {}

    # Linting configurations
    criteria["ESLint_Configured"] = any([
        (student_path / ".eslintrc").exists(),
        (student_path / ".eslintrc.js").exists(),
        (student_path / ".eslintrc.json").exists(),
        (student_path / ".eslintrc.yml").exists(),
    ])

    criteria["Pylint_Configured"] = any([
        (student_path / ".pylintrc").exists(),
        (student_path / "pylintrc").exists(),
        (student_path / "pyproject.toml").exists(),  # Can contain pylint config
    ])

    criteria["Ruff_Configured"] = any([
        (student_path / "ruff.toml").exists(),
        (student_path / "pyproject.toml").exists(),  # Can contain ruff config
    ])

    criteria["Flake8_Configured"] = any([
        (student_path / ".flake8").exists(),
        (student_path / "setup.cfg").exists(),
        (student_path / "tox.ini").exists(),
    ])

    # Formatters
    criteria["Black_Configured"] = any([
        (student_path / "pyproject.toml").exists(),  # Can contain black config
        # Check if black is in requirements/dependencies
        check_dependency(student_path, "black")
    ])

    criteria["Prettier_Configured"] = any([
        (student_path / ".prettierrc").exists(),
        (student_path / ".prettierrc.js").exists(),
        (student_path / ".prettierrc.json").exists(),
        (student_path / "prettier.config.js").exists(),
    ])

    # Type checking
    criteria["MyPy_Configured"] = any([
        (student_path / "mypy.ini").exists(),
        (student_path / ".mypy.ini").exists(),
        (student_path / "pyproject.toml").exists(),  # Can contain mypy config
    ])

    criteria["TypeScript_Configured"] = any([
        (student_path / "tsconfig.json").exists(),
    ])

    # Pre-commit hooks
    criteria["Pre_Commit_Configured"] = any([
        (student_path / ".pre-commit-config.yaml").exists(),
        (student_path / ".pre-commit-config.yml").exists(),
    ])

    # Test frameworks
    criteria["Test_Framework_Configured"] = any([
        (student_path / "pytest.ini").exists(),
        (student_path / ".pytest.ini").exists(),
        (student_path / "jest.config.js").exists(),
        (student_path / "jest.config.ts").exists(),
        (student_path / "vitest.config.ts").exists(),
        (student_path / "karma.conf.js").exists(),
    ])

    # Count total quality tools
    criteria["Quality_Tools_Count"] = sum([
        criteria["ESLint_Configured"],
        criteria["Pylint_Configured"],
        criteria["Ruff_Configured"],
        criteria["Flake8_Configured"],
        criteria["Black_Configured"],
        criteria["Prettier_Configured"],
        criteria["MyPy_Configured"],
        criteria["TypeScript_Configured"],
        criteria["Pre_Commit_Configured"],
        criteria["Test_Framework_Configured"],
    ])

    return criteria


def check_dependency(student_folder, package_name):
    """Check if a package is in requirements or package.json"""
    student_path = Path(student_folder)

    # Check Python requirements
    req_files = ["requirements.txt", "requirements-dev.txt", "pyproject.toml"]
    for req_file in req_files:
        req_path = student_path / req_file
        if req_path.exists():
            try:
                content = req_path.read_text()
                if package_name in content.lower():
                    return True
            except Exception:
                continue

    # Check Node package.json
    package_json = student_path / "package.json"
    if package_json.exists():
        try:
            content = json.loads(package_json.read_text())
            deps = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
            if package_name in deps:
                return True
        except Exception:
            pass

    return False


def run_full_code_analysis(student_folder):
    """
    Run all code analysis checks

    Returns combined dict with all criteria from:
    - Git repository analysis
    - Security scanning
    - Code quality tool verification
    """

    results = {
        "student_folder": student_folder,
        "analysis_complete": True
    }

    try:
        # Git analysis
        git_results = analyze_git_repository(student_folder)
        results.update(git_results)

        # Security scanning
        security_results = scan_for_secrets(student_folder)
        results.update(security_results)

        # Code quality tools
        quality_results = check_code_quality_tools(student_folder)
        results.update(quality_results)

    except Exception as e:
        results["analysis_complete"] = False
        results["error"] = str(e)

    return results


def format_criteria_summary(analysis_results):
    """Format analysis results as criteria summary"""

    criteria_list = []

    # Git criteria
    if analysis_results.get("Git_Commits_10Plus"):
        criteria_list.append("Git Commits 10+ (verified)")
    if analysis_results.get("Meaningful_Commit_Messages"):
        criteria_list.append("Meaningful Commit Messages (verified)")
    if analysis_results.get("Prompt_Book"):
        criteria_list.append("PROMPT_BOOK.md (verified)")
    if analysis_results.get("Branching_Strategy"):
        criteria_list.append("Branching Strategy (verified)")

    # Security criteria
    if analysis_results.get("No_Hardcoded_Secrets"):
        criteria_list.append("No Hardcoded Secrets (verified)")
    if analysis_results.get("Env_Example_Exists"):
        criteria_list.append(".env.example (verified)")
    if analysis_results.get("Gitignore_Exists"):
        criteria_list.append(".gitignore (verified)")
    if analysis_results.get("Gitignore_Properly_Configured"):
        criteria_list.append(".gitignore Properly Configured (verified)")

    # Quality tool criteria
    if analysis_results.get("ESLint_Configured"):
        criteria_list.append("ESLint Configuration (verified)")
    if analysis_results.get("Pylint_Configured"):
        criteria_list.append("Pylint Configuration (verified)")
    if analysis_results.get("Ruff_Configured"):
        criteria_list.append("Ruff Configuration (verified)")
    if analysis_results.get("Black_Configured"):
        criteria_list.append("Black Formatting (verified)")
    if analysis_results.get("Prettier_Configured"):
        criteria_list.append("Prettier Formatting (verified)")
    if analysis_results.get("MyPy_Configured"):
        criteria_list.append("MyPy Type Checking (verified)")
    if analysis_results.get("TypeScript_Configured"):
        criteria_list.append("TypeScript Configuration (verified)")
    if analysis_results.get("Pre_Commit_Configured"):
        criteria_list.append("Pre-commit Hooks (verified)")
    if analysis_results.get("Test_Framework_Configured"):
        criteria_list.append("Test Framework Configured (verified)")

    return criteria_list


if __name__ == "__main__":
    # Test the analysis on a sample folder
    import sys

    if len(sys.argv) > 1:
        test_folder = sys.argv[1]
        print(f"Analyzing: {test_folder}")
        print("=" * 80)

        results = run_full_code_analysis(test_folder)

        print("\nGit Analysis:")
        print(f"  Commits: {results.get('Total_Commits', 0)}")
        print(f"  10+ commits: {results.get('Git_Commits_10Plus', False)}")
        print(f"  Meaningful messages: {results.get('Meaningful_Commit_Messages', False)}")
        print(f"  PROMPT_BOOK.md: {results.get('Prompt_Book', False)}")
        print(f"  Branching: {results.get('Branching_Strategy', False)}")

        print("\nSecurity:")
        print(f"  No secrets: {results.get('No_Hardcoded_Secrets', False)}")
        print(f"  .env.example: {results.get('Env_Example_Exists', False)}")
        print(f"  .gitignore: {results.get('Gitignore_Exists', False)}")
        print(f"  .gitignore configured: {results.get('Gitignore_Properly_Configured', False)}")

        if results.get('Secrets_Found'):
            print(f"\n  WARNING: Found {len(results['Secrets_Found'])} potential secrets:")
            for secret in results['Secrets_Found']:
                print(f"    - {secret['file']}: {secret['type']} ({secret['count']}x)")

        print("\nCode Quality Tools:")
        print(f"  Total tools: {results.get('Quality_Tools_Count', 0)}")
        print(f"  ESLint: {results.get('ESLint_Configured', False)}")
        print(f"  Pylint: {results.get('Pylint_Configured', False)}")
        print(f"  Ruff: {results.get('Ruff_Configured', False)}")
        print(f"  Black: {results.get('Black_Configured', False)}")
        print(f"  Prettier: {results.get('Prettier_Configured', False)}")
        print(f"  MyPy: {results.get('MyPy_Configured', False)}")
        print(f"  TypeScript: {results.get('TypeScript_Configured', False)}")
        print(f"  Pre-commit: {results.get('Pre_Commit_Configured', False)}")
        print(f"  Test framework: {results.get('Test_Framework_Configured', False)}")

        print("\nVerified Criteria:")
        for criterion in format_criteria_summary(results):
            print(f"  ✓ {criterion}")
    else:
        print("Usage: python code_analysis.py <student_folder_path>")
