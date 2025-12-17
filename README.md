# Student Project Evaluator v3.0

**Markdown-Based Criteria Discovery**

A Claude Code skill for fair, comprehensive evaluation of student coding projects by analyzing their markdown documentation.

## Overview

The Student Project Evaluator v3.0 discovers evaluation criteria organically by reading students' `.md` files (README, PRD, Architecture docs, etc.), then grades everyone against the complete discovered criteria.

### Key Innovation

Instead of scanning code files or using predetermined rubrics, this tool:

1. **Reads markdown files** - READMEs and docs provide holistic project summaries
2. **Extracts criteria** - Discovers what students actually built
3. **Validates context** - Only counts implemented features (not TODOs)
4. **Weights by prevalence** - Common criteria matter more than rare ones
5. **Grades relatively** - Best student = 100, others scaled proportionally

## How It Works

```
For each student:
    Find all .md files
    Extract criteria (with context validation)
    Add student to criteria graph

Build weights: weight = students_with_criterion / total_students
Score students: sum of weights for criteria they have
Grade: relative to best student
```

### Example

| Criterion | Students | Weight | Meaning |
|-----------|----------|--------|---------|
| README | 35/35 | 1.00 | Core requirement |
| Unit tests | 28/35 | 0.80 | Important feature |
| CI/CD | 10/35 | 0.29 | Nice to have |
| Cost analysis | 3/35 | 0.09 | Bonus feature |

Students missing high-weight criteria are penalized more than those missing low-weight criteria.

## Features

- **Markdown-first analysis** - Fast, holistic project understanding
- **Context-aware extraction** - "TODO: add tests" doesn't count
- **Prevalence weighting** - Fair, class-relative grading
- **Automatic categorization** - Groups criteria into topics
- **Flagged items review** - Uncategorized criteria saved for manual review
- **Comprehensive outputs** - CSV, JSON, and markdown reports

## Installation

This is a Claude Code skill. No additional installation required beyond Claude Code itself.

```bash
# Clone the repository
git clone <repository-url>
cd student-project-evaluator
```

The skill is located in `.claude/skills/evaluating-student-projects/`.

## Usage

Simply ask Claude Code to evaluate your student projects:

```
Evaluate the student projects in /path/to/submissions/
```

Or more specific requests:

```
Grade the assignments in E:/Courses/CS101/Assignment1/
```

```
Compare student work in /Assignments/WebDev/ and generate a grade report
```

### What Claude Does

1. **Discovers students** - Scans folder for subdirectories
2. **Reads markdown** - Finds all .md files in each student folder
3. **Extracts criteria** - Identifies features, tests, docs, etc.
4. **Validates context** - Filters out "TODO" and "not implemented" items
5. **Builds graph** - Tracks which students have which criteria
6. **Categorizes** - Groups into Documentation, Testing, DevOps, etc.
7. **Calculates weights** - Based on class prevalence
8. **Grades students** - Relative scoring with best = 100
9. **Generates outputs** - CSV, JSON, and markdown reports

## Output Files

Generated in `outputs/` directory:

| File | Description |
|------|-------------|
| `criteria_graph.json` | Complete criteria data with students and weights |
| `flagged_criteria.md` | Uncategorized items for manual review |
| `grades.csv` | Student grades for import into grading systems |
| `evaluation_report.md` | Full analysis with statistics and breakdowns |

### Sample grades.csv

```csv
Rank,Student,Grade,Percentage,Criteria_Count,Total_Criteria
1,alice,100.0,80.5,45,89
2,bob,96.2,77.4,43,89
3,carol,94.1,75.8,42,89
```

## Criteria Categories

Extracted criteria are grouped into:

| Category | Examples |
|----------|----------|
| Documentation | README, API docs, user guide |
| Planning | PRD, architecture, design docs |
| Testing | Unit tests, integration tests, coverage |
| DevOps | CI/CD, Docker, deployment |
| Research | Analysis notebooks, findings |
| Visuals | Screenshots, diagrams, charts |
| Code Quality | Linting, type checking |
| Business | Cost analysis, ROI, market research |

Criteria that don't fit are flagged for manual review.

## Project Structure

```
student-project-evaluator/
├── .claude/
│   └── skills/
│       └── evaluating-student-projects/
│           ├── SKILL.md           # Main skill instructions
│           ├── CATEGORIES.md      # Category definitions
│           ├── EXTRACTION.md      # Extraction rules
│           └── OUTPUT-FORMATS.md  # Output specifications
├── docs/
│   ├── PRD.md                     # Product requirements
│   ├── PLANNING.md                # Architecture
│   ├── TASKS.md                   # Implementation tasks
│   └── CLAUDE.md                  # Development rules
├── outputs/                       # Generated files
├── tests/                         # Test fixtures
└── README.md                      # This file
```

## Context Validation

The skill validates that criteria are actually implemented:

| Pattern | Counts? |
|---------|---------|
| "We implemented unit tests" | Yes |
| "Test coverage is 85%" | Yes |
| "TODO: add unit tests" | No |
| "Unit tests not yet implemented" | No |
| "We plan to add CI/CD" | No |

## Troubleshooting

### No criteria extracted

**Cause**: Students may have minimal markdown documentation.

**Solution**: Check that students have README.md or other .md files with content.

### Student got very low grade

**Cause**: Missing high-weight (common) criteria.

**Check**: Look at `criteria_graph.json` to see what they're missing.

### Too many flagged criteria

**Cause**: Category keywords may need expansion.

**Solution**: Review `flagged_criteria.md` and update CATEGORIES.md.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2025-12-17 | Markdown-based discovery, prevalence weighting |
| 2.0 | 2025-12-16 | Sliding window approach |
| 1.0 | 2024-12-15 | Initial baseline comparison |

## License

MIT License

---

**Built with [Claude Code](https://claude.com/claude-code)**
