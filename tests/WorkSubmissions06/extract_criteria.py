#!/usr/bin/env python3
"""
Extract criteria from student markdown files in WorkSubmissions06
"""
import os
import json
import re
from pathlib import Path
from collections import defaultdict

# Base directory
BASE_DIR = Path(r"E:\Projects\student-project-evaluator\tests\WorkSubmissions06")
OUTPUT_DIR = Path(r"E:\Projects\student-project-evaluator\tests\WorkSubmissions06\outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Criteria graph: {criterion_name: {"students": [], "count": 0, "sources": {}}}
criteria_graph = defaultdict(lambda: {"students": [], "count": 0, "sources": defaultdict(list)})

# Student data: {student_id: {"criteria": [], "md_files": []}}
student_data = defaultdict(lambda: {"criteria": set(), "md_files": []})

# File-based criteria detection
FILENAME_CRITERIA = {
    r"(?i)prd\.md|productrequ": "PRD Document",
    r"(?i)testing\.md|test\.md": "Testing Documentation",
    r"(?i)contributing\.md": "Contributing Guide",
    r"(?i)quickstart\.md|quick-start\.md": "Quick Start Guide",
    r"(?i)architecture\.md|design\.md": "Architecture Documentation",
    r"(?i)changelog\.md|changes\.md": "Changelog",
    r"(?i)api\.md|api_docs\.md": "API Documentation",
    r"(?i)roadmap\.md": "Roadmap",
    r"(?i)deployment\.md|deploy\.md": "Deployment Guide",
    r"(?i)troubleshooting\.md|faq\.md": "Troubleshooting Guide",
    r"(?i)readme\.md": "README",
}

# Content-based extraction patterns
EXTRACTION_PATTERNS = {
    # Testing
    r"(?i)\b(unit test|unittest|unit testing)\b": "Unit Tests",
    r"(?i)\b(integration test|integration testing)\b": "Integration Tests",
    r"(?i)\b(e2e test|end-to-end test|e2e testing)\b": "E2E Tests",
    r"(?i)\b(test coverage|code coverage|coverage:?\s*[\d~]+%)\b": "Test Coverage Metrics",
    r"(?i)\b(pytest|jest|mocha|junit)\b": "Testing Framework",

    # Quality Standards
    r"(?i)\b(eslint|\.eslintrc)\b": "ESLint Configuration",
    r"(?i)\b(pylint|\.pylintrc)\b": "Pylint Configuration",
    r"(?i)\b(prettier|\.prettierrc)\b": "Prettier Formatting",
    r"(?i)\b(black formatter|black formatting)\b": "Black Formatting",
    r"(?i)\b(pre-commit hook|pre-commit|\.pre-commit)\b": "Pre-commit Hooks",
    r"(?i)\b(type checking|mypy|typescript strict)\b": "Type Checking",
    r"(?i)\b(code review|peer review)\b": "Code Review Process",
    r"(?i)\b(code style guide|coding standards|style guide)\b": "Code Style Guide",
    r"(?i)\b(pep ?8 compli|follows? pep ?8)\b": "PEP8 Compliance",

    # DevOps
    r"(?i)\b(ci/?cd|continuous integration|github actions|gitlab ci)\b": "CI/CD Pipeline",
    r"(?i)\b(docker|dockerfile|containeriz)\b": "Docker",
    r"(?i)\b(kubernetes|k8s)\b": "Kubernetes",

    # Planning & Analysis
    r"(?i)##\s*(problem statement|problem)\b": "Problem Statement",
    r"(?i)##\s*(solution|proposed solution)\b": "Solution Overview",
    r"(?i)##\s*(requirements|functional requirements)\b": "Functional Requirements",
    r"(?i)##\s*(use case|use cases)\b": "Use Case Documentation",
    r"(?i)##\s*(cost analysis|budget|costs)\b": "Cost Analysis",
    r"(?i)##\s*(risk analysis|risks)\b": "Risk Analysis",
    r"(?i)##\s*(success metrics|kpis|metrics)\b": "Success Metrics",
    r"(?i)##\s*(assumptions|constraints)\b": "Assumptions Documentation",
    r"(?i)##\s*(roadmap|future work)\b": "Roadmap",
    r"(?i)##\s*(design decision|trade-?offs)\b": "Design Decision Documentation",
    r"(?i)##\s*(user stories|user personas)\b": "User Research",

    # Documentation
    r"(?i)##\s*(api|endpoints|api reference)\b": "API Documentation",
    r"(?i)##\s*(installation|setup|getting started)\b": "Installation Instructions",
    r"(?i)##\s*(usage|how to use)\b": "Usage Guide",
    r"(?i)##\s*(screenshots|demo|examples)\b": "Screenshots",
    r"(?i)##\s*(architecture|design)\b": "Architecture Documentation",
    r"(?i)##\s*(contributing|development)\b": "Contributing Guide",
}

# Negative patterns (don't count these)
NEGATIVE_PATTERNS = [
    r"(?i)\b(todo|fixme|not yet|not complete|missing|planned|future work|out of scope|skipped|omitted)\b",
    r"(?i)\bwill (add|implement|create)\b",
    r"(?i)\b(might be|considering|if time permits|would be nice|ideally|optional)\b",
]

def is_student_folder(path):
    """Check if this is a student folder"""
    return path.is_dir() and path.name.startswith("Participant_")

def is_negative_context(text):
    """Check if text contains negative indicators"""
    for pattern in NEGATIVE_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def extract_from_filename(filepath):
    """Extract criteria based on filename"""
    filename = filepath.name
    criteria = []
    for pattern, criterion in FILENAME_CRITERIA.items():
        if re.search(pattern, filename):
            criteria.append(criterion)
    return criteria

def extract_from_content(content, filepath):
    """Extract criteria from file content"""
    criteria = []

    # Check each pattern
    for pattern, criterion in EXTRACTION_PATTERNS.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            # Get context around the match (100 chars before and after)
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end]

            # Skip if negative context
            if not is_negative_context(context):
                criteria.append(criterion)
                break  # Only count once per file

    return criteria

