"""
Granular Student Project Evaluator
Extracts SPECIFIC criteria, not broad categories.

Examples of granular criteria:
- "31 unit tests" (not just "Unit Tests")
- "80% code coverage" (not just "Test Coverage")
- "Docker Compose support" (not just "Docker")
- "Charts.js integration" (not just "visualization")
- "WCAG 2.1 compliance" (not just "accessibility")
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

def normalize_criterion(text):
    """Normalize a criterion name"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Create key for deduplication
    key = text.lower().replace(' ', '_').replace('-', '_')
    key = re.sub(r'[^a-z0-9_]', '', key)
    return key, text

def extract_specific_features(content):
    """Extract specific, granular features from markdown content"""
    criteria = set()

    # Extract bulleted feature lists
    # Match patterns like:
    # - Feature name
    # * Feature name
    # + Feature name
    feature_bullets = re.findall(r'^[*\-+]\s+(?:\*\*)?([^*\n]+?)(?:\*\*)?(?:\s*-\s*|$)', content, re.MULTILINE)
    for feature in feature_bullets:
        feature = feature.strip()
        # Skip if too short or looks like a sentence
        if len(feature) > 10 and len(feature) < 100 and not feature.endswith('.'):
            criteria.add(feature)

    # Extract specific technologies/tools mentioned
    tech_patterns = [
        r'\b(Docker(?:\s+Compose)?)\b',
        r'\b(Kubernetes|K8s)\b',
        r'\b(AWS|GCP|Azure|Heroku)\b',
        r'\b(FastAPI|Flask|Django|Express)\b',
        r'\b(React|Vue|Angular|Svelte)\b',
        r'\b(PostgreSQL|MySQL|MongoDB|Redis)\b',
        r'\b(pytest|unittest|Jest|Mocha)\b',
        r'\b(GitHub Actions|Travis|CircleCI)\b',
        r'\b(Swagger|ReDoc|OpenAPI)\b',
        r'\b(Charts\.js|D3\.js|Plotly)\b',
        r'\b(TypeScript|Python|JavaScript|Go|Rust)\b',
    ]

    for pattern in tech_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if match:
                criteria.add(f"{match} integration")

    # Extract specific metrics
    metric_patterns = [
        (r'(\d+)\s*(?:unit\s*)?tests?(?:\s+passing)?', lambda m: f"{m.group(1)} tests"),
        (r'(\d+)%\s*(?:code\s*)?coverage', lambda m: f"{m.group(1)}% code coverage"),
        (r'(\d+)\s*(?:documentation|doc)\s*files?', lambda m: f"{m.group(1)} documentation files"),
        (r'(\d+)\+?\s*features?', lambda m: f"{m.group(1)}+ features"),
    ]

    for pattern, formatter in metric_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            criteria.add(formatter(match))

    # Extract compliance/standards
    compliance_patterns = [
        r'(WCAG\s+[\d.]+)',
        r'(OWASP\s+Top\s+\d+)',
        r'(ISO\s+[\d-]+)',
        r'(GDPR)\s+complian',
    ]

    for pattern in compliance_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            criteria.add(f"{match} compliance")

    # Extract specific documentation types from headings
    doc_headings = re.findall(r'^#{1,3}\s+(.+?)$', content, re.MULTILINE)
    for heading in doc_headings:
        heading = heading.strip()
        # Look for specific doc types
        doc_keywords = [
            'PRD', 'Product Requirements', 'Architecture', 'Design Document',
            'API Documentation', 'Deployment', 'Contributing', 'Changelog',
            'Security', 'Test Report', 'Accessibility', 'Code of Conduct',
            'Research', 'Analysis', 'Mathematical', 'Grading', 'Submission'
        ]
        for keyword in doc_keywords:
            if keyword.lower() in heading.lower():
                criteria.add(heading)
                break

    # Extract version features (v1, v2, v3)
    version_features = re.findall(r'(?:v\d+|version\s+\d+)[:\s]+(.+?)(?:\n|$)', content, re.IGNORECASE)
    for feature in version_features:
        if len(feature) > 5 and len(feature) < 80:
            criteria.add(feature.strip())

    return criteria

