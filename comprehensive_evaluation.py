"""
Comprehensive Student Project Evaluator
Implements all improved EXTRACTION.md rules including:
- Filename-based detection
- Section header detection
- Liberal pattern matching
- Case-insensitive matching
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# Filename-based criteria detection
FILENAME_CRITERIA = {
    r'prd\.md$|productrequ': 'PRD Document',
    r'testing\.md$|test\.md$': 'Testing Documentation',
    r'contributing\.md$': 'Contributing Guide',
    r'quickstart\.md$|quick.?start': 'Quick Start Guide',
    r'architecture\.md$|design\.md$': 'Architecture Documentation',
    r'changelog\.md$|changes\.md$': 'Changelog',
    r'api\.md$|api.?docs': 'API Documentation',
    r'roadmap\.md$': 'Roadmap',
    r'deployment\.md$|deploy\.md$': 'Deployment Guide',
    r'troubleshooting\.md$|faq\.md$': 'Troubleshooting Guide',
    r'readme\.md$': 'README',
}

# Positive indicator patterns (case-insensitive)
POSITIVE_PATTERNS = [
    (r'(?:we |project |this )?(?:built|created|developed|implemented)', 'implementation'),
    (r'(?:includes?|contains?|has|comes with|features?|provides?|offers?|enables?)', 'feature'),
    (r'(?:comprehensive|complete|full|thorough)', 'comprehensive'),
    (r'(?:unit tests?|testing|test suite)', 'Unit Tests'),
    (r'(?:integration tests?)', 'Integration Tests'),
    (r'(?:e2e|end.?to.?end) tests?', 'E2E Tests'),
    (r'(?:test coverage|code coverage|~?\d+%\s*coverage)', 'Test Coverage Metrics'),
    (r'total tests?:\s*~?\d+', 'Unit Tests'),
    (r'(?:ci/cd|continuous integration|github actions)', 'CI/CD Pipeline'),
    (r'docker(?:file|ized|\.)', 'Docker'),
    (r'(?:screenshot|image|demo|diagram)', 'visual'),
]

# Negative patterns (invalidate)
NEGATIVE_PATTERNS = [
    r'todo:',
    r'fixme:',
    r'not yet',
    r'not complete',
    r'out of scope',
    r'future work',
    r'planned for',
    r'will add',
    r'stretch goal',
]

def extract_student_id(folder_name):
    """Extract student ID from Participant_XXXXX_assignsubmission_file"""
    match = re.search(r'Participant_(\d+)_', folder_name)
    return match.group(1) if match else folder_name

def find_all_md_files(student_folder):
    """Recursively find all .md files"""
    md_files = []
    for root, dirs, files in os.walk(student_folder):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def detect_criteria_from_filename(filepath):
    """Detect criteria based on filename alone"""
    filename = os.path.basename(filepath).lower()
    criteria = []

    for pattern, criterion in FILENAME_CRITERIA.items():
        if re.search(pattern, filename, re.IGNORECASE):
            criteria.append(criterion)

    return criteria

def extract_criteria_from_content(content):
    """Extract criteria from markdown content"""
    criteria = []
    content_lower = content.lower()

    # Check for negative patterns first
    has_negative = any(re.search(pattern, content_lower) for pattern in NEGATIVE_PATTERNS)

    if not has_negative:
        # Check positive patterns
        for pattern, criterion_type in POSITIVE_PATTERNS:
            if re.search(pattern, content_lower):
                if criterion_type == 'Unit Tests':
                    criteria.append('Unit Tests')
                elif criterion_type == 'Integration Tests':
                    criteria.append('Integration Tests')
                elif criterion_type == 'E2E Tests':
                    criteria.append('E2E Tests')
                elif criterion_type == 'Test Coverage Metrics':
                    criteria.append('Test Coverage Metrics')
                elif criterion_type == 'CI/CD Pipeline':
                    criteria.append('CI/CD Pipeline')
                elif criterion_type == 'Docker':
                    criteria.append('Docker')

    # Check for section headers
    sections = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE | re.IGNORECASE)
    for section in sections:
        section_lower = section.lower()
        if 'test' in section_lower:
            criteria.append('Testing Documentation')
        if 'install' in section_lower or 'setup' in section_lower or 'getting started' in section_lower:
            criteria.append('Installation Instructions')
        if 'usage' in section_lower or 'how to use' in section_lower:
            criteria.append('Usage Guide')
        if 'feature' in section_lower:
            criteria.append('Features Documentation')
        if 'screenshot' in section_lower or 'demo' in section_lower:
            criteria.append('Screenshots')
        if 'architecture' in section_lower or 'design' in section_lower:
            criteria.append('Architecture Documentation')
        if 'api' in section_lower or 'endpoint' in section_lower:
            criteria.append('API Documentation')
        if 'contribut' in section_lower:
            criteria.append('Contributing Guide')

    # Look for file references in markdown links
    file_refs = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content, re.IGNORECASE)
    for _, filepath in file_refs:
        filename_lower = filepath.lower()
        if 'prd' in filename_lower:
            criteria.append('PRD Document')
        if 'test' in filename_lower:
            criteria.append('Testing Documentation')
        if 'contribut' in filename_lower:
            criteria.append('Contributing Guide')
        if 'quickstart' in filename_lower:
            criteria.append('Quick Start Guide')
        if 'architecture' in filename_lower:
            criteria.append('Architecture Documentation')

    return list(set(criteria))  # Remove duplicates

def evaluate_student(student_folder, student_id):
    """Evaluate a single student"""
    print(f"  Evaluating {student_id}...", end='')

    # Find all markdown files
    md_files = find_all_md_files(student_folder)

    all_criteria = set()

    # Filename-based detection
    for md_file in md_files:
        file_criteria = detect_criteria_from_filename(md_file)
        all_criteria.update(file_criteria)

    # Content-based detection
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                content_criteria = extract_criteria_from_content(content)
                all_criteria.update(content_criteria)
        except Exception as e:
            print(f"\n    Warning: Could not read {md_file}: {e}")
            continue

    print(f" {len(md_files)} files, {len(all_criteria)} criteria")
    return list(all_criteria)

def normalize_criterion_name(name):
    """Normalize criterion names for consistency"""
    # Convert to lowercase for keying
    key = name.lower().replace(' ', '_').replace('-', '_')
    return key, name

def main():
    master_folder = 'tests/WorkSubmissions01'

    print("[Step 2/9] Discovering students...")
    student_folders = [f for f in os.listdir(master_folder) if f.startswith('Participant_')]
    total_students = len(student_folders)
    print(f"Found {total_students} student folders\n")

    print("[Step 3-4/9] Reading markdown files and extracting criteria...")

    # Build criteria graph
    criteria_graph = defaultdict(lambda: {
        'display_name': '',
        'students': [],
        'count': 0,
        'weight': 0.0,
        'category': None
    })

    student_criteria_map = {}

    for idx, student_folder_name in enumerate(sorted(student_folders), 1):
        student_id = extract_student_id(student_folder_name)
        student_path = os.path.join(master_folder, student_folder_name)

        criteria_list = evaluate_student(student_path, student_id)
        student_criteria_map[student_id] = criteria_list

        # Add to criteria graph
        for criterion in criteria_list:
            key, display_name = normalize_criterion_name(criterion)
            criteria_graph[key]['display_name'] = display_name
            criteria_graph[key]['students'].append(student_id)
            criteria_graph[key]['count'] += 1

    print(f"\n[Step 5/9] Building criteria graph...")
    print(f"Total unique criteria discovered: {len(criteria_graph)}")

    # Calculate weights
    print(f"[Step 7/9] Calculating weights...")
    for key, data in criteria_graph.items():
        data['weight'] = data['count'] / total_students

    # Save output
    output = {
        'metadata': {
            'generated_at': '2025-12-23T00:00:00Z',
            'total_students': total_students,
            'total_criteria': len(criteria_graph),
            'master_folder': master_folder,
        },
        'criteria': dict(criteria_graph)
    }

    os.makedirs('outputs', exist_ok=True)
    with open('outputs/criteria_graph_v2.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved: outputs/criteria_graph_v2.json")

    # Show comparison for student 38986
    if '38986' in student_criteria_map:
        print(f"\n📊 Student 38986 Results:")
        print(f"   Previous: 2 criteria (README, Installation Instructions)")
        print(f"   New: {len(student_criteria_map['38986'])} criteria")
        print(f"   Criteria found: {', '.join(sorted(student_criteria_map['38986']))}")

if __name__ == '__main__':
    main()