def process_student(student_dir):
    """Process all markdown files for a student"""
    student_id = student_dir.name
    print(f"Processing {student_id}...")

    # Find all .md files
    md_files = list(student_dir.rglob("*.md"))
    student_data[student_id]["md_files"] = [str(f.relative_to(BASE_DIR)) for f in md_files]

    print(f"  Found {len(md_files)} markdown files")

    # Extract criteria from each file
    for md_file in md_files:
        try:
            # Extract from filename
            file_criteria = extract_from_filename(md_file)
            for criterion in file_criteria:
                student_data[student_id]["criteria"].add(criterion)

            # Extract from content
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            content_criteria = extract_from_content(content, md_file)
            for criterion in content_criteria:
                student_data[student_id]["criteria"].add(criterion)

        except Exception as e:
            print(f"  Warning: Error reading {md_file}: {e}")
            continue

    print(f"  Extracted {len(student_data[student_id]['criteria'])} unique criteria")
    return student_id, student_data[student_id]["criteria"]

def build_criteria_graph():
    """Build the criteria graph from student data"""
    for student_id, data in student_data.items():
        for criterion in data["criteria"]:
            if student_id not in criteria_graph[criterion]["students"]:
                criteria_graph[criterion]["students"].append(student_id)
                criteria_graph[criterion]["count"] = len(criteria_graph[criterion]["students"])

def main():
    print("=" * 80)
    print("STUDENT PROJECT EVALUATOR - WorkSubmissions06")
    print("=" * 80)

    # Find all student folders
    student_folders = [f for f in BASE_DIR.iterdir() if is_student_folder(f)]
    student_folders.sort()

    print(f"\n[Step 1] Found {len(student_folders)} student folders\n")

    # Process each student
    print("[Step 2] Reading markdown files and extracting criteria...\n")
    for i, student_dir in enumerate(student_folders, 1):
        print(f"[{i}/{len(student_folders)}] ", end="")
        process_student(student_dir)

    # Build criteria graph
    print(f"\n[Step 3] Building criteria graph...")
    build_criteria_graph()

    # Save intermediate results
    output_file = OUTPUT_DIR / "criteria_extraction_raw.json"
    output_data = {
        "student_data": {
            sid: {
                "criteria": list(data["criteria"]),
                "md_files": data["md_files"],
                "criteria_count": len(data["criteria"])
            }
            for sid, data in student_data.items()
        },
        "criteria_graph": {
            criterion: {
                "students": data["students"],
                "count": data["count"],
                "prevalence": round(data["count"] / len(student_folders), 3)
            }
            for criterion, data in criteria_graph.items()
        },
        "summary": {
            "total_students": len(student_folders),
            "total_criteria": len(criteria_graph),
            "total_md_files": sum(len(data["md_files"]) for data in student_data.values())
        }
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n[Step 4] Saved raw extraction to {output_file}")

    # Print summary
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Students processed: {len(student_folders)}")
    print(f"Total markdown files: {output_data['summary']['total_md_files']}")
    print(f"Unique criteria discovered: {len(criteria_graph)}")
    print(f"\nTop 10 most common criteria:")
    sorted_criteria = sorted(criteria_graph.items(), key=lambda x: x[1]["count"], reverse=True)
    for i, (criterion, data) in enumerate(sorted_criteria[:10], 1):
        prevalence = (data["count"] / len(student_folders)) * 100
        print(f"  {i:2d}. {criterion:<40s} - {data['count']:2d}/{len(student_folders)} ({prevalence:.1f}%)")

    print(f"\nRare criteria (≤15% prevalence - get bonus weight):")
    rare_criteria = [(c, d) for c, d in sorted_criteria if d["count"] / len(student_folders) <= 0.15]
    print(f"  Found {len(rare_criteria)} rare criteria")
    for criterion, data in rare_criteria[:10]:
        prevalence = (data["count"] / len(student_folders)) * 100
        print(f"    - {criterion:<40s} - {data['count']:2d}/{len(student_folders)} ({prevalence:.1f}%)")

    return output_data

if __name__ == "__main__":
    main()
