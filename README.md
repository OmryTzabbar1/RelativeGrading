# Student Project Evaluator

A Claude Code skill for comparative evaluation of student coding projects using dynamic baseline updates.

## Overview

This skill implements a comparative grading system where each student project is evaluated relative to the highest-graded project encountered so far. The baseline dynamically updates as better projects are discovered, ensuring fair relative assessment across all submissions.

## Features

- **Comparative Grading**: Evaluate students relative to the best submission
- **Dynamic Baseline**: Automatically updates when superior projects are found
- **Batch Processing**: Handles large classes efficiently (5 students at a time)
- **Multi-Language Support**: Detects JavaScript, Python, and Java projects
- **Automated Reports**: Generates CSV for gradebook import and markdown summary
- **Metadata Extraction**: Automatically identifies team names and student IDs

## Installation

1. Ensure Claude Code CLI is installed
2. Clone this repository:
   ```bash
   git clone https://github.com/OmryTzabbar1/RelativeGrading.git
   cd RelativeGrading
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### As a Claude Code Skill

From any directory in Claude Code CLI:

```
Use the student-project-evaluator skill
```

Claude will guide you through:
1. Providing the assignment description
2. Specifying the master folder containing student projects
3. Selecting the baseline student and their grade
4. Automatic evaluation of all students
5. Generation of grades.csv and evaluation_summary.md

### Manual Script Usage

The helper scripts can also be used independently:

```python
from scripts.scan_folders import scan_student_folders
from scripts.analyze_repo import analyze_repository

# Find all student folders
students = scan_student_folders('/path/to/assignments')

# Analyze a specific project
info = analyze_repository('/path/to/student_folder')
print(info['project_type'])
print(info['key_files'])
```

## Project Structure

```
student-project-evaluator/
├── .claude/
│   └── skills/
│       └── student-project-evaluator.md  # Main skill definition
├── docs/
│   ├── PRD.md                            # Product requirements
│   ├── PLANNING.md                       # Architecture & ADRs
│   ├── CLAUDE.md                         # Development conventions
│   └── TASKS.md                          # Implementation phases
├── scripts/
│   ├── analyze_repo.py                   # Project type detection
│   └── scan_folders.py                   # Student folder discovery
├── tests/
│   └── fixtures/                         # Sample student projects
├── examples/
│   └── assignment-config.yml             # Configuration template
└── requirements.txt
```

## Grading Methodology

### Evaluation Criteria

Each project is assessed on two dimensions (50% weight each):

1. **Assignment Relevance**: How well the project addresses requirements
2. **Functionality**: Implementation quality and completeness

### Scoring System

- Baseline student receives manually assigned grade (0-100)
- Subsequent students receive: `baseline_grade ± adjustment`
- Adjustments range from -10 to +20 points per criterion
- Final grades clamped to 0-100 range
- Baseline updates if a student scores higher

### Example Flow

```
Baseline: student_alice - 85/100

Evaluating student_bob:
- Assignment Relevance: +8 (added dark mode, extra features)
- Functionality: +7 (better error handling, cleaner code)
- Final Grade: 85 + 8 + 7 = 100/100
- New baseline: student_bob - 100/100

Evaluating student_carol (compared to student_bob):
- Assignment Relevance: -5 (missing features)
- Functionality: -8 (no LocalStorage, poor documentation)
- Final Grade: 100 - 5 - 8 = 87/100
```

## Output Files

### grades.csv

```csv
Student,ID,Grade,Rank,Team,Notes
student_bob,67890,100,1,Beta Squad,"Excellent implementation with dark mode"
student_alice,12345,85,2,Alpha Team,"Solid baseline with all requirements"
student_carol,,75,3,,"Missing update functionality"
```

### evaluation_summary.md

Contains:
- Overall statistics (mean, median, std deviation)
- Grade distribution histogram
- Individual evaluations with detailed feedback
- List of students requiring manual review

### assignment-config.yml

Generated after baseline calibration:
- Assignment details and criteria
- Baseline student features
- File focus patterns
- Grading weights (customizable)

## Development

### Running Tests

```bash
# Test helper scripts
python -c "from scripts.scan_folders import scan_student_folders; print(scan_student_folders('tests/fixtures/sample_assignment'))"

python -c "from scripts.analyze_repo import analyze_repository; print(analyze_repository('tests/fixtures/sample_assignment/student_alice'))"
```

### Code Conventions

- Maximum 150 lines per file
- PEP 8 style with type hints
- Docstrings for all public functions
- Commit format: `<type>(<scope>): <description> [TaskID]`

See [docs/CLAUDE.md](docs/CLAUDE.md) for full development guidelines.

## Architecture

Built as a Claude Code skill with Python helper utilities:
- **SKILL.md**: Orchestrates evaluation workflow
- **Python scripts**: Handle file operations and analysis
- **YAML configs**: Store evaluation criteria and results

For detailed architecture including C4 diagrams and ADRs, see [docs/PLANNING.md](docs/PLANNING.md).

## License

MIT License - see LICENSE file for details

## Contributing

This project follows the academic-msc guideline for quality standards.

See [docs/TASKS.md](docs/TASKS.md) for current implementation phases.

## Support

For issues or questions:
- Open an issue on GitHub
- Refer to docs/ folder for detailed documentation
- Check examples/ for sample configurations
