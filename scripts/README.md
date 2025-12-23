# Student Project Evaluator Scripts

This directory contains utility scripts organized by purpose.

## Directory Structure

```
scripts/
├── experimental/     # Alternative evaluation implementations
├── dev/             # Development & testing utilities
└── README.md        # This file
```

## Core Workflow Scripts

The **core evaluation scripts** used in the standard workflow are located in:
```
.claude/skills/evaluating-student-projects/scripts/
```

These include:
- `smart_grouping.py` - Step 6: Consolidate tech variations
- `recalculate_grades.py` - Step 9: Calculate grades
- `create_excel_report.py` - Step 10: Generate Excel reports

See `.claude/skills/evaluating-student-projects/scripts/README.md` for details.

## Experimental Scripts

**Location:** `scripts/experimental/`

Alternative evaluation implementations and experimental approaches:
- `comprehensive_evaluation.py` - Enhanced extraction rules
- `granular_evaluation.py` - Very specific criteria extraction
- `evaluate_criteria.py` - WorkSubmissions01-specific evaluator

These are **not** part of the standard workflow. See `scripts/experimental/README.md` for details.

## Development Utilities

**Location:** `scripts/dev/`

Validation and analysis scripts for development:
- `validate_output.py` - Comprehensive validation
- `validate_simple.py` - Quick validation
- `analyze_results.py` - Criteria distribution analysis
- `verify_student.py` - Single student criteria check
- `sample_students_report.py` - Sample student reports

See `scripts/dev/README.md` for details.

## Quick Reference

### Standard Workflow
```bash
# Core scripts (after criteria extraction)
cd .claude/skills/evaluating-student-projects/scripts
python smart_grouping.py
python recalculate_grades.py
python create_excel_report.py
```

### Validation
```bash
cd scripts/dev
python validate_output.py
```

### Analysis
```bash
cd scripts/dev
python analyze_results.py
```