def extract_from_filename(filepath):
    """Extract criteria from filename"""
    filename = os.path.basename(filepath).lower()
    criteria = set()

    # Specific document types
    if 'prd' in filename or 'product_req' in filename:
        criteria.add('PRD Document')
    if 'architecture' in filename or 'design' in filename:
        criteria.add('Architecture Documentation')
    if 'test' in filename:
        criteria.add('Testing Documentation')
    if 'deployment' in filename or 'deploy' in filename:
        criteria.add('Deployment Guide')
    if 'contributing' in filename:
        criteria.add('Contributing Guide')
    if 'changelog' in filename or 'changes' in filename:
        criteria.add('Changelog')
    if 'security' in filename:
        criteria.add('Security Policy')
    if 'code_of_conduct' in filename or 'codeofconduct' in filename:
        criteria.add('Code of Conduct')
    if 'api' in filename and 'doc' in filename:
        criteria.add('API Documentation')
    if 'research' in filename or 'analysis' in filename:
        criteria.add('Research & Analysis')
    if 'quickstart' in filename or 'quick_start' in filename:
        criteria.add('Quick Start Guide')
    if 'mathematical' in filename or 'math' in filename:
        criteria.add('Mathematical Analysis')
    if 'accessibility' in filename:
        criteria.add('Accessibility Audit')
    if 'grading' in filename:
        criteria.add('Grading Report')
    if 'submission' in filename:
        criteria.add('Submission Checklist')

    return criteria

def evaluate_student(student_folder, student_id):
    """Evaluate a single student with granular criteria extraction"""
    print(f"  Evaluating {student_id}...", end='', flush=True)

    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk(student_folder):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(os.path.join(root, file))

    all_criteria = set()

    # Process each file
    for md_file in md_files:
        # Filename-based detection
        all_criteria.update(extract_from_filename(md_file))

        # Content-based extraction
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Extract granular features
                specific_features = extract_specific_features(content)
                all_criteria.update(specific_features)

        except Exception as e:
            continue

    print(f" {len(md_files)} files, {len(all_criteria)} criteria")
    return list(all_criteria)

def main():
    master_folder = 'tests/WorkSubmissions01'

    print("[Step 2/9] Discovering students...")
    student_folders = [f for f in os.listdir(master_folder) if f.startswith('Participant_')]
    total_students = len(student_folders)
    print(f"Found {total_students} student folders\n")

    print("[Step 3-4/9] Extracting GRANULAR criteria...")

    # Build criteria graph
    criteria_graph = defaultdict(lambda: {
        'display_name': '',
        'students': [],
        'count': 0,
        'weight': 0.0,
        'category': None
    })

    student_criteria_map = {}

    for student_folder_name in sorted(student_folders):
        student_id = re.search(r'Participant_(\d+)_', student_folder_name).group(1)
        student_path = os.path.join(master_folder, student_folder_name)

        criteria_list = evaluate_student(student_path, student_id)
        student_criteria_map[student_id] = criteria_list

        # Add to criteria graph
        for criterion in criteria_list:
            key, display_name = normalize_criterion(criterion)
            if key:  # Skip empty keys
                criteria_graph[key]['display_name'] = display_name
                if student_id not in criteria_graph[key]['students']:
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
    with open('outputs/criteria_graph_granular.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved: outputs/criteria_graph_granular.json")

    # Show sample for student 38970 and 38986
    for student in ['38970', '38986']:
        if student in student_criteria_map:
            print(f"\nStudent {student}: {len(student_criteria_map[student])} criteria")
            print(f"Sample criteria: {', '.join(sorted(student_criteria_map[student])[:10])}...")

if __name__ == '__main__':
    main()
