# Architecture and Technical Planning
# Student Project Evaluator - Markdown Criteria Discovery v3.0

**Version:** 3.0
**Date:** 2025-12-17
**Status:** Active

---

## 1. System Architecture

### 1.1 Overview

The Student Project Evaluator v3.0 uses a **Markdown-Based Criteria Discovery** architecture:

- **Single-pass analysis**: Read markdown files once, extract criteria AND track students
- **Claude as agent**: Claude reads, understands context, and extracts criteria
- **Prevalence weighting**: More students have it = higher weight
- **Relative grading**: Best student = 100, others scaled

### 1.2 High-Level Architecture

```
User Input → Discovery Phase → Categorization → Weighting → Grading → Outputs
    ↓              ↓                ↓              ↓           ↓          ↓
Master Folder   Read .md files   Group into     Calculate   Compute    CSV
                Extract criteria  categories    prevalence   grades     Report
                Track students    Flag unknown   weights      ranks      YAML
                Build graph
```

### 1.3 Core Principles

1. **Markdown-First**: Only read .md files - they provide holistic project summaries
2. **Context-Aware**: Validate that criteria are actually implemented, not just mentioned
3. **Single-Pass**: Build criteria graph in one iteration, no re-evaluation needed
4. **Prevalence Weights**: Common criteria are critical; rare criteria are bonuses
5. **Claude-Powered**: Leverage Claude's understanding for extraction and validation

---

## 2. Detailed Architecture

### 2.1 Phase 1: Discovery (Single-Pass)

**Input**: Master folder containing student project folders

**Process**:
```
criteria_graph = {}  # {criterion: {students: [], category: None}}

for student_folder in master_folder:
    student_name = get_folder_name(student_folder)
    md_files = find_all_md_files(student_folder)

    for md_file in md_files:
        content = read_file(md_file)
        extracted = claude_extract_criteria(content)

        for criterion in extracted:
            if is_valid_context(criterion):  # Not "TODO", "not implemented"
                if criterion not in criteria_graph:
                    criteria_graph[criterion] = {students: [], category: None}
                criteria_graph[criterion].students.append(student_name)

save_criteria_graph(criteria_graph)
```

**Output**: `criteria_graph.json` with all criteria and their students

### 2.2 Phase 2: Categorization

**Input**: Raw criteria graph

**Process**:
```
categories = {
    "Documentation": ["README", "API docs", "user guide", ...],
    "Testing": ["unit tests", "integration tests", "E2E", ...],
    "DevOps": ["CI/CD", "Docker", "deployment", ...],
    "Planning": ["PRD", "architecture", "design", ...],
    "Research": ["analysis", "findings", "notebooks", ...],
    "Visuals": ["screenshots", "diagrams", "charts", ...],
    "Code Quality": ["linting", "type checking", ...],
    "Business": ["cost analysis", "ROI", "market research", ...]
}

flagged_criteria = []

for criterion in criteria_graph:
    matched_category = match_to_category(criterion, categories)

    if matched_category:
        criteria_graph[criterion].category = matched_category
    else:
        flagged_criteria.append(criterion)

save_flagged_criteria(flagged_criteria)
```

**Output**:
- Updated `criteria_graph.json` with categories
- `flagged_criteria.md` for manual review

### 2.3 Phase 3: Weighting

**Input**: Categorized criteria graph, total student count

**Process**:
```
total_students = count(all_students)

for criterion in criteria_graph:
    if criterion.category is not None:  # Only valid criteria
        student_count = len(criterion.students)
        criterion.weight = student_count / total_students
```

**Output**: Criteria graph with weights

### 2.4 Phase 4: Grading

**Input**: Weighted criteria graph

**Process**:
```
student_scores = {}

# Calculate max possible score
max_possible = sum(criterion.weight for criterion in valid_criteria)

# Score each student
for student in all_students:
    score = 0
    for criterion in valid_criteria:
        if student in criterion.students:
            score += criterion.weight

    percentage = (score / max_possible) * 100
    student_scores[student] = {score, percentage}

# Find best and assign relative grades
best_percentage = max(s.percentage for s in student_scores)

for student in student_scores:
    if student.percentage == best_percentage:
        student.grade = 100
    else:
        student.grade = (student.percentage / best_percentage) * 100

    # Assign rank based on grade
    student.rank = calculate_rank(student.grade)
```

**Output**:
- `grades.csv`
- `evaluation_report.md`

---

## 3. Claude Agent Design

### 3.1 Skill Structure

