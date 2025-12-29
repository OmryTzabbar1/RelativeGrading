#!/usr/bin/env python3
"""
Enhanced criteria extraction with comprehensive pattern matching
Based on EXTRACTION.md and CATEGORIES.md
"""
import os
import json
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(r"E:\Projects\student-project-evaluator\tests\WorkSubmissions06")
OUTPUT_DIR = Path(r"E:\Projects\student-project-evaluator\tests\WorkSubmissions06\outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize data structures
criteria_graph = defaultdict(lambda: {
    "students": [],
    "count": 0,
    "sources": defaultdict(list),
    "category": None,
    "weight": 0.0
})
student_data = defaultdict(lambda: {"criteria": set(), "md_files": []})

# FILENAME-BASED CRITERIA DETECTION
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
    r"(?i)security\.md": "Security Documentation",
    r"(?i)references\.md": "References Documentation",
    r"(?i)license\.md|licence\.md": "License Documentation",
}

# CONTENT-BASED EXTRACTION PATTERNS (Comprehensive)
EXTRACTION_PATTERNS = {
    # === TESTING ===
    r"(?i)\b(unit test|unittest|unit testing)\b": "Unit Tests",
    r"(?i)\b(integration test|integration testing)\b": "Integration Tests",
    r"(?i)\b(e2e test|end-to-end test|e2e testing)\b": "E2E Tests",
    r"(?i)\b(test coverage|code coverage|coverage:?\s*[\d~]+%)\b": "Test Coverage Metrics",
    r"(?i)\b(pytest|jest|mocha|junit)\b": "Testing Framework",
    r"(?i)\b(\d+\+? tests?|\d+ test cases?|~\d+ tests?)\b": "Test Suite",
    r"(?i)##\s*Testing\b": "Testing Documentation",

    # === CODE QUALITY ===
    r"(?i)\b(eslint|\.eslintrc)\b": "ESLint Configuration",
    r"(?i)\b(pylint|\.pylintrc)\b": "Pylint Configuration",
    r"(?i)\b(prettier|\.prettierrc)\b": "Prettier Formatting",
    r"(?i)\b(black formatter|black formatting)\b": "Black Formatting",
    r"(?i)\b(pre-commit hook|pre-commit|\.pre-commit)\b": "Pre-commit Hooks",
    r"(?i)\b(type checking|mypy|typescript strict)\b": "Type Checking",
    r"(?i)\b(code review|peer review)\b": "Code Review Process",
    r"(?i)\b(code style guide|coding standards|style guide)\b": "Code Style Guide",
    r"(?i)\b(pep ?8 compli|follows? pep ?8)\b": "PEP8 Compliance",
    r"(?i)\b(quality gates?|quality checks?)\b": "Quality Gates",
    r"(?i)\b(static analysis|sonarqube|sonarcloud)\b": "Static Analysis",
    r"(?i)\b(linting|linter configuration)\b": "Linting Configuration",

    # === DEVOPS ===
    r"(?i)\b(ci/?cd|continuous integration|github actions?|gitlab ci)\b": "CI/CD Pipeline",
    r"(?i)\b(docker|dockerfile|containeriz)\b": "Docker",
    r"(?i)\b(kubernetes|k8s)\b": "Kubernetes",
    r"(?i)\b(automated deployment|deployment automation)\b": "Automated Deployment",
    r"(?i)\b(environment variables?|\.env)\b": "Environment Configuration",

    # === PLANNING & ANALYSIS ===
    r"(?i)##\s*(problem statement|problem)\b": "Problem Statement",
    r"(?i)##\s*(solution|proposed solution)\b": "Solution Overview",
    r"(?i)##\s*(requirements|functional requirements)\b": "Functional Requirements",
    r"(?i)##\s*(non-functional requirements)\b": "Non-functional Requirements",
    r"(?i)##\s*(use case|use cases)\b": "Use Case Documentation",
    r"(?i)##\s*(cost analysis|budget|costs)\b": "Cost Analysis",
    r"(?i)##\s*(risk analysis|risks)\b": "Risk Analysis",
    r"(?i)##\s*(success metrics|kpis|metrics)\b": "Success Metrics",
    r"(?i)##\s*(assumptions|constraints)\b": "Assumptions Documentation",
    r"(?i)##\s*(roadmap|future work)\b": "Roadmap",
    r"(?i)##\s*(design decision|trade-?offs)\b": "Design Decision Documentation",
    r"(?i)##\s*(user stories|user personas)\b": "User Research",
    r"(?i)##\s*(project goals?|objectives?)\b": "Project Goals",
    r"(?i)##\s*(scope|project scope)\b": "Scope Documentation",
    r"(?i)##\s*(timeline|schedule|milestones?)\b": "Timeline Documentation",

    # === DOCUMENTATION ===
    r"(?i)##\s*(api|endpoints|api reference)\b": "API Documentation",
    r"(?i)##\s*(installation|setup|getting started)\b": "Installation Instructions",
    r"(?i)##\s*(usage|how to use)\b": "Usage Guide",
    r"(?i)##\s*(architecture|design)\b": "Architecture Documentation",
    r"(?i)##\s*(contributing|development)\b": "Contributing Guide",
    r"(?i)##\s*(troubleshooting|common (problems|issues))\b": "Troubleshooting Guide",
    r"(?i)##\s*(examples?|demos?)\b": "Examples Documentation",
    r"(?i)##\s*(security|threat model)\b": "Security Documentation",
    r"(?i)##\s*(references?|citations?|bibliography)\b": "References Documentation",
    r"(?i)\b(docstrings?|documentation strings?)\b": "Code Documentation",
    r"(?i)\b(inline comments?|code comments?)\b": "Code Comments",

    # === VISUALS ===
    r"(?i)##\s*(screenshots?|demo|visuals?)\b": "Screenshots",
    r"(?i)\b(architecture diagram|system diagram)\b": "Architecture Diagram",
    r"(?i)\b(flowchart|flow diagram)\b": "Flowchart",
    r"(?i)\b(visualization|charts?|graphs?)\b": "Data Visualization",
    r"(?i)\b(demo video|video walkthrough)\b": "Demo Video",

    # === RESEARCH ===
    r"(?i)\b(data analysis|statistical analysis)\b": "Statistical Analysis",
    r"(?i)\b(jupyter notebooks?|ipynb)\b": "Jupyter Notebooks",
    r"(?i)\b(experiment|experimentation)\b": "Experimental Research",
    r"(?i)\b(benchmarking|benchmark results?)\b": "Benchmarking",
    r"(?i)\b(user research|user study)\b": "User Research",
    r"(?i)\b(literature review|academic research)\b": "Literature Review",

    # === BUSINESS ===
    r"(?i)\b(roi analysis|return on investment)\b": "ROI Analysis",
    r"(?i)\b(market analysis|market research)\b": "Market Research",
    r"(?i)\b(competitive analysis|competitor comparison)\b": "Competitive Analysis",
    r"(?i)\b(business model|revenue model)\b": "Business Model",
    r"(?i)\b(cost-benefit|cost benefit)\b": "Cost-Benefit Analysis",
}

