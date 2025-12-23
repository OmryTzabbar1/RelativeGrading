"""
Smart Criteria Grouping System
Groups technology-specific criteria into general categories for fair comparison.

Example:
- "ESLint" + "Black Formatter" + "Prettier" → "Code Linting"
- "Jest Testing" + "Pytest Framework" → "Unit Testing Framework"
- "React" + "Vue.js" + "Angular" → "Frontend Framework"
"""

import json
from collections import defaultdict

# Define grouping rules: specific → general
GROUPING_RULES = {
    # Testing Frameworks
    "Unit Testing Framework": [
        "Pytest Framework", "Jest Testing", "Mocha", "JUnit",
        "unittest", "Vitest Testing", "Karma"
    ],

    # Code Quality Tools
    "Code Linting": [
        "ESLint", "Black Formatter", "Pylint", "Prettier",
        "Flake8", "Rubocop", "TSLint"
    ],

    # Type Systems (keep Type Safety general, group implementations)
    "Static Type Checking": [
        "TypeScript", "Pydantic Type Safety", "MyPy", "Flow",
        "PropTypes", "Type Safety"  # Include the generic one too
    ],

    # Frontend Frameworks
    "Frontend Framework": [
        "React", "Vue.js", "Angular", "Svelte", "Next.js",
        "Nuxt.js", "Solid.js"
    ],

    # Backend Frameworks
    "Backend Framework": [
        "FastAPI", "Flask", "Django", "Express", "Express.js",
        "NestJS", "Spring Boot", "Ruby on Rails"
    ],

    # Databases
    "Database": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite",
        "MariaDB", "Cassandra", "DynamoDB"
    ],

    # Cloud Deployment
    "Cloud Deployment": [
        "AWS Deployment", "GCP Deployment", "Azure Deployment",
        "Heroku Deployment", "Netlify Deployment", "Vercel Deployment",
        "DigitalOcean", "Railway"
    ],

    # Containerization
    "Containerization": [
        "Docker", "Dockerfile", "Docker Compose", "Podman"
    ],

    # CSS Frameworks
    "CSS Framework": [
        "Tailwind CSS", "Bootstrap", "Material-UI", "Chakra UI",
        "Shadcn UI", "Ant Design", "Bulma"
    ],

    # API Types
    "API Architecture": [
        "REST API", "GraphQL", "gRPC", "WebSocket",
        "REST API Design"
    ],

    # Authentication Methods
    "Authentication": [
        "JWT Authentication", "OAuth", "Session-based Auth",
        "API Keys", "Basic Auth"
    ],

    # State Management (Frontend)
    "State Management": [
        "Redux", "Vuex", "Zustand", "MobX", "Context API",
        "Pinia", "Recoil"
    ],

    # Build Tools
    "Build Tool": [
        "Webpack", "Vite", "Rollup", "Parcel", "esbuild",
        "Turbopack"
    ],

    # Package Managers
    "Package Manager": [
        "npm", "yarn", "pnpm", "pip", "poetry", "conda"
    ],

    # Testing Tools (E2E)
    "E2E Testing Framework": [
        "Playwright", "Cypress", "Selenium", "Puppeteer"
    ],

    # Monitoring/Observability
    "Monitoring": [
        "Prometheus", "Grafana", "New Relic", "Datadog",
        "Sentry", "Metrics Collection"
    ],

    # Message Queues
    "Message Queue": [
        "RabbitMQ", "Kafka", "Redis Queue", "AWS SQS",
        "Google Pub/Sub"
    ],
}

# Criteria that should NOT be grouped (they're already general or functionally different)
KEEP_SEPARATE = [
    # Different types of testing (functionally different)
    "Unit Tests", "Integration Tests", "E2E Tests",

    # Different documentation types (functionally different)
    "README Documentation", "PRD Document", "Architecture Documentation",
    "API Documentation", "User Guide", "Contributing Guide", "Changelog",
    "Deployment Guide", "Testing Documentation",

    # Core features (specific to the project, not tech choices)
    "Chat History", "File Upload", "Image Analysis", "Real-time Streaming",
    "Multi-Session Support", "Dark Theme", "Light Theme", "Theme Switching",
    "Markdown Support", "Code Syntax Highlighting", "Session Management",
    "Responsive Design", "Mobile Support", "Accessibility Features",

    # Security/Compliance (specific standards)
    "OWASP Security", "WCAG Compliance", "Security Features",

    # Architecture patterns (functionally different)
    "Microservices Architecture", "API Gateway", "Load Balancer",
    "Caching Strategy",

    # Performance
    "Performance Benchmarking", "Load Testing",

    # Coverage metrics (specific numbers matter)
    "Test Coverage", "Code Coverage Metrics",

    # Development practices
    "CI/CD Pipeline", "GitHub Actions", "Environment Variables",
    "Environment Validation", "Error Handling", "Input Validation",
    "Logging", "Database Migrations",

    # Research/Analysis
    "Data Analysis", "Mathematical Analysis", "Jupyter Notebooks",

    # Media support
    "PDF Support", "Multimodal Support", "Streaming Responses"
]

