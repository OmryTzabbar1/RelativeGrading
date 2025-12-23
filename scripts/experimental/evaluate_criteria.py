#!/usr/bin/env python3
"""
Student Project Evaluator - Criteria Discovery Script
Analyzes markdown documentation to discover and categorize implemented criteria.
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Base directory
BASE_DIR = Path("E:/Projects/student-project-evaluator/tests/WorkSubmissions01")
OUTPUT_DIR = Path("E:/Projects/student-project-evaluator/outputs")

# Negative patterns - things to exclude
NEGATIVE_PATTERNS = [
    r'\btodo\b',
    r'\bwill implement\b',
    r'\bfuture work\b',
    r'\bplanned\b',
    r'\bnot yet\b',
    r'\bcoming soon\b',
    r'\bout of scope\b',
    r'\bto be implemented\b',
    r'\bin progress\b',
    r'\bnot complete\b',
]

# Criteria patterns to detect (pattern, category, key, display_name)
CRITERIA_PATTERNS = [
    # Documentation
    (r'\bREADME\b', 'Documentation', 'readme', 'README Documentation'),
    (r'\bPRD\b|Product Requirements Document', 'Documentation', 'prd', 'PRD Document'),
    (r'\barchitecture\s+(?:document|diagram|doc)', 'Documentation', 'architecture_doc', 'Architecture Documentation'),
    (r'\bAPI\s+documentation\b', 'Documentation', 'api_docs', 'API Documentation'),
    (r'\bcontributing\s+guide\b', 'Documentation', 'contributing_guide', 'Contributing Guide'),
    (r'\bchangelog\b', 'Documentation', 'changelog', 'Changelog'),
    (r'\buser\s+guide\b|user\s+manual', 'Documentation', 'user_guide', 'User Guide'),
    (r'\bdeployment\s+guide\b', 'Documentation', 'deployment_guide', 'Deployment Guide'),

    # Testing
    (r'\bunit\s+test', 'Testing', 'unit_tests', 'Unit Tests'),
    (r'\bintegration\s+test', 'Testing', 'integration_tests', 'Integration Tests'),
    (r'\be2e\s+test|end-to-end\s+test', 'Testing', 'e2e_tests', 'E2E Tests'),
    (r'\btest\s+coverage\b', 'Testing', 'test_coverage', 'Test Coverage'),
    (r'(\d+)%\s+(?:code\s+)?coverage', 'Testing', 'coverage_metric', 'Code Coverage Metrics'),
    (r'\bpytest\b', 'Testing', 'pytest', 'Pytest Framework'),
    (r'\bjest\b', 'Testing', 'jest', 'Jest Testing'),
    (r'\bvitest\b', 'Testing', 'vitest', 'Vitest Testing'),
    (r'\btest\s+automation\b', 'Testing', 'test_automation', 'Test Automation'),
    (r'\bmocking\b', 'Testing', 'mocking', 'Test Mocking'),

    # Features - Chat/AI
    (r'\bchat\s+history\b', 'Features', 'chat_history', 'Chat History'),
    (r'\bchat\s+persistence\b', 'Features', 'chat_persistence', 'Chat History Persistence'),
    (r'\breal-?time\s+streaming\b', 'Features', 'realtime_streaming', 'Real-time Streaming'),
    (r'\bstreaming\s+response', 'Features', 'streaming_responses', 'Streaming Responses'),
    (r'\bmulti-?session\b', 'Features', 'multi_session', 'Multi-Session Support'),
    (r'\bsession\s+management\b', 'Features', 'session_management', 'Session Management'),
    (r'\bfile\s+upload\b', 'Features', 'file_upload', 'File Upload'),
    (r'\bimage\s+analysis\b', 'Features', 'image_analysis', 'Image Analysis'),
    (r'\bPDF\s+(?:support|upload|processing)', 'Features', 'pdf_support', 'PDF Support'),
    (r'\bmulti-?modal\b', 'Features', 'multimodal', 'Multimodal Support'),

    # UI/UX Features
    (r'\bdark\s+(?:mode|theme)\b', 'Features', 'dark_theme', 'Dark Theme'),
    (r'\blight\s+(?:mode|theme)\b', 'Features', 'light_theme', 'Light Theme'),
    (r'\btheme\s+(?:switching|toggle)\b', 'Features', 'theme_switching', 'Theme Switching'),
    (r'\bresponsive\s+design\b', 'Features', 'responsive_design', 'Responsive Design'),
    (r'\bmobile\s+(?:support|friendly|responsive)', 'Features', 'mobile_support', 'Mobile Support'),
    (r'\baccessibility\b', 'Features', 'accessibility', 'Accessibility Features'),
    (r'\bWCAG\b', 'Features', 'wcag_compliance', 'WCAG Compliance'),
    (r'\bmarkdown\s+(?:support|rendering)', 'Features', 'markdown_support', 'Markdown Support'),
    (r'\bcode\s+syntax\s+highlighting\b', 'Features', 'syntax_highlighting', 'Code Syntax Highlighting'),

    # DevOps
    (r'\bDocker\b(?!.*(?:todo|plan))', 'DevOps', 'docker', 'Docker'),
    (r'\bDockerfile\b', 'DevOps', 'dockerfile', 'Dockerfile'),
    (r'\bDocker\s+Compose\b', 'DevOps', 'docker_compose', 'Docker Compose'),
    (r'\bKubernetes\b', 'DevOps', 'kubernetes', 'Kubernetes'),
    (r'\bCI/CD\b', 'DevOps', 'cicd', 'CI/CD Pipeline'),
    (r'\bGitHub\s+Actions\b', 'DevOps', 'github_actions', 'GitHub Actions'),
    (r'\bAWS\b', 'DevOps', 'aws', 'AWS Deployment'),
    (r'\bGCP\b|Google\s+Cloud', 'DevOps', 'gcp', 'GCP Deployment'),
    (r'\bHeroku\b', 'DevOps', 'heroku', 'Heroku Deployment'),
    (r'\bVercel\b', 'DevOps', 'vercel', 'Vercel Deployment'),
    (r'\bNetlify\b', 'DevOps', 'netlify', 'Netlify Deployment'),
    (r'\benvironment\s+variables\b', 'DevOps', 'env_vars', 'Environment Variables'),

    # Code Quality
    (r'\bTypeScript\b', 'Code Quality', 'typescript', 'TypeScript'),
    (r'\bPydantic\b', 'Code Quality', 'pydantic', 'Pydantic Type Safety'),
    (r'\btype\s+(?:safety|checking|hints)\b', 'Code Quality', 'type_safety', 'Type Safety'),
    (r'\bESLint\b', 'Code Quality', 'eslint', 'ESLint'),
    (r'\bPrettier\b', 'Code Quality', 'prettier', 'Prettier'),
    (r'\bBlack\b.*formatter', 'Code Quality', 'black', 'Black Formatter'),
    (r'\berror\s+handling\b', 'Code Quality', 'error_handling', 'Error Handling'),
    (r'\blogging\b', 'Code Quality', 'logging', 'Logging'),
    (r'\bsecurity\b.*(?:implementation|features)', 'Code Quality', 'security', 'Security Features'),
    (r'\bOWASP\b', 'Code Quality', 'owasp', 'OWASP Security'),
    (r'\binput\s+validation\b', 'Code Quality', 'input_validation', 'Input Validation'),
    (r'\benvironment\s+(?:validation|config)', 'Code Quality', 'env_validation', 'Environment Validation'),

    # Research/Analysis
    (r'\bmathematical\s+analysis\b', 'Research', 'math_analysis', 'Mathematical Analysis'),
    (r'\bdata\s+analysis\b', 'Research', 'data_analysis', 'Data Analysis'),
    (r'\bJupyter\s+(?:notebook|notebooks)\b', 'Research', 'jupyter', 'Jupyter Notebooks'),
    (r'\bperformance\s+(?:benchmark|analysis)\b', 'Research', 'performance_benchmark', 'Performance Benchmarking'),
    (r'\bload\s+testing\b', 'Research', 'load_testing', 'Load Testing'),
    (r'\bmetrics\b.*(?:collection|tracking)', 'Research', 'metrics', 'Metrics Collection'),

    # Database
    (r'\bPostgreSQL\b', 'Database', 'postgresql', 'PostgreSQL'),
    (r'\bMongoDB\b', 'Database', 'mongodb', 'MongoDB'),
    (r'\bRedis\b', 'Database', 'redis', 'Redis'),
    (r'\bSQLite\b', 'Database', 'sqlite', 'SQLite'),
    (r'\bPrisma\b', 'Database', 'prisma', 'Prisma ORM'),
    (r'\bdatabase\s+migration', 'Database', 'db_migrations', 'Database Migrations'),

    # Architecture
    (r'\bREST\s+API\b', 'Architecture', 'rest_api', 'REST API'),
    (r'\bWebSocket', 'Architecture', 'websocket', 'WebSocket'),
    (r'\bmicroservices\b', 'Architecture', 'microservices', 'Microservices Architecture'),
    (r'\bAPI\s+gateway\b', 'Architecture', 'api_gateway', 'API Gateway'),
    (r'\bload\s+balancer\b', 'Architecture', 'load_balancer', 'Load Balancer'),
    (r'\bcaching\s+(?:strategy|layer)\b', 'Architecture', 'caching', 'Caching Strategy'),

    # Frontend Frameworks
    (r'\bReact\b', 'Frontend', 'react', 'React'),
    (r'\bNext\.js\b', 'Frontend', 'nextjs', 'Next.js'),
    (r'\bVue\b', 'Frontend', 'vue', 'Vue.js'),
    (r'\bSvelte\b', 'Frontend', 'svelte', 'Svelte'),
    (r'\bTailwind\s+CSS\b', 'Frontend', 'tailwind', 'Tailwind CSS'),
    (r'\bShadcn\b', 'Frontend', 'shadcn', 'Shadcn UI'),

    # Backend Frameworks
    (r'\bFastAPI\b', 'Backend', 'fastapi', 'FastAPI'),
    (r'\bExpress\b', 'Backend', 'express', 'Express.js'),
    (r'\bFlask\b', 'Backend', 'flask', 'Flask'),
    (r'\bDjango\b', 'Backend', 'django', 'Django'),
]


def is_negative_context(text: str, match_pos: Tuple[int, int]) -> bool:
    """Check if a match appears in a negative context (TODO, planned, etc.)"""
    # Get surrounding context (200 chars before and after)
    start = max(0, match_pos[0] - 200)
    end = min(len(text), match_pos[1] + 200)
    context = text[start:end].lower()

    for pattern in NEGATIVE_PATTERNS:
        if re.search(pattern, context, re.IGNORECASE):
            return True
    return False


def extract_criteria_from_text(text: str, student_id: str) -> Set[str]:
    """Extract criteria keys from markdown text"""
    criteria = set()

    for pattern, category, key, display_name in CRITERIA_PATTERNS:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in matches:
            # Check if this is in a negative context
            if not is_negative_context(text, match.span()):
                criteria.add(key)

    return criteria


def analyze_student(student_dir: Path) -> Tuple[str, Set[str]]:
    """Analyze all markdown files for a single student"""
    student_id = student_dir.name.split('_')[1]
    all_criteria = set()

    # Find all .md files
    md_files = list(student_dir.rglob("*.md"))

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                criteria = extract_criteria_from_text(content, student_id)
                all_criteria.update(criteria)
        except Exception as e:
            print(f"Error reading {md_file}: {e}")

    return student_id, all_criteria


def build_criteria_graph(student_criteria: Dict[str, Set[str]]) -> Dict:
    """Build the final criteria graph with metadata"""

    # Create reverse mapping: criterion -> students who have it
    criterion_to_students = defaultdict(list)
    for student_id, criteria in student_criteria.items():
        for criterion in criteria:
            criterion_to_students[criterion].append(student_id)

    # Build the output structure
    total_students = len(student_criteria)
    criteria_dict = {}

    # Create a mapping of keys to their metadata
    key_to_metadata = {}
    for pattern, category, key, display_name in CRITERIA_PATTERNS:
        key_to_metadata[key] = {
            'category': category,
            'display_name': display_name
        }

    for criterion_key, students in criterion_to_students.items():
        count = len(students)
        weight = count / total_students

        metadata = key_to_metadata.get(criterion_key, {
            'category': 'Other',
            'display_name': criterion_key.replace('_', ' ').title()
        })

        criteria_dict[criterion_key] = {
            'display_name': metadata['display_name'],
            'students': sorted(students),
            'count': count,
            'weight': round(weight, 3),
            'category': metadata['category']
        }

    # Sort by count (most common first)
    criteria_dict = dict(sorted(criteria_dict.items(),
                                key=lambda x: x[1]['count'],
                                reverse=True))

    return {
        'metadata': {
            'total_students': total_students,
            'total_criteria': len(criteria_dict),
            'evaluation_date': '2025-12-23'
        },
        'criteria': criteria_dict
    }


def main():
    """Main evaluation function"""
    print("Starting student project evaluation...")
    print(f"Base directory: {BASE_DIR}")

    # Get all student directories
    student_dirs = sorted([d for d in BASE_DIR.iterdir()
                          if d.is_dir() and d.name.startswith('Participant_')])

    print(f"Found {len(student_dirs)} students")

    # Analyze each student
    student_criteria = {}
    for i, student_dir in enumerate(student_dirs, 1):
        student_id, criteria = analyze_student(student_dir)
        student_criteria[student_id] = criteria
        print(f"[{i}/{len(student_dirs)}] Student {student_id}: {len(criteria)} criteria found")

    # Build criteria graph
    print("\nBuilding criteria graph...")
    criteria_graph = build_criteria_graph(student_criteria)

    print(f"\nTotal unique criteria discovered: {criteria_graph['metadata']['total_criteria']}")

    # Print top 20 most common criteria
    print("\nTop 20 most common criteria:")
    for i, (key, data) in enumerate(list(criteria_graph['criteria'].items())[:20], 1):
        print(f"{i:2d}. {data['display_name']:40s} - {data['count']:2d} students ({data['weight']:.1%})")

    # Save to file
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "criteria_graph_final.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(criteria_graph, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {output_file}")

    # Print category summary
    category_counts = defaultdict(int)
    for data in criteria_graph['criteria'].values():
        category_counts[data['category']] += 1

    print("\nCriteria by category:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:20s}: {count:2d} criteria")


if __name__ == "__main__":
    main()
