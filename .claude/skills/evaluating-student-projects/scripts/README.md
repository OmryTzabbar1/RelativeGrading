# Core Evaluation Scripts

These scripts are used in the student project evaluation workflow as defined in SKILL.md.

## Scripts

### 1. smart_grouping.py
**Used in:** Step 6 - Smart Grouping

**Purpose:** Consolidates technology-specific criteria into general capability categories for fair, tech-agnostic comparison.

**Example Consolidations:**
- Black + Ruff + ESLint + MyPy → "Code Quality Tools"
- Pytest + Jest + Mocha → "Unit Testing Framework"
- React + Vue + Angular → "Frontend Framework"

**Input:** `outputs/criteria_graph_final.json` (raw criteria)
**Output:** `outputs/criteria_graph_grouped.json` (consolidated criteria)

**Usage:**
```bash
python smart_grouping.py
```

### 2. recalculate_grades.py
**Used in:** Step 9 - Score and Grade

**Purpose:** Calculates student grades with prevalence-based weighting and rarity bonuses.

**Grading Formula:**
- Base Score = (sum of weighted criteria) / (max possible weight) × 100
- Rarity Bonus = +1 point for each criterion with ≤15% prevalence
- Final Score = Base Score + Rarity Bonus (capped at 100)

**Input:** `outputs/criteria_graph_grouped.json`
**Output:** Console output with rankings and scores

**Usage:**
```bash
python recalculate_grades.py
```

### 3. create_excel_report.py
**Used in:** Step 10 - Generate Outputs

**Purpose:** Creates comprehensive Excel workbook with multiple sheets including:
- Final grades and rankings
- Detailed criteria breakdown
- Comparison charts
- Category distribution

**Input:**
- `outputs/criteria_graph_grouped.json`
- `outputs/criteria_graph_final.json`

**Output:** `outputs/grades.xlsx` (multi-sheet Excel report)

**Usage:**
```bash
python create_excel_report.py
```

## Workflow Integration

These scripts are typically run in sequence after criteria extraction:

```bash
# After Step 5: Build Criteria Graph (creates criteria_graph_final.json)
cd .claude/skills/evaluating-student-projects/scripts

# Step 6: Smart Grouping
python smart_grouping.py

# Step 9: Calculate Grades
python recalculate_grades.py

# Step 10: Generate Excel Report
python create_excel_report.py
```

## Dependencies

All scripts require:
- Python 3.8+
- openpyxl (for Excel generation)
- Standard library: json, collections

Install dependencies:
```bash
pip install openpyxl
```