The evaluation is implemented as a Claude Code skill (`SKILL.md`):

```markdown
---
name: student-project-evaluator
description: Evaluate student projects by analyzing markdown documentation
---

# Student Project Evaluator Skill

## When to Use
- User wants to grade/evaluate student coding projects
- User provides path to folder containing student submissions

## Execution Flow

### Step 1: Collect Input
- Get master folder path from user
- Confirm number of student folders found

### Step 2: Discovery Phase
- For each student folder:
  - Find all .md files
  - Read each file
  - Extract criteria with context validation
  - Add student to criteria graph

### Step 3: Categorization
- Match criteria to predefined categories
- Flag uncategorized for review

### Step 4: Calculate Weights & Grades
- Compute prevalence weights
- Score each student
- Assign relative grades

### Step 5: Generate Outputs
- Save criteria graph (JSON)
- Save flagged criteria (MD)
- Save grades (CSV)
- Generate evaluation report (MD)
```

### 3.2 Criteria Extraction Prompt

Claude uses semantic understanding to extract criteria:

```
When reading markdown content, extract:

1. **Features implemented**: "We built X", "The project includes Y"
2. **Testing**: "Unit tests", "Integration tests", "Test coverage"
3. **Documentation**: "README", "API docs", "Architecture docs"
4. **DevOps**: "CI/CD", "Docker", "Deployment"
5. **Research**: "Analysis", "Findings", "Data exploration"
6. **Visuals**: "Screenshots", "Diagrams", "Charts"
7. **Planning**: "PRD", "Design decisions", "Roadmap"
8. **Business**: "Cost analysis", "ROI", "Market research"

Context validation - DO NOT count if:
- "TODO: implement X"
- "X not yet implemented"
- "We plan to add X"
- "X is out of scope"
- "Future work: X"
```

### 3.3 Context Validation Logic

```
VALID patterns (count as implemented):
- "We implemented X"
- "The project has X"
- "X is included"
- "Built with X"
- "Features: X, Y, Z"
- Specific metrics: "80% test coverage"

INVALID patterns (do not count):
- "TODO:", "FIXME:"
- "not yet implemented"
- "planned", "will add", "future work"
- "out of scope"
- "skipped", "omitted"
```

---

## 4. Data Structures

### 4.1 Criteria Graph (Primary Data Structure)

```json
{
  "criteria": {
    "unit_tests": {
      "display_name": "Unit Tests",
      "students": ["alice", "bob", "carol"],
      "count": 3,
      "weight": 0.6,
      "category": "Testing",
      "sources": {
        "alice": "README.md",
        "bob": "TESTING.md",
        "carol": "README.md"
      }
    },
    "ci_cd_pipeline": {
      "display_name": "CI/CD Pipeline",
      "students": ["bob"],
      "count": 1,
      "weight": 0.2,
      "category": "DevOps",
      "sources": {
        "bob": "DEVOPS.md"
      }
    }
  },
  "metadata": {
    "total_students": 5,
    "total_criteria": 25,
    "categorized": 23,
    "uncategorized": 2
  }
}
```

### 4.2 Student Scores

```json
{
  "students": {
    "alice": {
      "criteria_present": ["unit_tests", "readme", "architecture"],
      "criteria_missing": ["ci_cd_pipeline", "cost_analysis"],
      "raw_score": 2.4,
      "max_possible": 3.2,
      "percentage": 75.0,
      "grade": 93.75,
      "rank": 2
    },
    "bob": {
      "criteria_present": ["unit_tests", "readme", "ci_cd_pipeline", "cost_analysis"],
      "criteria_missing": [],
      "raw_score": 3.2,
      "max_possible": 3.2,
      "percentage": 100.0,
      "grade": 100,
      "rank": 1
    }
  }
}
```

### 4.3 Flagged Criteria

```markdown
# Flagged Criteria for Manual Review

These criteria were extracted but could not be categorized.
Please review and either:
1. Add them to an existing category
2. Create a new category
3. Mark as irrelevant

## Uncategorized Criteria

| Criterion | Students | Count |
|-----------|----------|-------|
| "blockchain integration" | alice, bob | 2 |
| "AI chatbot" | carol | 1 |
| "custom logging framework" | diana | 1 |

## Action Required
Edit `categories.yml` to include these criteria or mark them as excluded.
```

---

## 5. File Structure

