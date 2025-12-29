# Student Project Evaluation Workflow

Complete guide for evaluating multiple submission folders with unique outputs.

---

## Quick Start

To evaluate a submission folder (e.g., WorkSubmissions04):

```bash
# Step 1: Run evaluation (via Claude Code skill)
# This creates outputs in outputs/ directory

# Step 2: Organize outputs into submission-specific folder
python organize_outputs.py WorkSubmissions04

# Step 3: Compare with actual grades
python compare_grades.py WorkSubmissions04
```

**Result:** All outputs saved to `outputs/WorkSubmissions04/`

---

## Detailed Workflow

### Step 1: Run Evaluation

**Option A: Using Claude Code CLI**
```bash
claude skill evaluating-student-projects tests/WorkSubmissions04
```

**Option B: Direct prompt to Claude**
```
Evaluate tests/WorkSubmissions04
```

This will:
- Read all .md files from 20+ student folders
- Extract 40-50 criteria (including Quality Standards)
- Generate initial outputs in `outputs/` directory

**Initial outputs created:**
- `outputs/criteria_graph_final.json`
- `outputs/grades.xlsx`
- `outputs/Student_Evaluation_Report.xlsx`
- `outputs/EVALUATION_SUMMARY.md`

---

### Step 2: Organize Outputs

Move outputs to submission-specific folder:

```bash
python organize_outputs.py WorkSubmissions04
```

**What this does:**
- Creates `outputs/WorkSubmissions04/` directory
- Moves all evaluation files there
- Keeps outputs organized by submission

**After organization:**
```
outputs/
├── WorkSubmissions04/
│   ├── criteria_graph_final.json
│   ├── grades.xlsx
│   ├── Student_Evaluation_Report.xlsx
│   └── EVALUATION_SUMMARY.md
```

---

### Step 3: Compare with Actual Grades

Generate grade comparison report:

```bash
python compare_grades.py WorkSubmissions04
```

**What this does:**
- Loads evaluator grades from `outputs/WorkSubmissions04/grades.xlsx`
- Finds student PDFs in `tests/WorkSubmissions04/`
- Extracts actual grades from `Detailed_Grade_Breakdown_{student_id}.pdf`
- Calculates correlation, RMSE, accuracy metrics
- Generates comparison Excel in `outputs/WorkSubmissions04/grade_comparison.xlsx`

**Output:**
```
================================================================================
GRADE COMPARISON TOOL - WorkSubmissions04
================================================================================

Mean Evaluator Grade:   75.7
Mean Actual Grade:      75.5
Mean Difference:        +0.2 (nearly perfect!)
Correlation:            0.782 (strong)
Students within ±10:    55.0%

Saved: outputs/WorkSubmissions04/grade_comparison.xlsx
```

---

## Evaluating Multiple Submissions

To evaluate multiple submission folders without conflicts:

### Example: Evaluate WorkSubmissions04, 05, and 06

```bash
# Evaluate WorkSubmissions04
claude "Evaluate tests/WorkSubmissions04"
python organize_outputs.py WorkSubmissions04
python compare_grades.py WorkSubmissions04

# Evaluate WorkSubmissions05
claude "Evaluate tests/WorkSubmissions05"
python organize_outputs.py WorkSubmissions05
python compare_grades.py WorkSubmissions05

# Evaluate WorkSubmissions06
claude "Evaluate tests/WorkSubmissions06"
python organize_outputs.py WorkSubmissions06
python compare_grades.py WorkSubmissions06
```

**Final directory structure:**
```
outputs/
├── WorkSubmissions04/
│   ├── criteria_graph_final.json
│   ├── grades.xlsx
│   ├── Student_Evaluation_Report.xlsx
│   ├── EVALUATION_SUMMARY.md
│   └── grade_comparison.xlsx
├── WorkSubmissions05/
│   ├── criteria_graph_final.json
│   ├── grades.xlsx
│   ├── Student_Evaluation_Report.xlsx
│   ├── EVALUATION_SUMMARY.md
│   └── grade_comparison.xlsx
└── WorkSubmissions06/
    ├── criteria_graph_final.json
    ├── grades.xlsx
    ├── Student_Evaluation_Report.xlsx
    ├── EVALUATION_SUMMARY.md
    └── grade_comparison.xlsx
```

---

## Output Files Explained

### 1. criteria_graph_final.json
**Purpose:** Complete criteria database
**Contents:**
- All 40-50 criteria discovered
- Which students have each criterion
- Weights (prevalence-based)
- Categories (CodeQuality, Planning, Testing, etc.)

**Use:** Programmatic analysis, debugging

### 2. grades.xlsx
**Purpose:** Student rankings
**Contents:**
- Student ID
- Raw Score
- Max Possible
- Percentage
- Grade (relative, 0-100)
- Rank (1 = highest)
- Criteria Count

**Use:** Quick grade lookup, import to LMS

### 3. Student_Evaluation_Report.xlsx
**Purpose:** Comprehensive multi-sheet report
**Sheets:**
1. Summary - Overview statistics
2. Grades - Full student rankings
3. Criteria Distribution - Which criteria are common
4. Category Breakdown - Points by category
5. Student Details - Per-student criteria lists
6. Flagged Criteria - Uncategorized items

**Use:** Detailed analysis, instructor review

### 4. EVALUATION_SUMMARY.md
**Purpose:** Human-readable narrative report
**Contents:**
- Executive summary
- Top students
- Criteria analysis by category
- Grade distribution
- Recommendations

**Use:** Share with stakeholders, documentation