# SPECIAL PATTERNS (more specific matching)
SPECIAL_PATTERNS = {
    # Look for explicit lists/badges in READMEs
    "coverage_badge": (r"!\[.*[Cc]overage.*\d+%", "Test Coverage Metrics"),
    "test_badge": (r"!\[.*[Tt]ests.*\d+", "Test Suite"),
    "license_badge": (r"!\[.*[Ll]icense", "License Documentation"),
    "iso_compliance": (r"ISO[- ]?\d+", "ISO Compliance Documentation"),
    "self_assessment": (r"[Ss]elf[- ]?[Aa]ssessment", "Self-Assessment Documentation"),
}

# NEGATIVE PATTERNS - DON'T COUNT
NEGATIVE_PATTERNS = [
    r"(?i)\b(todo|fixme|not yet|not complete|not implemented|missing|planned|future work|out of scope|skipped|omitted)\b",
    r"(?i)\bwill (add|implement|create|build)\b",
    r"(?i)\b(might be|considering|if time permits|would be nice|ideally|optional)\b",
    r"(?i)\b(stretch goal|nice to have|bonus)\b",
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
    criteria = set()

    # Regular extraction patterns
    for pattern, criterion in EXTRACTION_PATTERNS.items():
        matches = list(re.finditer(pattern, content))
        if matches:
            # Check first match for negative context
            match = matches[0]
            start = max(0, match.start() - 150)
            end = min(len(content), match.end() + 150)
            context = content[start:end]

            if not is_negative_context(context):
                criteria.add(criterion)

    # Special patterns
    for name, (pattern, criterion) in SPECIAL_PATTERNS.items():
        if re.search(pattern, content):
            criteria.add(criterion)

    return list(criteria)

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
                criteria_graph[criterion]["sources"][student_id].append(str(md_file.name))

            # Extract from content
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            content_criteria = extract_from_content(content, md_file)
            for criterion in content_criteria:
                student_data[student_id]["criteria"].add(criterion)
                criteria_graph[criterion]["sources"][student_id].append(str(md_file.name))

        except Exception as e:
            print(f"  Warning: Error reading {md_file.name}: {e}")
            continue

    print(f"  Extracted {len(student_data[student_id]['criteria'])} unique criteria")
    return student_id, student_data[student_id]["criteria"]

def build_criteria_graph(total_students):
    """Build the criteria graph from student data"""
    for student_id, data in student_data.items():
        for criterion in data["criteria"]:
            if student_id not in criteria_graph[criterion]["students"]:
                criteria_graph[criterion]["students"].append(student_id)
                criteria_graph[criterion]["count"] = len(criteria_graph[criterion]["students"])
                criteria_graph[criterion]["prevalence"] = criteria_graph[criterion]["count"] / total_students

def categorize_criteria():
    """Categorize criteria based on CATEGORIES.md rules"""

    # Category keywords from CATEGORIES.md
    CATEGORY_KEYWORDS = {
        "Documentation": ["readme", "api doc", "user guide", "usage guide", "changelog", "contributing",
                         "license", "installation", "setup", "getting started", "faq", "wiki", "manual",
                         "reference", "examples", "troubleshooting", "security doc", "code documentation"],
        "Planning": ["prd", "product requirements", "architecture", "design doc", "technical spec",
                    "roadmap", "milestones", "requirements", "system design", "schema", "wireframe",
                    "user stories", "use case", "problem statement", "solution", "project goals",
                    "success metrics", "kpi", "assumptions", "constraints", "scope", "design decision",
                    "trade-off", "technology", "user personas", "user flow", "timeline", "schedule"],
        "Testing": ["unit test", "integration test", "e2e", "test coverage", "pytest", "jest", "mocha",
                   "junit", "testing framework", "test suite", "automated test", "regression",
                   "smoke test", "load test", "performance test", "tdd", "test doc"],
        "DevOps": ["ci/cd", "continuous integration", "github actions", "gitlab ci", "jenkins",
                  "docker", "containerization", "kubernetes", "k8s", "deployment", "aws", "azure",
                  "gcp", "cloud", "terraform", "monitoring", "logging", "nginx", "ssl", "https",
                  "environment", "build pipeline", "automation"],
        "Research": ["research", "analysis", "jupyter", "notebook", "data exploration", "experiment",
                    "hypothesis", "findings", "results", "literature", "benchmark", "survey",
                    "user research", "insights", "statistical", "machine learning", "model evaluation"],
        "Visuals": ["screenshot", "diagram", "flowchart", "chart", "graph", "demo video", "gif",
                   "mockup", "wireframe", "ui preview", "architecture diagram", "sequence diagram",
                   "erd", "class diagram", "infographic", "visualization"],
        "CodeQuality": ["linting", "linter", "eslint", "pylint", "ruff", "flake8", "prettier",
                       "formatting", "black", "autopep8", "type checking", "typescript", "mypy",
                       "code review", "pre-commit", "git hooks", "refactoring", "clean code",
                       "solid", "design patterns", "style guide", "pep 8", "pep8", "docstring",
                       "comments", "static analysis", "sonarqube", "code complexity", "quality",
                       "setup.py", "pyproject.toml", "package.json", "dependency"],
        "Business": ["cost analysis", "budget", "roi", "return on investment", "market research",
                    "market analysis", "customer personas", "business case", "business model",
                    "pricing", "monetization", "competitive analysis", "competitor", "swot",
                    "value proposition", "stakeholder", "revenue", "go-to-market", "risk analysis",
                    "risk assessment", "risk mitigation"],
    }

    for criterion in criteria_graph.keys():
        criterion_lower = criterion.lower()

        # Try to match to a category
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in criterion_lower:
                    criteria_graph[criterion]["category"] = category
                    break
            if criteria_graph[criterion]["category"]:
                break

        # If still no category, mark as uncategorized
        if not criteria_graph[criterion]["category"]:
            criteria_graph[criterion]["category"] = "Uncategorized"

def calculate_weights(total_students):
    """Calculate weights with rarity bonus"""
    for criterion, data in criteria_graph.items():
        prevalence = data["count"] / total_students
        base_weight = prevalence

        # Rarity bonus: criteria with ≤15% prevalence get +1 bonus
        if prevalence <= 0.15:
            bonus = 1.0
            criteria_graph[criterion]["weight"] = base_weight + bonus
            criteria_graph[criterion]["rarity_bonus"] = bonus
        else:
            criteria_graph[criterion]["weight"] = base_weight
            criteria_graph[criterion]["rarity_bonus"] = 0.0

def main():
    print("=" * 80)
    print("ENHANCED STUDENT PROJECT EVALUATOR - WorkSubmissions06")
    print("=" * 80)

    # Find all student folders
    student_folders = [f for f in BASE_DIR.iterdir() if is_student_folder(f)]
    student_folders.sort()
    total_students = len(student_folders)

    print(f"\n[Step 1-2] Found {total_students} student folders\n")

    # Process each student
    print("[Step 3-4] Reading markdown files and extracting criteria...\n")
    for i, student_dir in enumerate(student_folders, 1):
        print(f"[{i}/{total_students}] ", end="")
        process_student(student_dir)

    # Build criteria graph
    print(f"\n[Step 5] Building criteria graph...")
    build_criteria_graph(total_students)

    # Categorize criteria
    print(f"[Step 6] Categorizing criteria...")
    categorize_criteria()

    # Calculate weights
    print(f"[Step 7] Calculating weights with rarity bonus...")
    calculate_weights(total_students)

    # Save results
    output_file = OUTPUT_DIR / "criteria_graph_final.json"
    output_data = {
        "metadata": {
            "total_students": total_students,
            "total_criteria": len(criteria_graph),
            "total_md_files": sum(len(data["md_files"]) for data in student_data.values()),
            "evaluation_date": "2025-12-26",
            "submission_folder": "WorkSubmissions06"
        },
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
                "prevalence": round(data["prevalence"], 3),
                "category": data["category"],
                "weight": round(data["weight"], 3),
                "rarity_bonus": round(data.get("rarity_bonus", 0), 3),
                "sources": dict(data["sources"])
            }
            for criterion, data in criteria_graph.items()
        }
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n[Step 8] Saved criteria graph to {output_file}")

    # Print summary
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Students processed: {total_students}")
    print(f"Total markdown files: {output_data['metadata']['total_md_files']}")
    print(f"Unique criteria discovered: {len(criteria_graph)}")

    # Count by category
    print(f"\nCriteria by category:")
    category_counts = defaultdict(int)
    for criterion, data in criteria_graph.items():
        category_counts[data["category"]] += 1
    for category in sorted(category_counts.keys()):
        print(f"  {category:<20s}: {category_counts[category]:2d} criteria")

    print(f"\nTop 15 most common criteria:")
    sorted_criteria = sorted(criteria_graph.items(), key=lambda x: x[1]["count"], reverse=True)
    for i, (criterion, data) in enumerate(sorted_criteria[:15], 1):
        prevalence = data["prevalence"] * 100
        bonus_str = " [+BONUS]" if data.get("rarity_bonus", 0) > 0 else ""
        print(f"  {i:2d}. {criterion:<45s} {data['category']:<15s} {data['count']:2d}/{total_students} ({prevalence:5.1f}%){bonus_str}")

    print(f"\nRare criteria (<=15% prevalence - receive +1 bonus weight):")
    rare_criteria = [(c, d) for c, d in sorted_criteria if d["prevalence"] <= 0.15]
    print(f"  Found {len(rare_criteria)} rare criteria (out of {len(criteria_graph)} total)")
    for criterion, data in rare_criteria:
        prevalence = data["prevalence"] * 100
        print(f"    - {criterion:<45s} {data['category']:<15s} {data['count']:2d}/{total_students} ({prevalence:5.1f}%)")

    return output_data

if __name__ == "__main__":
    main()