```
student-project-evaluator/
├── SKILL.md                          # Main Claude Code skill
├── README.md                         # User documentation
├── docs/
│   ├── PRD.md                        # Product requirements
│   ├── PLANNING.md                   # This file
│   ├── CLAUDE.md                     # Development rules
│   └── TASKS.md                      # Implementation tasks
├── config/
│   └── categories.yml                # Predefined criteria categories
├── outputs/                          # Generated files go here
│   ├── criteria_graph.json
│   ├── flagged_criteria.md
│   ├── grades.csv
│   └── evaluation_report.md
├── examples/
│   ├── sample_criteria_graph.json
│   └── sample_evaluation_report.md
└── tests/
    └── fixtures/
        ├── student_sample1/
        ├── student_sample2/
        └── student_sample3/
```

---

## 6. Category Configuration

### 6.1 categories.yml

```yaml
categories:
  Documentation:
    keywords:
      - readme
      - api docs
      - api documentation
      - user guide
      - changelog
      - contributing guide
      - license
    description: "Project documentation and guides"

  Testing:
    keywords:
      - unit tests
      - integration tests
      - e2e tests
      - end-to-end tests
      - test coverage
      - pytest
      - jest
      - testing framework
    description: "Testing and quality assurance"

  DevOps:
    keywords:
      - ci/cd
      - continuous integration
      - github actions
      - docker
      - containerization
      - deployment
      - kubernetes
      - monitoring
    description: "DevOps and deployment infrastructure"

  Planning:
    keywords:
      - prd
      - product requirements
      - architecture
      - design document
      - technical spec
      - roadmap
      - milestones
    description: "Planning and design documentation"

  Research:
    keywords:
      - research
      - analysis
      - findings
      - jupyter notebook
      - data exploration
      - experiment
      - hypothesis
    description: "Research and data analysis"

  Visuals:
    keywords:
      - screenshot
      - diagram
      - flowchart
      - chart
      - graph
      - demo video
      - gif
      - mockup
    description: "Visual documentation and demos"

  CodeQuality:
    keywords:
      - linting
      - eslint
      - prettier
      - type checking
      - typescript
      - code review
      - refactoring
      - clean code
    description: "Code quality and maintainability"

  Business:
    keywords:
      - cost analysis
      - roi
      - market research
      - user personas
      - business case
      - pricing
      - monetization
    description: "Business and market considerations"
```

---

## 7. Output Formats

### 7.1 grades.csv

```csv
Rank,Student,Grade,Percentage,Criteria_Count,Total_Criteria
1,bob,100,100.0,25,25
2,alice,93.75,75.0,20,25
3,carol,87.5,70.0,18,25
4,diana,81.25,65.0,16,25
5,eve,75.0,60.0,15,25
```

### 7.2 evaluation_report.md

```markdown
# Evaluation Report
Generated: 2025-12-17

## Summary
- **Total Students**: 35
- **Total Criteria Discovered**: 52
- **Categorized**: 48
- **Flagged for Review**: 4

## Criteria by Category

### Documentation (12 criteria)
| Criterion | Students | Weight |
|-----------|----------|--------|
| README | 35 | 1.00 |
| API docs | 20 | 0.57 |
| User guide | 8 | 0.23 |

### Testing (8 criteria)
...

## Grade Distribution
| Grade Range | Count |
|-------------|-------|
| 90-100 | 5 |
| 80-89 | 12 |
| 70-79 | 10 |
| 60-69 | 6 |
| Below 60 | 2 |

## Top 5 Students
1. **bob** (100) - 25/25 criteria
2. **alice** (93.75) - 20/25 criteria
...
```

---

## 8. Error Handling

### 8.1 Missing Markdown Files

```
If student folder has no .md files:
    - Log warning: "No markdown files found in {student_folder}"
    - Add student to results with 0 criteria
    - Continue processing other students
```

### 8.2 Unreadable Files

```
If file cannot be read:
    - Log warning: "Could not read {file_path}"
    - Skip file, continue with other files
    - Do not fail entire process
```

### 8.3 Empty Categories

```
If a category has no criteria after processing:
    - Keep category in output (shows no students had these features)
    - Do not remove category
```

---

## 9. Performance Considerations

### 9.1 Optimization Strategies

1. **Batch file reading**: Read all .md files for a student at once
2. **Parallel processing**: Process multiple students concurrently (if supported)
3. **Incremental output**: Write to files as processing completes
4. **Memory management**: Process one student at a time, don't load all content

### 9.2 Expected Performance

| Metric | Target |
|--------|--------|
| Per student (5 .md files) | <30 seconds |
| 35 students total | <20 minutes |
| Memory usage | <500MB |

---

**End of Architecture and Technical Planning**