### 5. grade_comparison.xlsx (after Step 3)
**Purpose:** Evaluator vs actual grade comparison
**Sheets:**
1. Comparison - Student-by-student comparison
2. Statistics - Correlation, RMSE, accuracy metrics
3. Discrepancies - Students with large differences (>10 points)

**Use:** Validate evaluator accuracy, identify outliers

---

## Key Features

### Criteria Extracted (48 total for WorkSubmissions04)

**CodeQuality (13 criteria):**
- ESLint, Pylint, Ruff, Flake8 configurations
- Prettier, Black formatting
- Pre-commit hooks
- TypeScript, Mypy type checking
- Code style guides, PEP8 compliance
- Code review processes
- Quality gates

**Planning (9 criteria):**
- PRD, Architecture documentation
- Problem Statement, Solution Overview
- Requirements, Use Cases
- Success Metrics, Assumptions
- Roadmap, Design Rationale

**Testing (4 criteria):**
- Unit, Integration, E2E tests
- Test coverage metrics

**Documentation (5 criteria):**
- README, API docs
- Usage guides, Contributing guides
- Changelog

**DevOps (2 criteria):**
- CI/CD pipelines
- Docker containerization

**Research (3 criteria):**
- Cost Analysis, Risk Analysis
- User Research

**Visuals (1 criterion):**
- Screenshots

**Uncategorized (11 criteria):**
- Implementation-specific items

---

## Troubleshooting

### Problem: "Could not find outputs/WorkSubmissions04/grades.xlsx"

**Solution:** Run `organize_outputs.py` first:
```bash
python organize_outputs.py WorkSubmissions04
```

### Problem: "No files found to move"

**Cause:** Evaluation hasn't been run yet
**Solution:** Run evaluation first via Claude Code skill

### Problem: Outputs getting overwritten

**Cause:** Running multiple evaluations without organizing
**Solution:** Always run `organize_outputs.py` after each evaluation

### Problem: "WorkSubmissions path does not exist"

**Cause:** Incorrect submission name
**Solution:** Check folder name in `tests/` directory:
```bash
ls tests/
```

---

## Advanced Usage

### Compare Multiple Submissions

```bash
# After evaluating all submissions
python -c "
import pandas as pd

ws04 = pd.read_excel('outputs/WorkSubmissions04/grade_comparison.xlsx', sheet_name='Statistics')
ws05 = pd.read_excel('outputs/WorkSubmissions05/grade_comparison.xlsx', sheet_name='Statistics')
ws06 = pd.read_excel('outputs/WorkSubmissions06/grade_comparison.xlsx', sheet_name='Statistics')

print('Assignment Comparison:')
print(f'WS04 Correlation: {ws04.loc[ws04[\"Metric\"] == \"Correlation\", \"Value\"].values[0]:.3f}')
print(f'WS05 Correlation: {ws05.loc[ws05[\"Metric\"] == \"Correlation\", \"Value\"].values[0]:.3f}')
print(f'WS06 Correlation: {ws06.loc[ws06[\"Metric\"] == \"Correlation\", \"Value\"].values[0]:.3f}')
"
```

### Extract Criteria Trends

```bash
# Compare criteria across assignments
python -c "
import json

with open('outputs/WorkSubmissions04/criteria_graph_final.json') as f:
    ws04 = json.load(f)

with open('outputs/WorkSubmissions05/criteria_graph_final.json') as f:
    ws05 = json.load(f)

print('Criteria Comparison:')
print(f'WS04: {ws04[\"metadata\"][\"total_criteria\"]} criteria')
print(f'WS05: {ws05[\"metadata\"][\"total_criteria\"]} criteria')
"
```

---

## Files in This Repository

### Evaluation Scripts
- `.claude/skills/evaluating-student-projects/` - Main evaluation skill
- `organize_outputs.py` - Organize outputs by submission
- `compare_grades.py` - Compare evaluator vs actual grades

### Configuration
- `.claude/skills/evaluating-student-projects/EXTRACTION.md` - Criteria extraction rules
- `.claude/skills/evaluating-student-projects/CATEGORIES.md` - Category definitions

### Documentation
- `EVALUATION_WORKFLOW.md` - This file
- `outputs/evaluator_gap_analysis.md` - Analysis of evaluator accuracy
- `outputs/quality_standards_impact.md` - Impact of Quality Standards

### Deprecated (for reference)
- `compare_ws04.py` - Old WorkSubmissions04-specific script (replaced by compare_grades.py)
- `.claude/skills/grade-comparison/` - Old comparison skill (replaced by compare_grades.py)

---

## Best Practices

1. **Always organize outputs immediately after evaluation**
   ```bash
   python organize_outputs.py WorkSubmissions04
   ```

2. **Run grade comparison to validate accuracy**
   ```bash
   python compare_grades.py WorkSubmissions04
   ```

3. **Keep submission folders separate**
   - Don't mix WorkSubmissions04 and WorkSubmissions05 outputs
   - Use unique output folders for each

4. **Review flagged criteria**
   - Check `Student_Evaluation_Report.xlsx` → "Flagged Criteria" sheet
   - Manually categorize uncategorized items if needed

5. **Validate evaluator accuracy**
   - Aim for correlation > 0.7 (strong)
   - Aim for mean difference < ±5 points
   - Aim for >50% students within ±10 points

---

## Summary

**3-Step Workflow:**
1. **Evaluate:** Run Claude Code skill on submission folder
2. **Organize:** `python organize_outputs.py <submission_name>`
3. **Compare:** `python compare_grades.py <submission_name>`

**Result:** Clean, organized, submission-specific outputs that don't overwrite each other.
