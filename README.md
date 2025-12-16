# Student Project Evaluator v2.0

**Sliding Window Criteria Discovery Approach**

A Python-based tool for fair, comprehensive evaluation of student coding projects using dynamic criteria discovery through sliding window analysis.

## Overview

The Student Project Evaluator v2.0 addresses a fundamental challenge in academic evaluation: how to fairly grade student projects when the full spectrum of quality and approaches isn't known upfront.

### The Problem

Traditional evaluation approaches face three critical issues:

1. **Premature Criteria**: Defining rubrics before seeing student work misses innovative approaches
2. **Baseline Bias**: Comparing all students to a single baseline may not capture the full range of quality
3. **Inconsistent Standards**: Early students evaluated against incomplete criteria

### The Solution: Sliding Window Criteria Discovery

This tool uses a **two-phase evaluation approach**:

**Phase 1: Criteria Discovery**
- Analyzes students in overlapping windows of 3
- Builds comprehensive criteria organically from all projects
- Tracks which student introduced each quality dimension

**Phase 2: Final Evaluation**
- Evaluates ALL students against the same complete criteria
- Assigns TRUE relative grades (only best student gets 100)
- Generates comprehensive reports with statistics

## Key Features

- ✅ **Dynamic Criteria Building**: Discovers evaluation criteria from actual student work
- ✅ **Fair Comparison**: All students judged by same complete criteria
- ✅ **True Relative Grading**: Best student = 100, others scaled proportionally
- ✅ **Comprehensive Analysis**: Evaluates documentation, testing, graphics, research, code quality
- ✅ **Transparent Reporting**: Detailed CSV and markdown reports with evolution log
- ✅ **Progress Tracking**: Real-time display of analysis progress

## Installation

### Requirements

- Python 3.8+
- PyYAML 6.0+

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd student-project-evaluator

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py <path-to-student-projects-folder>
```

### Advanced Options

```bash
python main.py <master-folder> \
    --window-size 3 \
    --output-dir ./outputs \
    --exclude baseline_student \
    --exclude .git
```

#### Arguments

- `master_folder` (required): Path to folder containing student project folders
- `--window-size N`: Window size for sliding analysis (default: 3)
- `--output-dir PATH`: Output directory for results (default: ./outputs)
- `--exclude FOLDER`: Folders to exclude (can be repeated)

### Example

```bash
# Evaluate 35 student projects with default settings
python main.py "E:/Assignments/WebDev_A1/"

# Use larger window size and custom output directory
python main.py "E:/Assignments/WebDev_A1/" \
    --window-size 5 \
    --output-dir ./results
```

## How It Works

### Phase 1: Criteria Discovery

```
Students: [1, 2, 3, 4, 5, ..., N]

Window 1: [1, 2, 3] → Discover initial criteria C1
Window 2: [2, 3, 4] → Update criteria C2 = C1 + new features from 4
Window 3: [3, 4, 5] → Update criteria C3 = C2 + new features from 5
...
Window N-2: [N-2, N-1, N] → Final complete criteria CF
```

**What's Discovered**:
- Documentation (README, PRD, Architecture docs, PROMPT_BOOK)
- Testing (test files, coverage, test types)
- Graphics (images, diagrams, charts)
- Research (notebooks, analysis documents)
- Code Quality (structure, organization, file count)

### Phase 2: Final Evaluation

1. **Score All Students**: Each student scored against complete criteria
2. **Calculate Quality Scores**: Composite score across all dimensions
3. **Assign Relative Grades**:
   - Best student: 100
   - 95%+ of best: 90-99
   - 80-95% of best: 75-89
   - 60-80% of best: 60-74
   - Below 60%: proportional
4. **Rank Students**: 1 = highest quality score

## Output Files

After evaluation, three files are generated in the output directory:

### 1. `discovered_criteria.yml`

Complete criteria with evolution log showing which student introduced each dimension.

```yaml
criteria:
  documentation:
    readme:
      present: true
      lines: 200
    prd:
      present: true
      weight: 5
  testing:
    present: true
    test_file_count: 10
  ...

evolution:
  - student: student_alice
    dimension: documentation
    properties: {...}
  - student: student_bob
    dimension: testing
    properties: {...}
```

### 2. `grades.csv`

Spreadsheet with grades and dimension scores for all students.

```csv
Student,Grade,Rank,Quality Score,documentation,testing,graphics,research,code_quality
student_alice,100,1,153.00,30.00,33.00,30.00,20.00,40.00
student_bob,91,2,147.00,38.00,27.00,22.00,20.00,40.00
...
```

### 3. `evaluation_report.md`

Comprehensive markdown report including:
- Summary statistics (mean, median, std dev)
- Grade distribution
- Criteria evolution log
- Top 10 projects
- Individual student evaluations with dimension breakdowns

## Project Structure

```
student-project-evaluator/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── scripts/
│   ├── sliding_window_analyzer.py   # Phase 1: Criteria discovery
│   ├── criteria_builder.py          # DiscoveredCriteria class
│   ├── final_evaluator.py           # Phase 2: Final evaluation
│   ├── analyze_project.py           # Project feature extraction
│   ├── output_generator.py          # CSV and markdown generation
│   └── utils.py                     # Helper functions
├── outputs/                         # Generated output files
├── tests/                           # Test scripts and fixtures
└── docs/                            # Documentation
    ├── PRD.md                       # Product requirements
    ├── PLANNING.md                  # Architecture
    ├── TASKS.md                     # Implementation tasks
    └── CLAUDE.md                    # Development rules
```

## Development

### Running Tests

```bash
# Test data structures
python test_structures.py

# Test full pipeline (10 students)
python test_pipeline.py
```

### Architecture

The system is built around two core classes:

**DiscoveredCriteria**
- Manages quality dimensions discovered during sliding window analysis
- Tracks evolution (which student added what)
- Exports to YAML format

**StudentEvaluation**
- Tracks scores across all quality dimensions
- Calculates composite quality score
- Stores final grade and rank

## Troubleshooting

### No students found

**Problem**: "No student folders found!"

**Solution**: Check that:
- Master folder path is correct
- Student projects are in subdirectories
- Folders aren't hidden (starting with '.')

### Student got 0 grade

**Problem**: Student received 0/100

**Possible causes**:
- Empty project folder
- No recognizable features (no code, docs, tests, etc.)
- Folder contains only metadata files

**Solution**: Manually inspect the student's folder

### Window size errors

**Problem**: "window_size must be at least 1"

**Solution**: Use `--window-size 3` or higher (recommended: 3-5)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2025-12-16 | Complete redesign with sliding window approach |
| 1.0 | 2024-12-15 | Initial baseline comparison approach |

## License

MIT License

## Contributing

This is an academic project for M.Sc. Computer Science. For questions or suggestions, please contact the development team.

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**

**Co-Authored-By**: Claude Sonnet 4.5 <noreply@anthropic.com>