def create_reverse_mapping(grouping_rules):
    """Create a reverse map: specific → general"""
    reverse_map = {}
    for general, specifics in grouping_rules.items():
        for specific in specifics:
            reverse_map[specific.lower()] = general
    return reverse_map

def smart_group_criteria(criteria_graph):
    """
    Group specific criteria into general ones while keeping both.

    Returns:
        - grouped_criteria: General criteria with combined student lists
        - specific_to_general: Mapping of which specific criteria contributed to each general
    """
    reverse_map = create_reverse_mapping(GROUPING_RULES)

    # Initialize structures
    grouped_criteria = defaultdict(lambda: {
        'display_name': '',
        'students': set(),
        'count': 0,
        'weight': 0.0,
        'category': None,
        'specific_criteria': set()  # Track which specific criteria contributed
    })

    # Track which specific criteria got grouped
    grouped_specific = set()

    total_students = criteria_graph['metadata']['total_students']

    # Process each criterion
    for crit_key, crit_data in criteria_graph['criteria'].items():
        display_name = crit_data['display_name']

        # Check if this should be grouped
        general_name = reverse_map.get(display_name.lower())

        if general_name:
            # This criterion should be grouped
            grouped_specific.add(display_name)
            general_key = general_name.lower().replace(' ', '_')

            grouped_criteria[general_key]['display_name'] = general_name
            grouped_criteria[general_key]['students'].update(crit_data['students'])
            grouped_criteria[general_key]['category'] = crit_data.get('category', 'Technology')
            grouped_criteria[general_key]['specific_criteria'].add(display_name)
        else:
            # Keep as-is (either in KEEP_SEPARATE or not tech-specific)
            key = crit_key
            grouped_criteria[key] = {
                'display_name': display_name,
                'students': set(crit_data['students']),
                'count': crit_data['count'],
                'weight': crit_data['weight'],
                'category': crit_data.get('category'),
                'specific_criteria': set([display_name])
            }

    # Calculate counts and weights for grouped criteria
    for key, data in grouped_criteria.items():
        data['students'] = list(data['students'])
        data['count'] = len(data['students'])
        data['weight'] = data['count'] / total_students
        data['specific_criteria'] = list(data['specific_criteria'])

    return dict(grouped_criteria), grouped_specific

def main():
    # Load original criteria graph
    print("Loading original criteria graph...")
    with open('outputs/criteria_graph_final.json', 'r') as f:
        original = json.load(f)

    print(f"Original: {original['metadata']['total_criteria']} criteria")

    # Apply smart grouping
    print("\nApplying smart grouping...")
    grouped_criteria, grouped_specific = smart_group_criteria(original)

    # Create new criteria graph
    new_graph = {
        'metadata': {
            'total_students': original['metadata']['total_students'],
            'total_criteria': len(grouped_criteria),
            'original_criteria': original['metadata']['total_criteria'],
            'grouped_specific_criteria': len(grouped_specific),
            'evaluation_date': original['metadata']['evaluation_date'],
            'grouping_applied': True
        },
        'criteria': grouped_criteria
    }

    # Save grouped version
    with open('outputs/criteria_graph_grouped.json', 'w', encoding='utf-8') as f:
        json.dump(new_graph, f, indent=2)

    print(f"\nGrouped: {new_graph['metadata']['total_criteria']} criteria")
    print(f"Grouped {len(grouped_specific)} specific criteria into general ones")

    # Show what was grouped
    print("\n" + "="*80)
    print("GROUPING SUMMARY")
    print("="*80)

    # Find grouped criteria and show examples
    for general_key, general_data in sorted(grouped_criteria.items(),
                                            key=lambda x: len(x[1]['specific_criteria']),
                                            reverse=True):
        specifics = general_data['specific_criteria']
        if len(specifics) > 1:  # Only show if multiple were grouped
            print(f"\n{general_data['display_name']} ({general_data['count']} students):")
            print(f"  ← Grouped from: {', '.join(sorted(specifics))}")

    print("\n" + "="*80)
    print(f"\nSaved to: outputs/criteria_graph_grouped.json")

    # Show impact on specific students
    print("\n" + "="*80)
    print("IMPACT ANALYSIS")
    print("="*80)

    # Compare student criterion counts
    student_counts_before = defaultdict(int)
    student_counts_after = defaultdict(int)

    for crit_data in original['criteria'].values():
        for student in crit_data['students']:
            student_counts_before[student] += 1

    for crit_data in grouped_criteria.values():
        for student in crit_data['students']:
            student_counts_after[student] += 1

    # Show students with biggest changes
    changes = []
    for student in student_counts_before:
        before = student_counts_before[student]
        after = student_counts_after[student]
        if before != after:
            changes.append((student, before, after, after - before))

    changes.sort(key=lambda x: abs(x[3]), reverse=True)

    print("\nTop 10 students most affected by grouping:")
    print(f"{'Student':<10} {'Before':<8} {'After':<8} {'Change':<8}")
    print("-"*40)
    for student, before, after, change in changes[:10]:
        sign = '+' if change > 0 else ''
        print(f"{student:<10} {before:<8} {after:<8} {sign}{change:<8}")

if __name__ == '__main__':
    main()
